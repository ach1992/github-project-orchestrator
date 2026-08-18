#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[.-][0-9A-Za-z.-]+)?$")
GRAPHQL_RELEASE_QUERY = """
query($owner:String!,$name:String!,$tag:String!) {
  repository(owner:$owner,name:$name) {
    release(tagName:$tag) {
      id
      tagName
      isDraft
      isPrerelease
    }
  }
}
""".strip()


@dataclass(frozen=True)
class ReleaseMetadata:
    release_id: str
    tag_name: str
    is_draft: bool
    is_prerelease: bool


def run_checked(args: list[str], *, capture_output: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        check=True,
        text=True,
        capture_output=capture_output,
    )


def resolve_remote_tag_commit(tag: str) -> str | None:
    result = run_checked(
        [
            "git",
            "ls-remote",
            "--tags",
            "origin",
            f"refs/tags/{tag}",
            f"refs/tags/{tag}^{{}}",
        ]
    )
    direct: str | None = None
    peeled: str | None = None
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        sha, ref = parts
        if ref == f"refs/tags/{tag}^{{}}":
            peeled = sha
        elif ref == f"refs/tags/{tag}":
            direct = sha
    return peeled or direct


def get_release_metadata(owner: str, repo: str, tag: str) -> ReleaseMetadata | None:
    result = run_checked(
        [
            "gh",
            "api",
            "graphql",
            "-f",
            f"query={GRAPHQL_RELEASE_QUERY}",
            "-f",
            f"owner={owner}",
            "-f",
            f"name={repo}",
            "-f",
            f"tag={tag}",
            "--jq",
            '.data.repository.release | if . == null then "ABSENT" else [.id,.tagName,(.isDraft|tostring),(.isPrerelease|tostring)] | @tsv end',
        ]
    )
    value = result.stdout.strip()
    if value == "ABSENT":
        return None
    fields = value.split("\t")
    if len(fields) != 4:
        raise RuntimeError(f"Unexpected release metadata for {tag}: {value!r}")
    release_id, tag_name, is_draft, is_prerelease = fields
    if is_draft not in {"true", "false"} or is_prerelease not in {"true", "false"}:
        raise RuntimeError(f"Unexpected release boolean metadata for {tag}: {value!r}")
    return ReleaseMetadata(
        release_id=release_id,
        tag_name=tag_name,
        is_draft=is_draft == "true",
        is_prerelease=is_prerelease == "true",
    )


def create_remote_tag(repo_full_name: str, tag: str, sha: str) -> None:
    run_checked(
        [
            "gh",
            "api",
            "--method",
            "POST",
            f"repos/{repo_full_name}/git/refs",
            "-f",
            f"ref=refs/tags/{tag}",
            "-f",
            f"sha={sha}",
        ]
    )


def assert_tag_identity(tag: str, expected_sha: str) -> str:
    actual_sha = resolve_remote_tag_commit(tag)
    if actual_sha is None:
        raise RuntimeError(f"Remote tag {tag} is missing")
    if actual_sha != expected_sha:
        raise RuntimeError(
            f"Remote tag {tag} resolves to {actual_sha}, expected release SHA {expected_sha}"
        )
    return actual_sha


def verify_release_assets(tag: str, local_zip: Path, local_checksum: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="release-verify-") as tmp:
        destination = Path(tmp)
        run_checked(
            [
                "gh",
                "release",
                "download",
                tag,
                "-p",
                local_zip.name,
                "-p",
                local_checksum.name,
                "--dir",
                str(destination),
            ]
        )
        downloaded_zip = destination / local_zip.name
        downloaded_checksum = destination / local_checksum.name
        if not downloaded_zip.is_file() or not downloaded_checksum.is_file():
            raise RuntimeError(f"Release {tag} is missing required assets")
        if downloaded_zip.read_bytes() != local_zip.read_bytes():
            raise RuntimeError(f"Release {tag} asset {local_zip.name} does not match this candidate")
        if downloaded_checksum.read_bytes() != local_checksum.read_bytes():
            raise RuntimeError(
                f"Release {tag} asset {local_checksum.name} does not match this candidate"
            )


