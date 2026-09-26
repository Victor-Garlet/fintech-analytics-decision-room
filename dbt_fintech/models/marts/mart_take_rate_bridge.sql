with period_totals as (
    select
        case
            when completion_month between date '2025-07-01' and date '2025-12-01' then 'baseline'
            when completion_month between date '2026-01-01' and date '2026-06-01' then 'comparison'
        end as period,
        sum(volume_usd) as volume_usd,
        sum(list_fee_usd) as list_fee_usd,
        sum(approved_price_investment_usd) as approved_price_investment_usd,
        sum(fee_leakage_usd) as fee_leakage_usd,
        sum(collected_fee_usd) as collected_fee_usd
    from {{ ref('int_transfer_unit_economics') }}
    where completion_month between date '2025-07-01' and date '2026-06-01'
    group by 1
),

cell_totals as (
    select
        corridor_id,
        customer_segment,
        sum(case when completion_month between date '2025-07-01' and date '2025-12-01' then volume_usd else 0 end)
            as baseline_volume_usd,
        sum(case when completion_month between date '2025-07-01' and date '2025-12-01' then list_fee_usd else 0 end)
            as baseline_list_fee_usd,
        sum(case when completion_month between date '2026-01-01' and date '2026-06-01' then volume_usd else 0 end)
            as comparison_volume_usd,
        sum(case when completion_month between date '2026-01-01' and date '2026-06-01' then list_fee_usd else 0 end)
            as comparison_list_fee_usd
    from {{ ref('int_transfer_unit_economics') }}
    where completion_month between date '2025-07-01' and date '2026-06-01'
    group by corridor_id, customer_segment
),

cell_metrics as (
    select
        c.*,
        c.baseline_volume_usd / nullif(b.volume_usd, 0) as baseline_volume_share,
        c.comparison_volume_usd / nullif(p.volume_usd, 0) as comparison_volume_share,
        10000.0 * c.baseline_list_fee_usd / nullif(c.baseline_volume_usd, 0) as baseline_list_rate_bps,
        10000.0 * c.comparison_list_fee_usd / nullif(c.comparison_volume_usd, 0) as comparison_list_rate_bps
    from cell_totals as c
    cross join period_totals as b
    cross join period_totals as p
    where b.period = 'baseline'
      and p.period = 'comparison'
),

list_rate_decomposition as (
    select
        sum(
            (comparison_volume_share - baseline_volume_share)
            * (
                coalesce(baseline_list_rate_bps, comparison_list_rate_bps)
                + coalesce(comparison_list_rate_bps, baseline_list_rate_bps)
            ) / 2.0
        ) as portfolio_mix_effect_bps,
        sum(
            (coalesce(comparison_list_rate_bps, baseline_list_rate_bps)
                - coalesce(baseline_list_rate_bps, comparison_list_rate_bps))
            * (baseline_volume_share + comparison_volume_share) / 2.0
        ) as within_cell_yield_effect_bps
    from cell_metrics
),

bridge_inputs as (
    select
        b.volume_usd as baseline_volume_usd,
        p.volume_usd as comparison_volume_usd,
        10000.0 * b.collected_fee_usd / nullif(b.volume_usd, 0) as baseline_collected_take_rate_bps,
        d.portfolio_mix_effect_bps,
        d.within_cell_yield_effect_bps,
        -10000.0 * p.approved_price_investment_usd / nullif(p.volume_usd, 0)
            as approved_price_investment_effect_bps,
        -10000.0 * p.fee_leakage_usd / nullif(p.volume_usd, 0) as fee_leakage_effect_bps,
        10000.0 * p.collected_fee_usd / nullif(p.volume_usd, 0) as comparison_collected_take_rate_bps
    from period_totals as b
    cross join period_totals as p
    cross join list_rate_decomposition as d
    where b.period = 'baseline'
      and p.period = 'comparison'
),

components as (
    select 0 as component_order, 'baseline' as component_code, 'Baseline collected take rate' as component_label,
        baseline_collected_take_rate_bps as impact_bps, true as is_total
    from bridge_inputs
    union all
    select 1, 'portfolio_mix', 'Portfolio mix', portfolio_mix_effect_bps, false from bridge_inputs
    union all
    select 2, 'within_cell_yield', 'Within-cell list yield', within_cell_yield_effect_bps, false from bridge_inputs
    union all
    select 3, 'approved_price_investment', 'Approved price investment', approved_price_investment_effect_bps, false
    from bridge_inputs
    union all
    select 4, 'fee_leakage', 'Pricing configuration leakage', fee_leakage_effect_bps, false from bridge_inputs
    union all
    select 5, 'comparison', 'Comparison collected take rate', comparison_collected_take_rate_bps, true
    from bridge_inputs
),

final as (
    select
        c.component_order,
        c.component_code,
        c.component_label,
        c.impact_bps,
        case
            when c.component_code = 'comparison' then i.comparison_collected_take_rate_bps
            else sum(c.impact_bps) over (order by c.component_order rows unbounded preceding)
        end as running_take_rate_bps,
        c.is_total,
        date '2025-07-01' as baseline_period_start,
        date '2025-12-31' as baseline_period_end,
        date '2026-01-01' as comparison_period_start,
        date '2026-06-30' as comparison_period_end,
        i.baseline_volume_usd,
        i.comparison_volume_usd
    from components as c
    cross join bridge_inputs as i
)

select *
from final
order by component_order
