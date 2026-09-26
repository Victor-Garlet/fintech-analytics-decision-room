select transfer_id
from {{ ref('int_transfer_unit_economics') }}
where volume_usd < 0
   or list_fee_usd < 0
   or approved_price_investment_usd < 0
   or expected_fee_usd < 0
   or collected_fee_usd < 0
   or fee_leakage_usd < 0
   or provider_cost_usd < 0
   or estimated_support_cost_usd < 0
