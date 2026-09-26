select
    refund_id,
    transfer_id,
    cast(refunded_at as timestamp) as refunded_at,
    refund_reason,
    refund_amount_usd
from {{ source('raw', 'refunds') }}
