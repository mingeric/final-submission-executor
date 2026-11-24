# 2. Task ledger and blocker resolution

## Ledger schema

`templates/TASK_LEDGER.tsv` has these columns:

| Column | Meaning |
|---|---|
| `task_id` | Stable identifier, e.g. `F03`, `SUPP-SYNC`. |
| `status` | `PENDING`, `DONE`, `VERIFIED`, or `BLOCKED`. |
| `deliverable` | Exact file path or concrete outcome. |
| `evidence` | Path to the file that proves the outcome. |
| `note` | For `BLOCKED`, the exact missing input or authorization. |

Rules:

- One row per independently verifiable task; do not fold five figures into one row.
- `VERIFIED` requires both a deliverable and an evidence path that exists.
- `BLOCKED` requires a specific, checkable reason, never "complex" or "not possible".
- Update the ledger after each validated commit so an interrupted run can resume from the last verified state.

## Resumable execution

- Check the target path, its SHA256 and the ledger before recomputing.
- If a valid file already exists, mark it `VERIFIED` with its evidence and move on.
- If a staged output exists, evaluate it first; reuse valid calculations, repair only the plotting or packaging code.
- Do not restart an entire project because one module failed.

## Common blockers and the expected response

| Blocker | Response |
|---|---|
| Missing preferred font | Inspect installed fonts in the actual plotting environment, choose an available publication-quality sans-serif, rebuild cache if needed, render a real test image, eliminate warnings. |
| Missing referenced asset directory | Treat as a locator problem; find the authoritative files through the registry. Do not create a permanent duplicate review package. |
| Figure-role conflict | Resolve by scientific content and the newest explicit ownership rule; update manuscript, legend and registry in one transaction. |
| Poor readability at print size | Rewrite plotting code: larger typography, fewer low-value annotations, asymmetric layouts, move secondary analysis to supplements. Render, inspect, repeat. |
| Stale staging outputs | Recover, evaluate and either promote after validation or discard after recording why. |
| Concurrent writer | Never overwrite a file another live process is writing. Finish independent work, then verify or take over after the writer stops. |
| Missing source data | Search the whole named project tree once, including sibling directories, before declaring absence. If genuinely absent, block only the dependent panel. |

## Parallel work

Independent tasks may run in parallel only when their write scopes do not overlap. Otherwise serialize. The main thread owns authoritative paths, registry commits and the final answer.
