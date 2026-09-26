select
    completion_month,
    corridor_id,
    source_country,
    target_country,
    source_currency,
    target_currency,
    count(*) as completed_transfers,
    count(distinct customer_id) as active_customers,
    sum(volume_usd) as volume_usd,
    sum(collected_fee_usd) as collected_fee_revenue_usd,
    sum(fee_leakage_usd) as fee_leakage_usd,
    10000.0 * sum(collected_fee_usd) / nullif(sum(volume_usd), 0) as collected_take_rate_bps,
    10000.0 * sum(fee_leakage_usd) / nullif(sum(volume_usd), 0) as fee_leakage_bps,
    1.0 * sum(case when is_instant then 1 else 0 end) / nullif(count(*), 0) as instant_transfer_rate,
    10000.0 * sum(provider_cost_usd) / nullif(sum(volume_usd), 0) as provider_cost_rate_bps,
    1.0 * sum(case when support_contact_count > 0 then 1 else 0 end) / nullif(count(*), 0)
        as support_contact_rate,
    sum(contribution_margin_proxy_usd) as contribution_margin_proxy_usd
from {{ ref('int_transfer_unit_economics') }}
group by
    completion_month,
    corridor_id,
    source_country,
    target_country,
    source_currency,
    target_currency
