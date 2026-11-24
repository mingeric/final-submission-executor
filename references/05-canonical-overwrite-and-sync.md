# 5. Canonical overwrite and synchronization

## Establish the authoritative state once

- Resolve symlinks to physical paths and record them.
- Read the manifest, registry, legends, manuscript references and build scripts before editing.
- Treat a `NOT_A_SUBMISSION_TARGET` branch label as scope information only when a later override names the merged paper as the target.
- Preserve branch-specific manuscripts and source data; do not renumber them to match the merged paper.

## Transaction per deliverable

1. Resolve exact canonical path and current SHA256.
2. Render a staged candidate from source data.
3. Pass scientific QA and both visual passes.
4. Verify format: RGB, dimensions, DPI, decode, file size.
5. Move the old canonical file into a bounded, recoverable superseded location.
6. Atomically move the staged file into the canonical path.
7. Recompute SHA256 and update manifest, registry, figure-to-source map, legend and manuscript reference together.
8. Mark the ledger row verified and continue to the next deliverable.

If any check fails, keep the existing canonical file and record that specific failure. Never replace a validated figure with an inferior one merely to create a diff.

## Cleanup discipline

- Only after successful integration and verification.
- Only inside the explicitly authorized tree. Never touch sibling projects or shared source data.
- Delete or quarantine verified redundant generated files: superseded renders, stale previews, abandoned staging outputs, exact duplicate copies.
- Keep source tables, scripts, unique records, audit trails and a recoverable rollback copy.
- Record old path, action, basis, SHA256 and bytes in a cleanup ledger.
- Do not count relocation as reclaimed disk space, and do not create permanent backup trees.

## Provenance

One primary owner per result. A primary result must not be repackaged as an independent discovery. Unique evidence from a retired figure family must be migrated into the active supplementary structure before that family is retired.
