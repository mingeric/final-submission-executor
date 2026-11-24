# 3. Scientific computation gates

Automation must not turn a weak result into a publishable-looking one.

## Data provenance

- Every analysis names its source table, accession/cohort, biological unit, sample count and denominator.
- Never infer scientific ownership from duplicate filenames, first hash match or historical figure numbers.
- Distinguish patient-level, donor-level, cell-level, spot-level and cancer-level inference. Pseudoreplication invalidates cell- or spot-level claims when the biological unit is donor or patient.
- If two tables contain the same concept under different labels or genome builds, normalize explicitly and assert the join is non-empty.

## Statistics and machine learning

- Choose the method from the question and data structure, not from a menu of algorithm names.
- Every model needs a baseline, an evaluation design, uncertainty and a reproducible implementation.
- Fit imputation, scaling, feature selection and hyperparameters on training data only.
- Use grouped or patient-disjoint splits when groups exist; verify no group overlap.
- Report informative negatives as negatives. Do not cherry-pick the highest metric after the fact.
- Prefer stratified/sensitivity analysis over unstable covariate adjustment when covariates come from the same measurement matrix or have near-zero variance.
- Check sign consistency across strata; a majority of significant strata is not enough if signs flip.
- Distinguish internal transport tests (nested CV, leave-one-cancer-out) from genuine external validation.
- Negative controls must be applied at the relevant unit (e.g. site-by-site subtraction, not a global comparison).

## Visualization honesty

- Unknown is not zero. Show missing explicitly.
- Do not clip display ranges to exaggerate differences; lock shared colour scales only for genuinely comparable panels.
- Computational pseudo-space is not anatomy. Label embeddings and reconstructed coordinates as such.
- Use real source-derived plots; never substitute demonstration data or a schematic for evidence.
- Preserve authentic null results (e.g. zero significant hits) with precision.

## Gate questions before committing a panel

1. Does every number trace to a named source file and script?
2. Is the biological unit and n stated?
3. Are adjustment, uncertainty and multiple-testing family correct?
4. Could the finding be a known confounder (proliferation, purity, batch, group leakage)?
5. Would a negative control reproduce the same apparent effect?
6. Does the figure claim more than the analysis supports?
