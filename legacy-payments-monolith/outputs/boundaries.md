# Boundary analysis: fintechco_core

- 12 modules, 249 LOC, 42 import edges
- Edges that would become network/API calls: **18** (internal to a service: 6)
- Circular dependencies: **1** -> [['fraud', 'payments']]
- Tables touched by more than one service: **3**

## Hotspots (fan-in / fan-out)

| module | fan-in | fan-out | proposed service |
|---|---|---|---|
| payments | 4 | 7 | payments-core |
| accounts | 6 | 3 | identity |
| db | 7 | 1 | platform-lib |
| batch_jobs | 0 | 7 | reporting-bi |
| config | 7 | 0 | platform-lib |
| ledger | 4 | 3 | ledger-core |
| reporting | 2 | 5 | reporting-bi |
| utils | 6 | 1 | platform-lib |
| fraud | 1 | 5 | payments-core |
| auth | 2 | 3 | identity |
| mobile_api | 0 | 5 | mobile-bff |
| notifications | 3 | 2 | notifications |

## Cross-service calls to turn into APIs / events

- batch_jobs (reporting-bi) -> payments (payments-core)
- batch_jobs (reporting-bi) -> ledger (ledger-core)
- batch_jobs (reporting-bi) -> accounts (identity)
- batch_jobs (reporting-bi) -> notifications (notifications)
- payments (payments-core) -> ledger (ledger-core)
- payments (payments-core) -> accounts (identity)
- payments (payments-core) -> notifications (notifications)
- ledger (ledger-core) -> accounts (identity)
- reporting (reporting-bi) -> payments (payments-core)
- reporting (reporting-bi) -> ledger (ledger-core)
- reporting (reporting-bi) -> accounts (identity)
- notifications (notifications) -> accounts (identity)
- fraud (payments-core) -> ledger (ledger-core)
- mobile_api (mobile-bff) -> payments (payments-core)
- mobile_api (mobile-bff) -> notifications (notifications)
- mobile_api (mobile-bff) -> accounts (identity)
- mobile_api (mobile-bff) -> auth (identity)
- mobile_api (mobile-bff) -> reporting (reporting-bi)

## Shared tables (need a single owner)

- `accounts`: accounts, batch_jobs
- `ledger`: ledger, reporting
- `payments`: payments, reporting

## Independent check: modularity communities (platform libs removed)

- batch_jobs, fraud, ledger, payments, reporting
- accounts, auth, mobile_api, notifications
