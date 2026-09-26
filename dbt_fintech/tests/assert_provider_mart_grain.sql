select completion_month, provider_id, routing_tier
from {{ ref('mart_provider_performance') }}
group by completion_month, provider_id, routing_tier
having count(*) > 1
