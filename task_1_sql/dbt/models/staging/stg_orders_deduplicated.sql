WITH ranked AS (
    SELECT 
        order_id,
        status,
        updated_at,
        ROW_NUMBER() OVER (
            PARTITION BY order_id, status
            ORDER BY updated_at DESC
        ) as rn
    FROM {{ source('raw', 'stg_orders') }}
    WHERE order_id IS NOT NULL
      AND status IS NOT NULL
      AND updated_at IS NOT NULL
)

SELECT 
    order_id,
    status,
    updated_at
FROM ranked
WHERE rn = 1
ORDER BY order_id, updated_at