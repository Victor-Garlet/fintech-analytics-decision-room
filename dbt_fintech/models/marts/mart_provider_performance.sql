select
    completion_month,
    provider_id,
    provider_name,
    routing_tier,
    count(*) as completed_transfers,
    sum(volume_usd) as volume_usd,
    1.0 * sum(case when is_instant then 1 else 0 end) / nullif(count(*), 0) as instant_transfer_rate,
    sum(provider_cost_usd) as provider_cost_usd,
    10000.0 * sum(provider_cost_usd) / nullif(sum(volume_usd), 0) as provider_cost_rate_bps,
    1.0 * sum(case when support_contact_count > 0 then 1 else 0 end) / nullif(count(*), 0)
        as support_contact_rate,
    sum(contribution_margin_proxy_usd) as contribution_margin_proxy_usd
from {{ ref('int_transfer_unit_economics') }}
group by completion_month, provider_id, provider_name, routing_tier
