select
    fee_id,
    transfer_id,
    list_fee_usd,
    approved_price_investment_usd,
    expected_fee_usd,
    collected_fee_usd,
    fee_leakage_usd,
    fee_outcome
from {{ source('raw', 'fees') }}
