select scenario_name
from {{ ref('mart_routing_scenario') }}
where reroute_share <= 0
   or reroute_share >= 1
   or scenario_provider_cost_usd >= current_provider_cost_usd
   or scenario_instant_transfer_rate >= current_instant_transfer_rate
