# Changelog

All notable changes to Kevin Cusnir's multilingual CV are recorded here.

## 1.2.0 — 2026-09-13

### Fixed

- **The live product link was a 404 in all three languages.** The CVs pointed at
  `ivrit-sheli-staging.onrender.com`, the Singapore service retired on
  2026-09-13 when the project finished moving to Frankfurt. A recruiter clicking
  the one link that shows the work got nothing. All three now point at
  `ivrit-sheli.onrender.com`, verified answering HTTP 200.
- The verifier had been red since 2026-09-11 because it required the literal
  string `Ivrit Sheli 2.2.0` while the three CVs correctly said 2.12.3. The
  content was right; the check was stale. It also pinned the old test figures
  139, 48 and 187, and the word `OAuth`, which disappeared when the sign-in
  sentence was rewritten.
- The honesty boundary markers still looked for the old wording. Google sign-in
  is live now and the two-real-account isolation check is the one open item, so
  the markers follow that sentence in each language.

### Changed

- The Ivrit Sheli version is no longer written into the verifier. It requires
  the three CVs to **agree** on one version, refuses a superseded one, and
  checks the 859 and 387 test figures appear in each. A number pinned in two
  places goes stale in one of them.
- New check: no CV or README may name a retired deployment host. That is the
  rule that would have caught this on the day the service was deleted.

## 1.1.0 — 2026-07-18

### Added

- Static recruiter-first banner shared across the repository README and the
  English, Spanish and Hebrew CVs.
- Deterministic 1280 × 640 SVG social-card source and upload-ready PNG.
- Reproducible Windows rendering command plus visual-asset documentation.
- Automated checks for banner integration, exact social-card dimensions,
  sub-1 MB delivery size and verified identity markers.

### Changed

- Unified the CV's public visual identity around Kevin Cusnir, Lirioth
  Teltanion and the KC ✦ LT signature without changing professional facts.
- Incremented the CV system from 1.0.0 to 1.1.0 for the coherent visual and
  recruiter-presentation update.

## 1.0.0 — 2026-07-18

### Added

- First explicit semantic version and reproducible CV verification workflow.
- Ivrit Sheli 2.2.0 as deployed full-stack evidence in English, Spanish and Hebrew.
- Exact 139-backend + 48-frontend = 187-test baseline with an honest OAuth verification boundary.
- Direct links to the four strongest live/source project pairs.
- Automated multilingual identity, evidence and education-boundary checks.
- Repository-specific agent rules for truth, translation parity and future version increments.

### Changed

- Aligned every headline to Junior Frontend & Full-Stack Developer · Creative Technologist.
- Expanded verified frontend, backend, database, testing, Docker and delivery skills.
- Removed the duplicated repository introduction and replaced it with one recruiter-first overview.
