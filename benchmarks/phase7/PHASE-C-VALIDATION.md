# Phase C Validation Contract

The canonical migration is accepted only when all of the following are true on one exact candidate HEAD:

1. `tests/test_phase_c_runtime_migration.py` proves exact selected P1-P5 fragment composition and no bytes outside the selected canonical surfaces changed relative to Phase C base.
2. Existing immutable-runtime equivalence, Rule/Goal traceability, adversarial/eval, package, platform-package, release-intent and runtime-cleanliness checks remain green.
3. Effective diff contains only the five canonical runtime surfaces plus directly necessary CI/test/evidence files.
4. No lifecycle/status namespace, Rule ID, `CAN_EXECUTE`, `MASTER_STOP`, Worker assignment/staleness, delivery proof, machine-relay transport, or simultaneous-effect obligation semantics are lost or newly implied.
5. No version/release intent is introduced.
6. A fresh independent HIGH_ASSURANCE reviewer inspects the exact Base/Head and complete effective diff before integration.
7. HIGH-risk integration remains separately human-gated.

Live-model/API A/B evidence is optional corroboration and is not part of this deterministic validation contract.
