#!/usr/bin/env python3
"""Runtime inventory and canonical-rule regression guard."""

import re
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill"
RULE_MAP = ROOT / "design" / "RULE-MAP.md"

sys.path.insert(0, str(ROOT / "tools"))
from validate_skill import markdown_prose, validate_links


WORKER_IDENTITY = (
    "Assignment ID",
    "Contract Revision",
    "Repository",
    "Worker",
    "Base SHA",
    "Assigned Branch",
    "Start HEAD",
    "Checkpoint HEAD",
    "Integration Target",
)

WORKER_PRECEDENCE = (
    "STALE_ASSIGNMENT",
    "MATERIAL_DECISION_REQUIRED",
    "SCOPE_CHANGE_REQUIRED",
    "ENVIRONMENT_MISMATCH",
    "BLOCKED",
    "READY_FOR_REVIEW",
)

REQUIRED_HIGH_CONSEQUENCE_RULES = {
    "OUTCOME-INTEGRITY",
    "EVIDENCE-TRUTH",
    "MUTATION-IDEMPOTENT",
    "AUTHORITY-SCOPE",
    "PERSISTENT-PROGRESS",
    "VALIDATION-ECONOMICS",
    "DEFENSIVE-SECURITY-CONTINUITY",
    "WORKER-BOUNDED",
    "ASSIGNMENT-IDENTITY",
    "WORKER-HANDOFF-PRECEDENCE",
    "REVIEW-FRESHNESS",
    "INTEGRATION-GATE",
    "RELEASE-MODEL-DISCOVER",
    "DELIVERY-PROOF",
    "RECOVERY-AUTHORITATIVE",
    "MACHINE-RELAY",
    "USER-STOP",
}


