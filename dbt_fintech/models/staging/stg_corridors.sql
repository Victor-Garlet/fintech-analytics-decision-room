select
    corridor_id,
    source_country,
    target_country,
    source_currency,
    target_currency,
    transfer_weight,
    variable_fee_bps,
    fixed_fee_usd,
    expected_instant_rate,
    corridor_cost_bps
from {{ source('raw', 'corridors') }}
