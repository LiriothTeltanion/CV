# AGENTS.md — Kevin Cusnir Multilingual CV

## Purpose

This public repository is the canonical recruiter-facing CV for **Kevin Cusnir**, with **Lirioth Teltanion** preserved as the creative identity. English, Spanish and Hebrew must describe the same verified professional evidence.

## Mandatory workflow

1. Read `README.md`, all three CV files, `VERSION` and `CHANGELOG.md`.
2. Run `git status --short --branch` before editing.
3. Change verified facts in all affected languages; never update only one translation.
4. Run `python tools/verify_cv.py` and `git diff --check` after editing.
5. Review the complete diff before committing or publishing.

## Truth boundaries

- Keep the professional positioning junior and recruiter-readable.
- Do not invent employment dates, employer names, education completion, certifications, users, revenue or project metrics.
- Keep Developers Institute education explicitly in progress until completion is independently confirmed.
- Preserve broad employment year ranges unless Kevin supplies exact months.
- Distinguish live products, public showcases, learning archives and roadmap work.
- Keep Ivrit Sheli's final live OAuth authorization-code exchange marked unverified end to end until confirmed.

## Versioning

- Use semantic versions in `VERSION`.
- Increment the minor version for a coherent recruiter-content, project or workflow update.
- Increment the patch version for a narrow correction with no meaningful content change.
- Reserve a major version for a structural CV redesign or positioning change.
- Update `VERSION`, `CHANGELOG.md` and the README version label together.

## Public safety

- Never add secrets, private exports, identity documents, private messages, health or financial data.
- Keep the canonical email `kevincusnir@gmail.com`.
- Use accessible Markdown, meaningful link text and relative paths for repository files.
- Do not commit, push, tag or release unless Kevin explicitly requests it.
