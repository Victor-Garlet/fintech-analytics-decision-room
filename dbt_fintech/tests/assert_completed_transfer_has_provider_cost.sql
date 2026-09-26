select t.transfer_id
from {{ ref('stg_transfers') }} as t
left join {{ ref('stg_provider_costs') }} as pc
    on t.transfer_id = pc.transfer_id
where t.transfer_status = 'completed'
  and pc.transfer_id is null
