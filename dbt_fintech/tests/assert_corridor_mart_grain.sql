select completion_month, corridor_id
from {{ ref('mart_corridor_performance') }}
group by completion_month, corridor_id
having count(*) > 1