def verify_release_state(
    metadata: ReleaseMetadata,
    *,
    tag: str,
    expected_prerelease: bool,
    local_zip: Path,
    local_checksum: Path,
) -> None:
    if metadata.tag_name != tag:
        raise RuntimeError(
            f"Release metadata tag {metadata.tag_name} does not match expected tag {tag}"
        )
    if metadata.is_draft:
        raise RuntimeError(f"Release {tag} exists only as a draft")
    if metadata.is_prerelease != expected_prerelease:
        raise RuntimeError(
            f"Release {tag} prerelease={metadata.is_prerelease}, expected {expected_prerelease}"
        )
    verify_release_assets(tag, local_zip, local_checksum)


def publish_release() -> None:
    repo_full_name = os.environ["GH_REPO"]
    github_sha = os.environ["GITHUB_SHA"]
    if not re.fullmatch(r"[0-9a-fA-F]{40}", github_sha):
        raise RuntimeError(f"Invalid GITHUB_SHA: {github_sha!r}")
    if repo_full_name.count("/") != 1:
        raise RuntimeError(f"Unexpected GH_REPO: {repo_full_name!r}")
    owner, repo = repo_full_name.split("/", 1)

    version = Path("VERSION").read_text(encoding="utf-8").strip()
    if not VERSION_RE.fullmatch(version):
        raise RuntimeError(f"Invalid VERSION: {version}")
    tag = f"v{version}"
    expected_prerelease = "-" in version
    local_zip = Path("skill.zip")
    local_checksum = Path("skill.zip.sha256")
    for path in (local_zip, local_checksum):
        if not path.is_file():
            raise RuntimeError(f"Required release asset missing: {path}")

    tag_sha = resolve_remote_tag_commit(tag)
    if tag_sha is None:
        try:
            create_remote_tag(repo_full_name, tag, github_sha)
        except subprocess.CalledProcessError:
            # A concurrent creator may have won the race. Re-read authoritative remote state.
            pass
        tag_sha = assert_tag_identity(tag, github_sha)
    elif tag_sha != github_sha:
        raise RuntimeError(
            f"Version/tag collision: {tag} resolves to {tag_sha}, current release SHA is {github_sha}"
        )

    # Existing releases are successful no-ops only when they prove exact delivery of this candidate.
    metadata = get_release_metadata(owner, repo, tag)
    if metadata is not None:
        assert_tag_identity(tag, github_sha)
        verify_release_state(
            metadata,
            tag=tag,
            expected_prerelease=expected_prerelease,
            local_zip=local_zip,
            local_checksum=local_checksum,
        )
        print(f"Release {tag} already exists and exactly matches {github_sha} and both assets.")
        return

    # Re-check immediately before publication. gh --verify-tag prevents implicit tag creation/rebinding.
    assert_tag_identity(tag, github_sha)
    command = [
        "gh",
        "release",
        "create",
        tag,
        str(local_zip),
        str(local_checksum),
        "--verify-tag",
        "--title",
        tag,
        "--notes",
        f"Release {tag} of GitHub Project Orchestrator. See CHANGELOG.md for release details.",
    ]
    if expected_prerelease:
        command.append("--prerelease")

    try:
        run_checked(command, capture_output=False)
    except subprocess.CalledProcessError:
        # Reconcile a possible concurrent exact publication; any mismatch still fails closed below.
        metadata = get_release_metadata(owner, repo, tag)
        if metadata is None:
            raise

    assert_tag_identity(tag, github_sha)
    metadata = get_release_metadata(owner, repo, tag)
    if metadata is None:
        raise RuntimeError(f"Release {tag} was not observable after publication")
    verify_release_state(
        metadata,
        tag=tag,
        expected_prerelease=expected_prerelease,
        local_zip=local_zip,
        local_checksum=local_checksum,
    )
    print(f"Published and verified {tag} at exact commit {github_sha} with exact release assets.")


def main() -> int:
    try:
        publish_release()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"release publication failed closed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
