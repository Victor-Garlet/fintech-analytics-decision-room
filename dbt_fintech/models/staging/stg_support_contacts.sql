select
    support_contact_id,
    transfer_id,
    cast(contacted_at as timestamp) as contacted_at,
    contact_reason,
    resolution_hours,
    estimated_support_cost_usd
from {{ source('raw', 'support_contacts') }}
