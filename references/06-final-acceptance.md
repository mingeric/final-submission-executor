# 6. Final acceptance

Fill this checklist from measured disk state. Counts must be measured, not estimated.

## Mandatory checks

- [ ] Every requested deliverable exists at the exact canonical path and decodes.
- [ ] Format contract satisfied (for example RGB PNG at the specified width and DPI).
- [ ] Each canonical file's SHA256 recomputed after final write and recorded.
- [ ] Manifest, registry, source map, legend and manuscript all reference the actual files.
- [ ] No dangling references to retired figure numbers or directories.
- [ ] Fonts resolved without warnings in the real plotting environment.
- [ ] Two visual QA passes completed, with defects repaired and rerendered.
- [ ] Genuine negative results preserved and labelled.
- [ ] Redundant generated files removed or quarantined with a ledger.
- [ ] No writes outside the authorized tree.
- [ ] Task ledger has no unexamined PENDING rows; every BLOCKED row has an exact reason.
- [ ] Validator (`scripts/validate_final_submission.py`) exits zero.

## Final report format

1. What was actually completed: reconstructed X/6, supplementary families X/5, canonical files overwritten X.
2. Exact deliverable paths and final pixel dimensions.
3. Old and new SHA256 values for overwritten files.
4. New source-supported analyses and integrated existing results.
5. Font and rendering issues resolved.
6. Two-round visual QA result.
7. Manuscript and registry synchronization status.
8. Redundant files actually removed or quarantined.
9. Genuine unresolved scientific limitations and the exact dependency for each.

Never report a future action as done. If completion was impossible, state the precise remaining dependency and list the work that was completed.
