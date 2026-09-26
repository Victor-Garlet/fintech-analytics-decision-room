select analysis_period_start, analysis_period_end, corridor_id, customer_segment
from {{ ref('mart_fee_leakage_hotspots') }}
group by analysis_period_start, analysis_period_end, corridor_id, customer_segment
having count(*) > 1
