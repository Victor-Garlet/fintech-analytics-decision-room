select transfer_id
from {{ ref('stg_transfers') }}
where (transfer_status = 'completed' and (completed_at is null or delivery_seconds is null))
   or (transfer_status = 'cancelled' and (completed_at is not null or delivery_seconds is not null))
