#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


LINK_RE = re.compile(r"^\s*-\s+\[([^\]]+)\]\(([^)]+)\)")


def page_url(markdown_path):
    path = markdown_path.split("#", 1)[0].strip()
    if path.startswith(("http://", "https://")):
        raise ValueError(f"External links are not valid sidebar targets: {markdown_path}")
    if not path.endswith(".md"):
        raise ValueError(f"Sidebar targets must be Markdown files: {markdown_path}")
    return "/" + path[:-3].lstrip("/") + ".html"


def parse_index(markdown):
    sections = []
    current_section = None
    current_group = None

    for line in markdown.splitlines():
        if line.startswith("## ") and not line.startswith("### "):
            current_section = {"title": line[3:].strip(), "groups": []}
            sections.append(current_section)
            current_group = None
            continue

        if line.startswith("### "):
            if current_section is None:
                continue
            current_group = {"title": line[4:].strip(), "items": []}
            current_section["groups"].append(current_group)
            continue

        match = LINK_RE.match(line)
        if not match or current_group is None:
            continue

        title, target = match.groups()
        current_group["items"].append({"title": title.strip(), "url": page_url(target)})

    return [
        {
            "title": section["title"],
            "groups": [group for group in section["groups"] if group["items"]],
        }
        for section in sections
        if any(group["items"] for group in section["groups"])
    ]


def quote(value):
    return json.dumps(value, ensure_ascii=False)


def render_navigation(sections):
    lines = ["sections:"]
    for section in sections:
        lines.append(f"  - title: {quote(section['title'])}")
        lines.append("    groups:")
        for group in section["groups"]:
            lines.append(f"      - title: {quote(group['title'])}")
            lines.append("        items:")
            for item in group["items"]:
                lines.append(f"          - title: {quote(item['title'])}")
                lines.append(f"            url: {quote(item['url'])}")
        lines.append("")

    lines.extend(
        [
            "maintenance:",
            f"  - title: {quote('Operation Log')}",
            f"    url: {quote('/log.html')}",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def wiki_path_for_url(url):
    relative = url.lstrip("/")
    if not relative.endswith(".html"):
        raise ValueError(f"Sidebar URLs must point to generated HTML pages: {url}")
    return Path("wiki") / (relative[:-5] + ".md")


def find_missing_targets(sections, wiki_files):
    missing = []
    for section in sections:
        for group in section["groups"]:
            for item in group["items"]:
                if wiki_path_for_url(item["url"]) not in wiki_files:
                    missing.append(item["url"])
    return missing


def repository_root():
    return Path(__file__).resolve().parents[3]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Sync GitHub Pages sidebar navigation from wiki/index.md."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check that navigation.yml is current.",
    )
    args = parser.parse_args(argv)

    root = repository_root()
    index_path = root / "wiki/index.md"
    navigation_path = root / ".github/pages/_data/navigation.yml"

    sections = parse_index(index_path.read_text(encoding="utf-8"))
    wiki_files = {path.relative_to(root) for path in (root / "wiki").rglob("*.md")}
    missing = find_missing_targets(sections, wiki_files)
    if missing:
        print("Missing sidebar targets:", file=sys.stderr)
        for target in missing:
            print(f"  - {target}", file=sys.stderr)
        return 1

    rendered = render_navigation(sections)
    existing = navigation_path.read_text(encoding="utf-8")

    if args.check:
        if existing != rendered:
            print(
                "Pages navigation is out of sync with wiki/index.md. "
                "Run .github/pages/scripts/sync_pages_navigation.py.",
                file=sys.stderr,
            )
            return 1
        print("Pages navigation is in sync.")
        return 0

    if existing != rendered:
        navigation_path.write_text(rendered, encoding="utf-8")
        print("Updated .github/pages/_data/navigation.yml from wiki/index.md.")
    else:
        print("Pages navigation is already in sync.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
