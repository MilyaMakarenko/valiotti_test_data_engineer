import pandas as pd
from datetime import datetime, timedelta
import random
import os

def generate_orders_data(num_orders=3, output_path="C:/tests/valiotti_test_data_engineer/scripts/init.sql"):
    """
    to SQL
    """
    
    # Statuses
    status = 'new' # ['new', 'processing', 'shipped', 'delivered', 'cancelled']
    
    # orders
    orders_data = []
    base_date = datetime(2026, 1, 1)
    
    for order_id in range(1, num_orders + 1):
        # Базовое время для каждого заказа (разные даты)
        order_date = base_date + timedelta(days=order_id - 1)
        
        # Только один статус 'new' для каждого заказа
        order_datetime = order_date.replace(
            hour=random.randint(8, 12),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )

        orders_data.append({
            'order_id': order_id,
            'status': status,
            'updated_at': order_datetime
        })
        orders_data.sort(key=lambda x: (x['order_id'], x['updated_at']))
    
    # SQL 
    sql_content = """
-- creating schema
CREATE SCHEMA IF NOT EXISTS raw;

-- creating table
CREATE TABLE IF NOT EXISTS raw.stg_orders (
    order_id INTEGER,
    status VARCHAR(50),
    updated_at TIMESTAMP
);

-- clear
TRUNCATE TABLE raw.stg_orders;

-- insert new dara
INSERT INTO raw.stg_orders (order_id, status, updated_at) VALUES
"""
    

    values = []
    for row in orders_data:
        values.append(f"    ({row['order_id']}, '{row['status']}', '{row['updated_at']}')")
        print( (f"    ({row['order_id']}, '{row['status']}', '{row['updated_at']}')") )
    
    sql_content += ",\n".join(values) + ";\n"
    
    # Save
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(sql_content)
    


    
    return orders_data

if __name__ == "__main__":
    generate_orders_data(num_orders=3)