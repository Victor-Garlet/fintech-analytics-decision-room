select
    pricing_rule_id,
    corridor_id,
    customer_segment,
    variable_fee_bps,
    fixed_fee_usd,
    cast(effective_start as date) as effective_start,
    cast(effective_end as date) as effective_end
from {{ source('raw', 'pricing_rules') }}
