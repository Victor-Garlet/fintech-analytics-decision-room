select
    quote_id,
    customer_id,
    corridor_id,
    pricing_rule_id,
    cast(quoted_at as timestamp) as quoted_at,
    cast(quote_expires_at as timestamp) as quote_expires_at,
    volume_usd,
    source_amount,
    target_amount_before_fee,
    synthetic_fx_rate,
    list_fee_usd,
    expected_fee_usd
from {{ source('raw', 'quotes') }}
