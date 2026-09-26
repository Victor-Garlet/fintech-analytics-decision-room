select t.transfer_id
from {{ ref('stg_transfers') }} as t
left join {{ ref('stg_fees') }} as f
    on t.transfer_id = f.transfer_id
where t.transfer_status = 'completed'
  and f.transfer_id is null
