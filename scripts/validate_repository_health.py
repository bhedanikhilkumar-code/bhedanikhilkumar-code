"""Validate profile repository documentation health.

This script mirrors the GitHub Actions Repository Health gate so checks can run
both locally and in CI.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ".gitattributes",
    ".gitignore",
    ".markdownlint.json",
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "SUPPORT.md",
    "CODE_OF_CONDUCT.md",
    "scripts/validate_repository_health.py",
    ".github/CODEOWNERS",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    "docs/ARCHITECTURE.md",
    "docs/CASE_STUDY.md",
    "docs/ROADMAP.md",
    "docs/QUALITY.md",
    "docs/PROJECT_SHOWCASE.md",
    "docs/PORTFOLIO_REVIEW_GUIDE.md",
    "docs/REVIEW_CHECKLIST.md",
]

FORBIDDEN_WIDGET_SOURCES = [
    "github-readme-stats.vercel.app",
    "streak-stats.demolab.com",
    "github-readme-activity-graph.vercel.app",
    "readme-typing-svg.herokuapp.com",
    "skillicons.dev",
    "komarev.com",
    "img.shields.io",
    "raw.githubusercontent.com/bhedanikhilkumar-code/bhedanikhilkumar-code/output/",
]

SUSPICIOUS_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_ed25519",
}

LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def fail(title: str, items: list[str]) -> None:
    print(title)
    for item in items:
        print(f"- {item}")
    raise SystemExit(1)


def repo_path(path: str | Path) -> Path:
    return ROOT / path


def markdown_files() -> list[Path]:
    return (
        list(ROOT.glob("*.md"))
        + list((ROOT / "docs").glob("*.md"))
        + list((ROOT / ".github").glob("*.md"))
    )


def validate_required_files() -> None:
    missing = [file for file in REQUIRED_FILES if not repo_path(file).exists()]
    if missing:
        fail("Missing professional repository files:", missing)


def validate_readme() -> None:
    readme = repo_path("README.md").read_text(encoding="utf-8", errors="ignore")
    checks = {
        "README has enough detail": len(readme) >= 1500,
        "README has H1": readme.startswith("# Nikhil Bheda"),
        "README has documentation hub": "Documentation Hub" in readme,
        "README links architecture": "docs/ARCHITECTURE.md" in readme,
        "README links roadmap": "docs/ROADMAP.md" in readme,
        "README links quality standard": "docs/QUALITY.md" in readme,
        "README links project showcase": "docs/PROJECT_SHOWCASE.md" in readme,
        "README links portfolio review guide": "docs/PORTFOLIO_REVIEW_GUIDE.md" in readme,
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        fail("README quality checks failed:", failed)


def validate_relative_links_and_images() -> None:
    missing_links: list[str] = []
    missing_images: list[str] = []
    relative_images: list[Path] = []

    for file in markdown_files():
        text = file.read_text(encoding="utf-8", errors="ignore")
        for match in LINK_PATTERN.finditer(text):
            href = match.group(1).strip()
            if not href or href.startswith(("#", "http://", "https://", "mailto:")):
                continue

            target = href.split("#", 1)[0]
            if not target:
                continue

            target_path = file.parent / target
            is_image = match.group(0).startswith("!")
            if is_image:
                relative_images.append(target_path)

            if not target_path.exists():
                item = f"{file.relative_to(ROOT)} -> {href}"
                if is_image:
                    missing_images.append(item)
                else:
                    missing_links.append(item)

    if missing_links:
        fail("Missing relative Markdown links:", missing_links)
    if missing_images:
        fail("Missing relative Markdown images:", missing_images)

    for image in sorted(set(relative_images)):
        if image.suffix.lower() == ".svg":
            svg = image.read_text(encoding="utf-8", errors="ignore")
            if "<svg" not in svg or "</svg>" not in svg:
                fail("Invalid SVG assets:", [str(image.relative_to(ROOT))])


def validate_forbidden_widgets() -> None:
    forbidden_hits: list[str] = []
    for file in markdown_files():
        text = file.read_text(encoding="utf-8", errors="ignore")
        for source in FORBIDDEN_WIDGET_SOURCES:
            if source in text:
                forbidden_hits.append(f"{file.relative_to(ROOT)} -> {source}")

    if forbidden_hits:
        fail("Forbidden flaky README/widget sources found:", forbidden_hits)


def validate_line_ending_policy() -> None:
    gitattributes = repo_path(".gitattributes").read_text(encoding="utf-8", errors="ignore")
    checks = {
        ".gitattributes normalizes text to LF": "* text=auto eol=lf" in gitattributes,
        ".gitattributes marks PNG as binary": "*.png binary" in gitattributes,
        ".editorconfig requests LF": "end_of_line = lf" in repo_path(".editorconfig").read_text(
            encoding="utf-8", errors="ignore"
        ),
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        fail("Line-ending policy checks failed:", failed)


def warn_suspicious_files() -> None:
    suspicious = [
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.is_file() and path.name in SUSPICIOUS_NAMES
    ]
    for path in suspicious:
        print(f"::warning file={path}::Review sensitive-looking tracked file")


def main() -> None:
    validate_required_files()
    validate_readme()
    validate_relative_links_and_images()
    validate_forbidden_widgets()
    validate_line_ending_policy()
    warn_suspicious_files()
    print("Repository health check passed.")


if __name__ == "__main__":
    main()
