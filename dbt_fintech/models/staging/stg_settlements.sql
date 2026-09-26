select
    settlement_id,
    transfer_id,
    provider_id,
    cast(expected_settlement_at as timestamp) as expected_settlement_at,
    cast(settled_at as timestamp) as settled_at,
    expected_settlement_usd,
    actual_settlement_usd,
    settlement_variance_usd,
    settlement_status,
    cast(is_reconciliation_exception as boolean) as is_reconciliation_exception
from {{ source('raw', 'settlements') }}
