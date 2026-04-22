-- Проверка, что активные записи в снепшоте (dbt_valid_to IS NULL)
-- полностью совпадают с исходной таблицей

with source_data as (
    select
        order_id,
        status,
        updated_at
    from {{ ref('stg_orders_deduplicated') }}  
),

snapshot_active as (
    select
        order_id,
        status,
        updated_at
    from {{ ref('orders_snapshot') }}
    where dbt_valid_to is null
),

mismatches as (
    -- Записи, которые есть в источнике, но не в снепшоте (или dbt_valid_to не null)
    select 
        'missing_in_snapshot' as error_type,
        s.order_id,
        s.status as source_status,
        s.updated_at as source_updated_at,
        null as snapshot_status
    from source_data s
    left join snapshot_active snap 
        on s.order_id = snap.order_id
    where snap.order_id is null

    union all

    -- Записи, которые есть в снепшоте, но не в источнике
    select 
        'extra_in_snapshot' as error_type,
        snap.order_id,
        null as source_status,
        null as source_updated_at,
        snap.status as snapshot_status
    from snapshot_active snap
    left join source_data s 
        on snap.order_id = s.order_id
    where s.order_id is null

    union all

    -- Записи с несовпадающими данными (можно добавить сравнение по хэшу)
    select 
        'data_mismatch' as error_type,
        s.order_id,
        s.status,
        s.updated_at,
        snap.status
    from source_data s
    inner join snapshot_active snap 
        on s.order_id = snap.order_id
    where (
        s.status != snap.status 
        or s.updated_at != snap.updated_at
    )
)

select *
from mismatches
