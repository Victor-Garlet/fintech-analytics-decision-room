select
    provider_id,
    provider_name,
    base_cost_bps,
    base_settlement_hours
from {{ source('raw', 'providers') }}
