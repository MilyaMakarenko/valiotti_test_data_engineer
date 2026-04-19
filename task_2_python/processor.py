import os
import csv
import io
import logging
from typing import Dict, List, Any

import boto3
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET', 'gdpr-processed-bucket')
OUTPUT_PREFIX = os.environ.get('OUTPUT_PREFIX', 'processed')
BATCH_SIZE = int(os.environ.get('BATCH_SIZE', '5000'))  
FERNET_KEY = os.environ.get('FERNET_KEY')


# Validate required config
if not FERNET_KEY:
    raise RuntimeError('FERNET_KEY environment variable is required')

# Initialize encryption
cipher = Fernet(FERNET_KEY.encode())

# Encrypt email address using Fernet symmetric encryption
def encrypt_email(email: str) -> str: # type: ignore
    if not email or email.strip() == '':
        return ''
    return cipher.encrypt(email.encode('utf-8')).decode('utf-8')

# Process CSV file from S3
def process_csv_file(bucket: str, key: str) -> Dict[str, Any]:
    logger.info(f"Processing s3://{bucket}/{key}")
    
    # Get S3 client
    s3 = boto3.client('s3')
    
    # Open S3 file as streaming text
    response = s3.get_object(Bucket=bucket, Key=key)
    text_stream = io.TextIOWrapper(response['Body'], encoding='utf-8')
    reader = csv.DictReader(text_stream)
    
    # Prepare output
    base_name = os.path.basename(key)
    output_key = f"{OUTPUT_PREFIX}/{base_name}"
    
    # Collect all processed rows (for small files) or write in chunks
    processed_rows = []
    row_count = 0
    
    for row in reader:
        # Encrypt email field
        if 'email' in row:
            row['email'] = encrypt_email(row['email'])
        else:
            logger.warning(f"Row {row_count}: missing 'email' column")
        
        processed_rows.append(row)
        row_count += 1
        
        # Write batch when reaching batch size
        if len(processed_rows) >= BATCH_SIZE:
            write_batch_to_s3(processed_rows, reader.fieldnames, output_key, row_count)
            processed_rows = []
    
    # Write remaining rows
    if processed_rows:
        write_batch_to_s3(processed_rows, reader.fieldnames, output_key, row_count)
    
    logger.info(f"Processed {row_count} rows from {key}")
    
    return {
        'source': f"s3://{bucket}/{key}",
        'destination': f"s3://{OUTPUT_BUCKET}/{OUTPUT_PREFIX}/",
        'rows_processed': row_count
    }

# Write a batch of rows to S3 as CSV
def write_batch_to_s3(rows: List[Dict], fieldnames: List[str], output_key: str, batch_num: int) -> None:

    s3 = boto3.client('s3')
    
    # Create CSV in memory
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    
    # Upload to S3
    batch_key = f"{output_key}.batch-{batch_num:06d}.csv"
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=batch_key,
        Body=buffer.getvalue().encode('utf-8')
    )
    logger.info(f"Wrote {len(rows)} rows to s3://{OUTPUT_BUCKET}/{batch_key}")


# AWS Lambda handler
def handler(event: Dict, context: Any) -> Dict:
    """
    {
        "bucket": "raw-data-bucket",
        "key": "incoming/users_20240115.csv"
    }
    """
    try:
        bucket = event.get('bucket')
        key = event.get('key')
        
        if not bucket or not key:
            raise ValueError("Event must contain 'bucket' and 'key' fields")
        
        result = process_csv_file(bucket, key)
        
        return {
            'statusCode': 200,
            'body': result
        }
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        return {
            'statusCode': 500,
            'body': {'error': str(e)}
        }
    
if __name__ == "__main__":
    print("GDPR Processor - Ready")
    print(f"Output bucket: {OUTPUT_BUCKET}")
    print(f"Batch size: {BATCH_SIZE}")