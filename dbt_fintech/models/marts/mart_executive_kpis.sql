select
    u.completion_month,
    count(*) as completed_transfers,
    count(distinct u.customer_id) as active_customers,
    sum(u.volume_usd) as cross_border_volume_usd,
    sum(u.list_fee_usd) as list_fee_revenue_usd,
    sum(u.approved_price_investment_usd) as approved_price_investment_usd,
    sum(u.expected_fee_usd) as expected_fee_revenue_usd,
    sum(u.collected_fee_usd) as collected_fee_revenue_usd,
    sum(u.fee_leakage_usd) as fee_leakage_usd,
    10000.0 * sum(u.list_fee_usd) / nullif(sum(u.volume_usd), 0) as list_take_rate_bps,
    10000.0 * sum(u.expected_fee_usd) / nullif(sum(u.volume_usd), 0) as expected_take_rate_bps,
    10000.0 * sum(u.collected_fee_usd) / nullif(sum(u.volume_usd), 0) as collected_take_rate_bps,
    1.0 * sum(case when u.is_instant then 1 else 0 end) / nullif(count(*), 0) as instant_transfer_rate,
    sum(u.provider_cost_usd) as provider_cost_usd,
    10000.0 * sum(u.provider_cost_usd) / nullif(sum(u.volume_usd), 0) as provider_cost_rate_bps,
    1.0 * sum(case when u.support_contact_count > 0 then 1 else 0 end) / nullif(count(*), 0) as support_contact_rate,
    sum(u.contribution_margin_proxy_usd) as contribution_margin_proxy_usd,
    sum(case when r.is_reconciliation_exception then 1 else 0 end) as reconciliation_exceptions,
    1.0 * sum(case when r.is_reconciliation_exception then 1 else 0 end) / nullif(count(*), 0)
        as reconciliation_exception_rate,
    sum(case when r.reporting_period_alignment = 'cross-month' then 1 else 0 end)
        as cross_month_settlements
from {{ ref('int_transfer_unit_economics') }} as u
inner join {{ ref('int_reconciliation_bridge') }} as r
    on u.transfer_id = r.transfer_id
group by u.completion_month
