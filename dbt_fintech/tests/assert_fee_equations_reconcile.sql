select transfer_id
from {{ ref('stg_fees') }}
where abs(expected_fee_usd - (list_fee_usd - approved_price_investment_usd)) > 0.011
   or abs(fee_leakage_usd - greatest(expected_fee_usd - collected_fee_usd, 0)) > 0.011
