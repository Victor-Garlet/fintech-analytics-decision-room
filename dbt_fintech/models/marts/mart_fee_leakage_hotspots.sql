select
    date '2026-01-01' as analysis_period_start,
    date '2026-06-30' as analysis_period_end,
    corridor_id,
    customer_segment,
    count(*) as completed_transfers,
    sum(case when fee_leakage_usd > 0 then 1 else 0 end) as affected_transfers,
    sum(volume_usd) as volume_usd,
    sum(expected_fee_usd) as expected_fee_usd,
    sum(fee_leakage_usd) as fee_leakage_usd,
    10000.0 * sum(fee_leakage_usd) / nullif(sum(volume_usd), 0) as fee_leakage_bps,
    sum(fee_leakage_usd) / nullif(sum(expected_fee_usd), 0) as expected_fee_leakage_rate
from {{ ref('int_transfer_unit_economics') }}
where completion_month between date '2026-01-01' and date '2026-06-01'
group by corridor_id, customer_segment
having sum(fee_leakage_usd) > 0
order by fee_leakage_usd desc
