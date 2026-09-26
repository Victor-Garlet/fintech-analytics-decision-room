select analysis_period, corridor_id, route_group
from {{ ref('mart_speed_cost_tradeoff') }}
group by analysis_period, corridor_id, route_group
having count(*) > 1
