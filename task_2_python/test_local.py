"""
Local test with CSV file (no AWS required)
Tests the main processor.py functions
"""

import os
import csv
import sys


# Add parent directory to path to import processor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from main processor
from processor import encrypt_email
from cryptography.fernet import Fernet

# Set a test key (for local testing only)
os.environ['FERNET_KEY'] = Fernet.generate_key().decode()

# Re-import to pick up the key (or just use the functions)
from processor import cipher



# Path to your CSV file
csv_path = os.path.join(os.path.dirname(__file__), 'test_data.csv')

print(f"Reading: {csv_path}")
print()

# Read and process
processed_rows = []
original_emails = []

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    
    for row in reader:
        original_emails.append(row.get('email', ''))
        row['email'] = encrypt_email(row.get('email', ''))
        processed_rows.append(row)
        
        # print(f"  {original_emails[-1][:30]} → {row['email'][:40]}...")


print(f"Processed {len(processed_rows)} rows")
print()

# Save result
output_path = os.path.join(os.path.dirname(__file__), 'test_data_encrypted.csv')
with open(output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(processed_rows)

print(f"Saved to: {output_path}")
print()


print(" Test completed!")
