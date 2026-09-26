select
    provider_cost_id,
    transfer_id,
    provider_id,
    provider_cost_bps,
    provider_fixed_cost_usd,
    provider_cost_usd,
    routing_tier
from {{ source('raw', 'provider_costs') }}
