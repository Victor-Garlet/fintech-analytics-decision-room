with scoped_transfers as (
    select
        case when provider_id = 'P02' then 'priority_speed_route' else 'other_routes' end as route_group,
        *
    from {{ ref('int_transfer_unit_economics') }}
    where corridor_id = 'C01'
      and completion_month between date '2026-01-01' and date '2026-06-01'
)

select
    '2026-H1' as analysis_period,
    'C01' as corridor_id,
    route_group,
    case when route_group = 'priority_speed_route' then 'P02' else 'All providers except P02' end as provider_scope,
    count(*) as completed_transfers,
    sum(volume_usd) as volume_usd,
    1.0 * sum(case when is_instant then 1 else 0 end) / nullif(count(*), 0) as instant_transfer_rate,
    sum(provider_cost_usd) as provider_cost_usd,
    10000.0 * sum(provider_cost_usd) / nullif(sum(volume_usd), 0) as provider_cost_rate_bps,
    1.0 * sum(case when support_contact_count > 0 then 1 else 0 end) / nullif(count(*), 0)
        as support_contact_rate,
    sum(contribution_margin_proxy_usd) as contribution_margin_proxy_usd,
    10000.0 * sum(contribution_margin_proxy_usd) / nullif(sum(volume_usd), 0)
        as contribution_margin_proxy_bps
from scoped_transfers
group by route_group
