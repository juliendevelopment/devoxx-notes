#!/usr/bin/env python3
"""Copy the processed talk notes from ../talks into docs/ for MkDocs.

Only talk folders (`talks/<Day NN> - <title>/note.md` + `images/`) are
published; the loose files in talks/ (general note, Slides to get…) are not.
Run it before committing: `python3 sync.py`.
"""
import re
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
TALKS = ROOT.parent / "talks"
DOCS = ROOT / "docs"
CODE = re.compile(r"^(Mon|Tue|Wed|Thu|Fri) \d\d - ")
DAYS = {"Mon": "Monday 5 October", "Tue": "Tuesday 6 October",
        "Wed": "Wednesday 7 October", "Thu": "Thursday 8 October",
        "Fri": "Friday 9 October"}
LIST_ITEM = re.compile(r"^\s*([-*+]|\d+\.)\s")


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def split_frontmatter(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return yaml.safe_load(text[4:end]) or {}, text[end + 5:]
    return {}, text


def obsidianish(body):
    """Obsidian starts a list without a blank line before it; Python-Markdown doesn't."""
    out, prev = [], ""
    for line in body.splitlines():
        if LIST_ITEM.match(line) and prev.strip() and not LIST_ITEM.match(prev) \
                and not prev.startswith((" ", "\t", "#")):
            out.append("")
        out.append(line)
        prev = line
    return "\n".join(out) + "\n"


def with_video(body, video):
    """Put the video link right under the H1 so it is visible on mobile."""
    if not video:
        return body
    return re.sub(r"^(# .*\n)", rf"\1\n[▶ Video]({video})\n\n", body, count=1, flags=re.M)


def main():
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir()
    talks = []
    for folder in sorted(p for p in TALKS.iterdir() if p.is_dir() and CODE.match(p.name)):
        note = folder / "note.md"
        if not note.exists():
            continue
        meta, body = split_frontmatter(note.read_text(encoding="utf-8"))
        target = DOCS / slug(folder.name)
        target.mkdir()
        page = "---\n" + yaml.safe_dump({"title": f"{folder.name[:6]} · {meta.get('title', folder.name)}"},
                                        allow_unicode=True) + "---\n\n"
        (target / "index.md").write_text(page + obsidianish(with_video(body, meta.get("video"))), encoding="utf-8")
        if (folder / "images").is_dir():
            shutil.copytree(folder / "images", target / "images")
        talks.append((folder.name, target.name, meta))

    lines = ["# Devoxx Belgium 2026 — talk notes", "",
             "Notes de Julien, prises pendant les talks (verbatim).", ""]
    day = None
    for name, path, meta in talks:
        if name[:3] != day:
            day = name[:3]
            lines += [f"## {DAYS[day]}", ""]
        speakers = ", ".join(meta.get("speakers") or [])
        video = " · ▶" if meta.get("video") else ""
        lines.append(f"- **{meta.get('slot', '')[:5]}** [{meta.get('title', name)}]({path}/index.md)  ")
        lines.append(f"  {speakers} · {meta.get('format', '')}{video}")
    (DOCS / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(talks)} talks synced into {DOCS}")


if __name__ == "__main__":
    main()
