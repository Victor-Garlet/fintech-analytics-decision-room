select t.transfer_id
from {{ ref('stg_transfers') }} as t
left join {{ ref('stg_settlements') }} as s
    on t.transfer_id = s.transfer_id
where t.transfer_status = 'completed'
  and s.transfer_id is null
