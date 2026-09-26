select
    customer_id,
    customer_type,
    customer_segment,
    home_country,
    cast(signup_date as date) as signup_date,
    risk_tier
from {{ source('raw', 'customers') }}
