select t.transfer_id
from {{ ref('stg_transfers') }} as t
left join {{ ref('stg_fees') }} as f
    on t.transfer_id = f.transfer_id
left join {{ ref('stg_provider_costs') }} as pc
    on t.transfer_id = pc.transfer_id
left join {{ ref('stg_settlements') }} as s
    on t.transfer_id = s.transfer_id
where t.transfer_status = 'cancelled'
  and (f.transfer_id is not null or pc.transfer_id is not null or s.transfer_id is not null)
