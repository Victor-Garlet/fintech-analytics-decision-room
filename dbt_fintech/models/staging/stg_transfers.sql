select
    transfer_id,
    quote_id,
    customer_id,
    corridor_id,
    provider_id,
    cast(created_at as timestamp) as created_at,
    cast(completed_at as timestamp) as completed_at,
    transfer_status,
    payment_method,
    cast(is_instant as boolean) as is_instant,
    delivery_seconds,
    volume_usd,
    source_currency,
    target_currency
from {{ source('raw', 'transfers') }}
