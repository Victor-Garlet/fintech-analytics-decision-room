select reporting_month
from {{ ref('mart_reporting_period_reconciliation') }}
where abs(bridge_residual_usd) > 0.01
