---
name: final-submission-executor
description: Drive a research or figure-production project from an execution spec to a physically committed final submission. Use when the user asks to finish a final submission, complete every task effectively, overwrite canonical deliverables, resolve blockers instead of reporting them, or enforce a maximum-quality autonomous execution standard. Includes task-ledger discipline, scientific and visual QA gates, canonical atomic overwrite, registry synchronization and an honest final acceptance report.
---

# Final Submission Executor

This skill turns a "final execution" specification into real, verified artifacts on disk. It is for the last mile: the stage where inventories, plans and audits are no longer enough and the canonical deliverable must actually change.

Core stance: **completion is the default**. A blocker is a problem to investigate, not a reason to stop. Ask the user only for genuinely missing authorization or a decision that cannot be inferred from the specification.

## When to use

- "Finish the final submission", "complete all tasks effectively", "overwrite the canonical files".
- A spec contains words such as FINAL EXECUTION OVERRIDE, SOLVE ALL BLOCKERS, REWRITE, REPRINT, OVERWRITE.
- A project has authoritative output paths that must be updated in place, with registry/manifest synchronization.
- A figure, report or dataset package repeatedly fails readiness checks and needs a closed-loop repair.

Do not use for exploratory analysis, open-ended research questions, or a first draft with no agreed deliverable contract.

## Non-negotiable rules

1. **One canonical truth.** Resolve symlinks and authoritative paths once. Never create `FINAL_V2`, `NEW_FINAL` or a parallel release root.
2. **Real work, not status theatre.** Scripts, review sheets, contact sheets and audit reports are intermediate operations, never the deliverable.
3. **Recover before recomputing.** Reuse validated results and existing staged outputs. Re-run only what is missing or scientifically invalid.
4. **No fabrication.** No synthetic data presented as observation, no invented significance, no simulated coordinates, no fictitious replication. Preserve genuine negative results.
5. **Atomic, one-by-one commits.** Validate a replacement (science + visual + metadata) before swapping it into the canonical path. Keep a recoverable superseded copy.
6. **Synchronize the transaction.** On each committed replacement, update legend/manuscript/source map/manifest/registry/hash in the same pass.
7. **Honest completion.** Report actual counts, exact paths, old/new SHA256, real limitations and unresolved blockers. Never claim a file was written, verified or deleted unless it was.

## Workflow

1. **Read the contract.** Extract: authoritative paths, allowed write scope, deliverable count, output format, acceptance criteria, and any explicit override of earlier instructions.
2. **Build a task ledger.** Use `templates/TASK_LEDGER.tsv`. One row per independently verifiable task: `task_id`, `status`, `deliverable`, `evidence`, `note`. Status is `PENDING`, `DONE`, `VERIFIED` or `BLOCKED`. Update it as work lands; use it to resume.
3. **Resolve blockers in priority order.** Font, path, ownership, readability, stale staging. For each: identify root cause, inspect the real environment, implement a fix, test it, continue. See `references/02`.
4. **Execute scientific work from traceable sources.** Compare competing methods; prevent leakage and pseudoreplication; keep positive and negative results. See `references/03`.
5. **Render and inspect.** Metadata checks are necessary but insufficient. Apply print-size gates and two visual passes. See `references/04`.
6. **Commit canonical replacements one at a time.** Backup → atomic swap → hash → registry sync → ledger update. See `references/05`.
7. **Clean only verified redundancy.** Within the authorized tree, after replacement verification. Keep source data, code, unique records and rollback copies.
8. **Close with a final acceptance report.** Use `templates/FINAL_ACCEPTANCE.md`. Fill every field from measured disk state. See `references/06`.

Run `python3 scripts/validate_final_submission.py --workspace <project> --ledger <ledger> --manifest <manifest>` before declaring completion. A failing gate means the work is not finished.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/check_skill.py <root>` | Validate this skill package structure and frontmatter. |
| `scripts/validate_final_submission.py` | Check PNG bytes, dimensions, DPI metadata, RGB mode, SHA256, ledger completeness and manifest consistency. Emits JSON; exits non-zero on failure. |

The validator checks evidence, not scientific truth. Scientific interpretation remains the operator's responsibility.

## References

- `references/01-execution-contract.md` — the full execution standard and priority rules.
- `references/02-task-ledger-and-blockers.md` — ledger schema, resumable checkpoints, blocker resolution patterns.
- `references/03-scientific-computation-gates.md` — real data, statistics, ML validity, negative controls.
- `references/04-visual-qa-and-print-spec.md` — typography, colour, collision gates, two-pass visual QA.
- `references/05-canonical-overwrite-and-sync.md` — authoritative paths, atomic transaction, cleanup, provenance.
- `references/06-final-acceptance.md` — acceptance checklist and reporting format.

## Limits

This skill enforces a process. It does not supply datasets, compute resources, journal approval or domain expertise. If an analysis is genuinely blocked by missing source data, record the exact blocker and complete every independent task instead of inventing a result.
