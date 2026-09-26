with reporting_months as (
    select distinct completion_month as reporting_month
    from {{ ref('int_reconciliation_bridge') }}
    where completion_month is not null

    union

    select distinct settlement_month as reporting_month
    from {{ ref('int_reconciliation_bridge') }}
    where settlement_month is not null
),

operations_view as (
    select
        completion_month as reporting_month,
        count(*) as operations_completed_transfers,
        sum(expected_settlement_usd) as operations_expected_settlement_usd,
        sum(case when settlement_month = completion_month then 1 else 0 end) as same_month_settled_transfers,
        sum(case when settlement_month = completion_month then actual_settlement_usd else 0 end)
            as same_month_actual_settlement_usd,
        sum(
            case
                when settlement_month = completion_month then actual_settlement_usd - expected_settlement_usd
                else 0
            end
        ) as same_month_settlement_variance_usd,
        sum(case when settlement_month is null or settlement_month <> completion_month then 1 else 0 end)
            as carry_out_transfers,
        sum(
            case
                when settlement_month is null or settlement_month <> completion_month then expected_settlement_usd
                else 0
            end
        ) as carry_out_expected_settlement_usd
    from {{ ref('int_reconciliation_bridge') }}
    group by completion_month
),

finance_view as (
    select
        settlement_month as reporting_month,
        count(*) as finance_settled_transfers,
        sum(actual_settlement_usd) as finance_actual_settlement_usd,
        sum(case when completion_month <> settlement_month then 1 else 0 end) as carry_in_transfers,
        sum(case when completion_month <> settlement_month then actual_settlement_usd else 0 end)
            as carry_in_actual_settlement_usd
    from {{ ref('int_reconciliation_bridge') }}
    where settlement_month is not null
    group by settlement_month
),

combined as (
    select
        m.reporting_month,
        coalesce(o.operations_completed_transfers, 0) as operations_completed_transfers,
        coalesce(o.operations_expected_settlement_usd, 0) as operations_expected_settlement_usd,
        coalesce(o.same_month_settled_transfers, 0) as same_month_settled_transfers,
        coalesce(o.same_month_actual_settlement_usd, 0) as same_month_actual_settlement_usd,
        coalesce(o.same_month_settlement_variance_usd, 0) as same_month_settlement_variance_usd,
        coalesce(o.carry_out_transfers, 0) as carry_out_transfers,
        coalesce(o.carry_out_expected_settlement_usd, 0) as carry_out_expected_settlement_usd,
        coalesce(f.carry_in_transfers, 0) as carry_in_transfers,
        coalesce(f.carry_in_actual_settlement_usd, 0) as carry_in_actual_settlement_usd,
        coalesce(f.finance_settled_transfers, 0) as finance_settled_transfers,
        coalesce(f.finance_actual_settlement_usd, 0) as finance_actual_settlement_usd
    from reporting_months as m
    left join operations_view as o
        on m.reporting_month = o.reporting_month
    left join finance_view as f
        on m.reporting_month = f.reporting_month
)

select
    *,
    operations_expected_settlement_usd
        - carry_out_expected_settlement_usd
        + carry_in_actual_settlement_usd
        + same_month_settlement_variance_usd as reconciled_finance_actual_settlement_usd,
    operations_expected_settlement_usd
        - carry_out_expected_settlement_usd
        + carry_in_actual_settlement_usd
        + same_month_settlement_variance_usd
        - finance_actual_settlement_usd as bridge_residual_usd
from combined
order by reporting_month
