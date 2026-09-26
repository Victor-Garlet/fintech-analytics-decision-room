with support_by_transfer as (
    select
        transfer_id,
        count(*) as support_contact_count,
        sum(estimated_support_cost_usd) as estimated_support_cost_usd
    from {{ ref('stg_support_contacts') }}
    group by transfer_id
),

refunds_by_transfer as (
    select
        transfer_id,
        count(*) as refund_count,
        sum(refund_amount_usd) as refund_amount_usd
    from {{ ref('stg_refunds') }}
    group by transfer_id
)

select
    t.transfer_id,
    t.customer_id,
    c.customer_type,
    c.customer_segment,
    t.corridor_id,
    cr.source_country,
    cr.target_country,
    t.source_currency,
    t.target_currency,
    t.provider_id,
    p.provider_name,
    t.created_at,
    t.completed_at,
    cast({{ dbt.date_trunc('month', 't.completed_at') }} as date) as completion_month,
    t.payment_method,
    t.is_instant,
    t.delivery_seconds,
    t.volume_usd,
    f.list_fee_usd,
    f.approved_price_investment_usd,
    f.expected_fee_usd,
    f.collected_fee_usd,
    f.fee_leakage_usd,
    f.fee_outcome,
    pc.provider_cost_bps,
    pc.provider_fixed_cost_usd,
    pc.provider_cost_usd,
    pc.routing_tier,
    coalesce(s.support_contact_count, 0) as support_contact_count,
    coalesce(s.estimated_support_cost_usd, 0) as estimated_support_cost_usd,
    coalesce(r.refund_count, 0) as refund_count,
    coalesce(r.refund_amount_usd, 0) as refund_amount_usd,
    f.collected_fee_usd
        - pc.provider_cost_usd
        - coalesce(s.estimated_support_cost_usd, 0) as contribution_margin_proxy_usd
from {{ ref('stg_transfers') }} as t
inner join {{ ref('stg_customers') }} as c
    on t.customer_id = c.customer_id
inner join {{ ref('stg_corridors') }} as cr
    on t.corridor_id = cr.corridor_id
inner join {{ ref('stg_providers') }} as p
    on t.provider_id = p.provider_id
inner join {{ ref('stg_fees') }} as f
    on t.transfer_id = f.transfer_id
inner join {{ ref('stg_provider_costs') }} as pc
    on t.transfer_id = pc.transfer_id
left join support_by_transfer as s
    on t.transfer_id = s.transfer_id
left join refunds_by_transfer as r
    on t.transfer_id = r.transfer_id
where t.transfer_status = 'completed'
