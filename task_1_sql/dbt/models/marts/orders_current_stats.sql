{{ config(
    materialized='table',
    description='Кол-во заказов апо статусам'
) }}

WITH current_orders AS (
    SELECT 
        status,
        COUNT(*) AS total_orders,
        MIN(updated_at) AS earliest_order,
        MAX(updated_at) AS latest_order
    FROM {{ ref('stg_orders_deduplicated') }}
    GROUP BY status
)

SELECT 
    status,
    total_orders,
    earliest_order,
    latest_order,
    ROUND(100.0 * total_orders / SUM(total_orders) OVER (), 2) AS percentage
FROM current_orders
ORDER BY 
     status
