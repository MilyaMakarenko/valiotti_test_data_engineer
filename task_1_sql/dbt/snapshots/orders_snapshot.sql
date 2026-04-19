{% snapshot orders_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='order_id',
        strategy='check',
        check_cols=['updated_at'],
        invalidate_hard_deletes=True,
        description='SCD Type 2 history of order status changes based on updated_at column'
        
    )
}}

    SELECT
        a.order_id,
        a.status,
        a.updated_at
    FROM {{ ref('stg_orders_deduplicated') }} a


{% endsnapshot %}