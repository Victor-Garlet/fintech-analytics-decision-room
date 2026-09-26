select
    transfer_id,
    customer_id,
    corridor_id,
    provider_id,
    completed_at,
    completion_month,
    expected_settlement_at,
    settled_at,
    settlement_month,
    expected_settlement_usd,
    actual_settlement_usd,
    settlement_variance_usd,
    absolute_settlement_variance_usd,
    settlement_status,
    reporting_period_alignment
from {{ ref('int_reconciliation_bridge') }}
where is_reconciliation_exception
