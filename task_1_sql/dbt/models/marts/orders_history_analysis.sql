SELECT 
    status,
    COUNT(*) AS times_in_status,
    MIN(dbt_valid_from) AS first_time,
    MAX(dbt_valid_to) AS last_time
FROM {{ ref('orders_snapshot') }}
GROUP BY  status
ORDER BY  status