with expected as (
    select
        completion_month,
        count(*) as completed_transfers,
        sum(volume_usd) as cross_border_volume_usd,
        sum(collected_fee_usd) as collected_fee_revenue_usd
    from {{ ref('mart_transfer_unit_economics') }}
    group by completion_month
)

select e.completion_month
from expected as e
inner join {{ ref('mart_executive_kpis') }} as k
    on e.completion_month = k.completion_month
where e.completed_transfers <> k.completed_transfers
   or abs(e.cross_border_volume_usd - k.cross_border_volume_usd) > 0.01
   or abs(e.collected_fee_revenue_usd - k.collected_fee_revenue_usd) > 0.01
