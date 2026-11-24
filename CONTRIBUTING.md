# Contributing

Keep changes small and verifiable.

1. Run `python3 scripts/check_skill.py .` and `python3 -m unittest discover -s tests -v` before opening a pull request.
2. If you change a gate, add an offline test that demonstrates both the passing and failing case.
3. Do not add real research data, personal paths, credentials or generated figure outputs to this repository. Tests must use synthetic fixtures only.
4. Prefer plain language in documentation. State limits explicitly; do not promise scientific validity from a mechanical check.
5. When documenting a workflow change, update both README files and the relevant reference page.

Issues describing a real failure mode are welcome, especially silent failures where a check reports success but the deliverable is wrong.
