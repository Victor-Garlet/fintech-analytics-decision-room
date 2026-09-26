select
    t.transfer_id,
    t.customer_id,
    t.corridor_id,
    t.provider_id,
    t.completed_at,
    cast({{ dbt.date_trunc('month', 't.completed_at') }} as date) as completion_month,
    s.expected_settlement_at,
    s.settled_at,
    cast({{ dbt.date_trunc('month', 's.settled_at') }} as date) as settlement_month,
    s.expected_settlement_usd,
    s.actual_settlement_usd,
    s.settlement_variance_usd,
    abs(s.settlement_variance_usd) as absolute_settlement_variance_usd,
    s.settlement_status,
    s.is_reconciliation_exception,
    case
        when s.settled_at is null then 'missing settlement'
        when cast({{ dbt.date_trunc('month', 't.completed_at') }} as date)
            <> cast({{ dbt.date_trunc('month', 's.settled_at') }} as date)
            then 'cross-month'
        else 'same-month'
    end as reporting_period_alignment
from {{ ref('stg_transfers') }} as t
inner join {{ ref('stg_settlements') }} as s
    on t.transfer_id = s.transfer_id
where t.transfer_status = 'completed'
