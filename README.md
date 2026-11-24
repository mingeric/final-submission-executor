# final-submission-executor

An Agent Skill for the last mile of a research or figure-production project: turning a "final execution" specification into files that are actually written, checked and synchronized.

This skill is for the stage where another inventory or status report would be a failure. It encodes a simple contract: recover existing valid work, solve blockers, compute what is missing, render and inspect, overwrite the canonical file atomically, synchronize its records, and report measured completion.

It does not supply data, compute or domain judgment. It supplies the discipline that prevents a finished-looking package from being mistaken for a finished one.

## Install

Clone into the skill directory your agent reads:

```bash
git clone https://github.com/mingeric/final-submission-executor.git
# place the resulting directory where your client expects project skills
```

Python 3.9+ standard library is sufficient.

## Quick start

```bash
python3 scripts/check_skill.py .
python3 -m unittest discover -s tests -v

python3 scripts/validate_final_submission.py \
  --workspace path/to/project \
  --ledger path/to/project/TASK_LEDGER.tsv \
  --manifest path/to/project/CANONICAL_MANIFEST.tsv
```

The validator prints a JSON report and exits non-zero if any canonical file is missing, does not decode, has the wrong colour mode, dimensions or DPI, fails its recorded SHA256, or if the ledger has an unexamined pending task. A documented `BLOCKED` row passes; an unexplained one does not.

## How an execution runs

1. Read the specification once and extract authoritative paths, write scope, deliverable contract and acceptance criteria.
2. Copy `templates/TASK_LEDGER.tsv` into the project and create one row per independently verifiable task.
3. Resolve blockers in order: environment, paths, ownership, readability, stale staging output.
4. Use only traceable sources; preserve genuine negative results; prevent leakage and pseudoreplication.
5. Render, inspect the whole figure, inspect dense crops, repair and rerender.
6. Commit each validated replacement on its own: backup, atomic swap, recompute hashes, update manifest/registry/legend/manuscript.
7. Remove only verified redundancy inside the authorized tree.
8. Fill `templates/FINAL_ACCEPTANCE.md` from measured disk state.

See `references/` for the detailed contract, ledger rules, computation gates, visual QA, overwrite protocol and final reporting format.

## Files

| Path | Purpose |
|---|---|
| `SKILL.md` | Main instructions and non-negotiable rules |
| `references/01`–`06` | Execution contract, blockers, science, visual QA, overwrite, acceptance |
| `scripts/check_skill.py` | Package structure and frontmatter check |
| `scripts/validate_final_submission.py` | Evidence validator for a project workspace |
| `templates/` | Task ledger, canonical manifest, acceptance report |
| `tests/` | Offline tests using synthetic fixtures only |

## Honest boundary

`validate_final_submission.py` checks evidence fields, not scientific truth. It cannot decide whether an analysis is well designed or whether a figure tells the truth about the data. That judgment stays with the operator, and an unresolved evidence gap must be reported rather than filled with a plausible result.

## License

MIT. See `LICENSE`.
