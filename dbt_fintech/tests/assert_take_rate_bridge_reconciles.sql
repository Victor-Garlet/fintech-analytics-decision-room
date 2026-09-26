with totals as (
    select
        max(case when component_code = 'baseline' then impact_bps end) as baseline_bps,
        max(case when component_code = 'comparison' then impact_bps end) as comparison_bps,
        sum(case when not is_total then impact_bps else 0 end) as explained_change_bps
    from {{ ref('mart_take_rate_bridge') }}
)

select *
from totals
where abs(comparison_bps - baseline_bps - explained_change_bps) > 0.000001
