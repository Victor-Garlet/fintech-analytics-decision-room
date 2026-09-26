select transfer_id
from {{ ref('int_reconciliation_bridge') }}
where (settlement_status = 'matched' and is_reconciliation_exception)
   or (settlement_status <> 'matched' and not is_reconciliation_exception)
   or (settlement_status = 'missing' and (settled_at is not null or actual_settlement_usd is not null))
