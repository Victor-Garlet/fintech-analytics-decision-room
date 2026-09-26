with parameters as (
    select 0.25 as reroute_share
),

selected_route as (
    select *
    from {{ ref('mart_speed_cost_tradeoff') }}
    where route_group = 'priority_speed_route'
),

benchmark_route as (
    select *
    from {{ ref('mart_speed_cost_tradeoff') }}
    where route_group = 'other_routes'
),

scenario_inputs as (
    select
        p.reroute_share,
        s.completed_transfers as selected_route_transfers,
        s.volume_usd as selected_route_volume_usd,
        s.instant_transfer_rate as selected_route_instant_rate,
        s.provider_cost_rate_bps as selected_route_cost_bps,
        s.support_contact_rate as selected_route_support_rate,
        s.contribution_margin_proxy_bps as selected_route_contribution_bps,
        b.completed_transfers as benchmark_route_transfers,
        b.volume_usd as benchmark_route_volume_usd,
        b.instant_transfer_rate as benchmark_route_instant_rate,
        b.provider_cost_rate_bps as benchmark_route_cost_bps,
        b.support_contact_rate as benchmark_route_support_rate,
        b.contribution_margin_proxy_bps as benchmark_route_contribution_bps,
        s.provider_cost_usd + b.provider_cost_usd as current_provider_cost_usd,
        s.contribution_margin_proxy_usd + b.contribution_margin_proxy_usd as current_contribution_margin_proxy_usd
    from parameters as p
    cross join selected_route as s
    cross join benchmark_route as b
)

select
    'C01 controlled routing test' as scenario_name,
    'hypothesis for controlled experiment' as scenario_status,
    reroute_share,
    selected_route_transfers as eligible_transfers,
    selected_route_volume_usd as eligible_volume_usd,
    reroute_share * selected_route_transfers as estimated_rerouted_transfers,
    reroute_share * selected_route_volume_usd as estimated_rerouted_volume_usd,
    current_provider_cost_usd,
    current_provider_cost_usd
        - reroute_share * selected_route_volume_usd
            * (selected_route_cost_bps - benchmark_route_cost_bps) / 10000.0 as scenario_provider_cost_usd,
    reroute_share * selected_route_volume_usd
        * (selected_route_cost_bps - benchmark_route_cost_bps) / 10000.0 as estimated_provider_cost_savings_usd,
    (
        selected_route_transfers * selected_route_instant_rate
        + benchmark_route_transfers * benchmark_route_instant_rate
    ) / nullif(selected_route_transfers + benchmark_route_transfers, 0) as current_instant_transfer_rate,
    (
        selected_route_transfers * selected_route_instant_rate
        + benchmark_route_transfers * benchmark_route_instant_rate
        - reroute_share * selected_route_transfers
            * (selected_route_instant_rate - benchmark_route_instant_rate)
    ) / nullif(selected_route_transfers + benchmark_route_transfers, 0) as scenario_instant_transfer_rate,
    -100.0 * reroute_share * selected_route_transfers
        * (selected_route_instant_rate - benchmark_route_instant_rate)
        / nullif(selected_route_transfers + benchmark_route_transfers, 0) as instant_rate_change_percentage_points,
    (
        selected_route_transfers * selected_route_support_rate
        + benchmark_route_transfers * benchmark_route_support_rate
    ) / nullif(selected_route_transfers + benchmark_route_transfers, 0) as current_support_contact_rate,
    (
        selected_route_transfers * selected_route_support_rate
        + benchmark_route_transfers * benchmark_route_support_rate
        + reroute_share * selected_route_transfers
            * (benchmark_route_support_rate - selected_route_support_rate)
    ) / nullif(selected_route_transfers + benchmark_route_transfers, 0) as scenario_support_contact_rate,
    100.0 * reroute_share * selected_route_transfers
        * (benchmark_route_support_rate - selected_route_support_rate)
        / nullif(selected_route_transfers + benchmark_route_transfers, 0) as support_rate_change_percentage_points,
    current_contribution_margin_proxy_usd,
    current_contribution_margin_proxy_usd
        + reroute_share * selected_route_volume_usd
            * (benchmark_route_contribution_bps - selected_route_contribution_bps) / 10000.0
        as scenario_contribution_margin_proxy_usd,
    reroute_share * selected_route_volume_usd
        * (benchmark_route_contribution_bps - selected_route_contribution_bps) / 10000.0
        as estimated_contribution_margin_uplift_usd
from scenario_inputs
