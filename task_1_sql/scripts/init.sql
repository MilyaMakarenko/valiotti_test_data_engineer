
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
    (1, 'new', '2026-01-01 11:13:44'),
    (2, 'new', '2026-01-02 12:25:14'),
    (3, 'new', '2026-01-03 12:44:07');
