# Quality Standard — Nikhil Bheda GitHub Portfolio

This document defines what makes the repository strong, review-ready, and portfolio-safe.

## Quality Goals

| Goal | What it means |
| --- | --- |
| Clear first impression | README explains purpose, value, workflow, stack, and setup. |
| Reviewable structure | Architecture, case study, roadmap, and quality docs are easy to find. |
| Safe collaboration | Issue templates, PR template, security policy, support guide, and code of conduct exist. |
| Repeatable checks | Repository health workflow validates the professional documentation layer. |
| Portfolio readiness | A reviewer can understand the project without asking for missing context. |
| Metadata polish | Repository descriptions, topics, and homepage links communicate the project clearly in GitHub cards/search. |

## Stack Profile

| Area | Value |
| --- | --- |
| Detected stack | Project-specific |
| Primary language | Project-specific |
| Topics | github-profile, profile-readme, developer-portfolio, portfolio, documentation, full-stack, flutter |

## Recommended Checks

| Check | Command / Location |
| --- | --- |
| Markdown lint | `npx --yes markdownlint-cli2@0.22.1 "*.md" "docs/*.md" ".github/*.md"` |
| Repository health | `python scripts/validate_repository_health.py` |
| CI verification | `GitHub Actions → Repository Health workflow` |

## Repository Health Gate

The local script `scripts/validate_repository_health.py` and GitHub Actions workflow `.github/workflows/repository-health.yml` check that the project has:

- README with a documentation hub.
- Architecture, case study, roadmap, quality, and review docs.
- Contribution, security, support, and conduct files.
- Issue and pull request templates.
- Clear repository ownership.
- `.gitignore` coverage for local caches, environment files, and editor noise.
- `.gitattributes` and `.editorconfig` line-ending policy for LF-normalized files.
- Stable Markdown links and SVG assets.
- No flaky third-party README/widget image sources.

## Metadata Standard

Public portfolio repositories should have:

- A concise description that explains product value, not just technology.
- Topics covering framework, language, product category, and recruiter/search keywords.
- A homepage URL when a working demo exists.
- README status links and stack indicators that match the actual project state.
- Avoid third-party generated README widgets when stable GitHub-native links are enough.
- Consistent naming and spelling across GitHub metadata, README, and resume.
- Inclusion in the project showcase catalog when the repository is part of the portfolio story.

## Definition of Strong

A strong repository should be able to answer these questions quickly:

1. What problem does it solve?
2. Who is it for?
3. What is the main workflow?
4. How is the code/project organized?
5. How can someone run, review, or extend it?
6. What is planned next?
7. How are contributions and security handled?

## Continuous Improvement

After every meaningful update:

- Update README if the user-facing behavior changes.
- Update architecture docs if structure changes.
- Update roadmap when items are completed or reprioritized.
- Update the project showcase catalog when a repository becomes more/less important.
- Add screenshots or demos when the UI/workflow becomes visually important.
- Keep commits small and meaningful.
