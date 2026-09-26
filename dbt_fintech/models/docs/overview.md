{% docs __overview__ %}

# Fintech Analytics Decision Room

This dbt project transforms a deterministic synthetic payments dataset into tested models for reconciliation, pricing, provider performance and unit economics.

The project is inspired by public fintech disclosures. It does not contain real customer data or reproduce Wise's internal systems.

## Model layers

- **Staging:** typed, named and documented source records.
- **Intermediate:** transfer-level financial and reconciliation logic.
- **Marts:** decision-facing monthly, corridor, provider and exception views.

Every public result should be traceable from a mart through the intermediate and staging layers to a synthetic source record.

{% enddocs %}
