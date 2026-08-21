# Qwen Bootstrap

This repository contains the canonical GitHub Project Orchestrator runtime under [`skill/`](skill/).

When this repository is provided to a Qwen environment as the instruction source, use this file only as a bootstrap. Do not treat `QWEN.md`, `README.md`, or platform documentation as a second runtime specification.

Canonical control kernel: @skill/SKILL.md

## Activate the orchestrator

1. Read `skill/SKILL.md` as the control kernel. Qwen Code's `@skill/SKILL.md` context reference above loads the canonical entrypoint when this repository is opened as a project.
2. Resolve the requested role (`MASTER` or `WORKER`) and current task from the user's request and authoritative repository/GitHub evidence.
3. Follow the one-step router in `skill/SKILL.md` and load only the referenced files that the current event requires.
4. Treat the portable runtime under `skill/` as canonical. Do not invent Qwen-specific orchestration rules or persistent manager-state files.
5. Keep platform/tool capability separate from project authority. If a required capability is unavailable, follow the canonical unavailable-capability and human-relay rules from the runtime.

## Qwen Code

Qwen Code supports Agent Skills with `SKILL.md`. Release packages include `github-project-orchestrator-qwen.zip`, generated from the same canonical runtime. Extract its `github-project-orchestrator/` folder into a configured Qwen Skill directory such as `~/.qwen/skills/` or a project `.qwen/skills/` directory.

## Repository-link environments

If the Qwen environment can inspect this GitHub repository but cannot install a Skill package, provide the repository URL and instruct it to read `QWEN.md` first. This bootstrap then routes it to the canonical runtime without maintaining a separate Qwen fork.
