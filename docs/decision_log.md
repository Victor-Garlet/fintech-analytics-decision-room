# Decision Log

This log records choices that materially affect how the project is interpreted or reproduced.

| Date | Decision | Reason | Revisit trigger |
| --- | --- | --- | --- |
| 2026-09-24 | Use Wise as public context, never as a claimed client or employer. | It creates a credible European fintech decision context while preserving the integrity boundary. | A different reference company becomes materially better suited to the case. |
| 2026-09-24 | Start with a deterministic 10,000-transfer prototype before scaling. | Grains, equations and scenario detectability are cheaper to correct at small scale. | The metric layer and tests reconcile end to end. |
| 2026-09-24 | Use DuckDB locally and BigQuery only for the scale milestone. | The local review path stays free and reproducible without weakening the target architecture. | A BigQuery environment is configured and the 1M-row generator is ready. |
| 2026-09-24 | Keep exact seeded-scenario configuration outside version control during the investigation. | Readers can follow the evidence without being handed the answer in advance. | The related finding has been published or the final repository is released. |
| 2026-09-24 | Make completion time and settlement time explicit, not forced into one monthly total. | Finance and Operations use different valid business events. | Stakeholders agree on a replacement reporting contract. |
| 2026-09-24 | Use one completed-transfer economic spine before aggregation. | It prevents mixed grains from creating plausible but incorrect unit-economics metrics. | A new source requires a different primary analytical grain. |
| 2026-09-24 | Delay public deployment and LinkedIn publication until individual review. | Code, narrative, visual and disclosure must be approved as one release unit. | Victor approves the relevant release. |
