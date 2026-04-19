WITH funnel AS (
    SELECT 
        COUNT(DISTINCT CASE WHEN status = 'new' THEN order_id END) AS new_orders,
        COUNT(DISTINCT CASE WHEN status = 'processing' THEN order_id END) AS processing_orders,
        COUNT(DISTINCT CASE WHEN status = 'shipped' THEN order_id END) AS shipped_orders,
        COUNT(DISTINCT CASE WHEN status = 'delivered' THEN order_id END) AS delivered_orders,
        COUNT(DISTINCT CASE WHEN status = 'cancelled' THEN order_id END) AS cancelled_orders
    FROM {{ ref('orders_snapshot') }}
)

SELECT 
    new_orders,
    processing_orders,
    shipped_orders,
    delivered_orders,
    cancelled_orders,
    ROUND(100.0 * delivered_orders / NULLIF(new_orders, 0), 2) AS conversion_rate
FROM funnel