def words(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").split())


def section(source: str, heading: str) -> str:
    level = len(heading) - len(heading.lstrip("#"))
    prose = markdown_prose(source)
    matches = list(re.finditer("^" + re.escape(heading) + "$", prose, re.M))
    if len(matches) != 1:
        raise AssertionError(f"Expected one {heading} section")
    start = matches[0].end()
    following = re.search(rf"^#{{1,{level}}} ", prose[start:], re.M)
    end = start + following.start() if following else len(source)
    return source[start:end]


def packet(source: str, name: str) -> str:
    blocks = re.findall(r"^(`{3,}|~{3,})[^\n]*\n(.*?)^\1[ \t]*$", source, re.M | re.S)
    matches = [body for _, body in blocks if body.splitlines()[:1] == [f"# {name}"]]
    if len(matches) != 1:
        raise AssertionError(f"Expected one complete fenced {name} packet")
    return matches[0]


def require_fields(body: str, fields: tuple[str, ...]) -> None:
    actual = {line.partition(":")[0] for line in body.splitlines() if ":" in line}
    missing = set(fields) - actual
    if missing:
        raise AssertionError(f"{body.splitlines()[0]} missing fields: {sorted(missing)}")


def check_worker(contract: str, protocol: str) -> None:
    identity = section(contract, "## Worker assignment identity")
    correction = section(protocol, "## 6. Correction/resume")
    for field in WORKER_IDENTITY:
        if field not in identity or field not in correction:
            raise AssertionError(f"Assignment or correction lost identity: {field}")

    dispatch = packet(protocol, "WORKER DISPATCH")
    require_fields(dispatch, WORKER_IDENTITY + (
        "Issue/Work item", "Allowed actions", "Goal / Scope / Acceptance",
        "Required validation", "Special constraints",
    ))
    if "worker-protocol.md#5-handoff" not in dispatch:
        raise AssertionError("Copied dispatch has no receiver handoff contract")

    handoff = packet(section(protocol, "## 5. Handoff"), "WORKER HANDOFF")
    require_fields(handoff, WORKER_IDENTITY + (
        "STATUS", "Issue/Work item", "HEAD", "PR", "Completed", "Validation", "Blocker/Decision",
    ))
    precedence = section(protocol, "## 4. Staleness and blockers")
    ordered = re.findall(r"^\|\s*`([A-Z_]+)`\s*\|", precedence, re.M)
    if tuple(ordered) != WORKER_PRECEDENCE:
        raise AssertionError(f"Worker controlling status precedence changed: {ordered}")
    status_line = next(line for line in handoff.splitlines() if line.startswith("STATUS:"))
    statuses = [status.strip() for status in status_line.removeprefix("STATUS:").split("|")]
    if sorted(statuses) != sorted(WORKER_PRECEDENCE):
        raise AssertionError("Worker handoff and controlling statuses disagree")


def check_reviewer(protocol: str) -> None:
    dispatch = packet(protocol, "INDEPENDENT REVIEW")
    if "independent-review.md#result" not in dispatch:
        raise AssertionError("Copied reviewer dispatch has no receiver result contract")
    result = section(protocol, "## Result")
    body = packet(result, "INDEPENDENT REVIEW RESULT")
    require_fields(body, (
        "Completion", "Verdict", "Envelope", "- Repository", "- Integration Target/Base",
        "- Candidate", "- Pull Request", "- Work item/acceptance", "Findings", "  Evidence",
        "  Impact", "  Action", "  Verification", "Residual risk", "Limitations",
    ))
    activation = result.split(body, 1)[0]
    if "MachineRelay" not in activation or "(relay-transport.md)" not in activation:
        raise AssertionError("Reviewer result must activate relay transport at the call site")
    for pair in ("INCOMPLETE / NO_VERDICT", "COMPLETE / CHANGES_REQUIRED", "COMPLETE / APPROVE"):
        if f"`{pair}`" not in result:
            raise AssertionError(f"Independent review lost decision: {pair}")


def check_pending(kernel: str, master: str, review: str) -> None:
    route = "master-cycle.md#pending-jobs)"
    if route not in kernel or route not in section(review, "## 3. Validation and CI"):
        raise AssertionError("Pending jobs must be reachable from both active delivery and CI")
    pending = section(master, "### Pending jobs")
    rows = re.findall(r"^\|[^|\n]+\|[ \t]*([^|\n]+?)[ \t]*\|$", pending, re.M)
    actions = [cell for cell in rows[1:] if cell.strip("-: ")]
    failure = "(review-integration.md#3-validation-and-ci)"
    alternatives = "(authority-gates.md#capability-selection)"
    if not (any(failure in action for action in actions)
            and any(alternatives in action for action in actions)
            and any(failure not in action and alternatives not in action for action in actions)):
        raise AssertionError("Pending jobs lost a waiting, terminal, or blocked action")


def check_link_validation() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        entry = root / "SKILL.md"
        ref = root / "ref.md"
        ref.write_text("## 5. Pending jobs\n## Résumé\n## Résumé\n", encoding="utf-8")
        valid = (
            "# Entry\n[local](#entry)\n[CI](ref.md#5-pending-jobs)\n"
            "[duplicate](ref.md#r%C3%A9sum%C3%A9-1)\n"
            "````text\n## Template heading\n```\n[sample](missing.md)\n````\n"
        )
        entry.write_text(valid, encoding="utf-8")
        validate_links(root)
        for target in ("#template-heading", "ref.md#5-removed", "absent.md", "../outside.md"):
            entry.write_text(valid + f"[broken]({target})\n", encoding="utf-8")
            try:
                validate_links(root)
            except ValueError as exc:
                if target not in str(exc):
                    raise
            else:
                raise AssertionError(f"Validator accepted a broken route: {target}")


def main() -> None:
    kernel = SKILL / "SKILL.md"
    kernel_words = words(kernel)
    runtime_markdown = (
        path for path in SKILL.rglob("*.md")
        if path.is_file() and "__pycache__" not in path.parts
    )
    runtime_words = sum(words(path) for path in runtime_markdown)
    package_words = sum(
        words(path)
        for path in SKILL.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    )

    if (SKILL / "references" / "eval-scenarios.md").exists():
        raise AssertionError("development evaluation leaked back into the packaged runtime")

    references = SKILL / "references"
    check_worker(
        (references / "task-contract.md").read_text(encoding="utf-8"),
        (references / "worker-protocol.md").read_text(encoding="utf-8"),
    )
    check_reviewer((references / "independent-review.md").read_text(encoding="utf-8"))
    check_pending(
        kernel.read_text(encoding="utf-8"),
        (references / "master-cycle.md").read_text(encoding="utf-8"),
        (references / "review-integration.md").read_text(encoding="utf-8"),
    )
    check_link_validation()

    rule_text = RULE_MAP.read_text(encoding="utf-8")
    rule_ids = set(
        re.findall(r"^\|\s*`([A-Z0-9]+(?:-[A-Z0-9]+)+)`\s*\|", rule_text, re.MULTILINE)
    )
    missing = sorted(REQUIRED_HIGH_CONSEQUENCE_RULES - rule_ids)
    if missing:
        raise AssertionError(f"canonical high-consequence rules disappeared: {missing}")

    print(
        f"PASS runtime-invariants kernel_words={kernel_words} "
        f"runtime_words={runtime_words} package_words={package_words}"
    )


if __name__ == "__main__":
    main()
