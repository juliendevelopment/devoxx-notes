#!/usr/bin/env python3
"""Turn one Devoxx Obsidian vault into the Starlight content of this site.

Run it before committing: `python3 sync.py [vault] [year]`
(defaults: the parent folder, year 2026).

Sources read from the vault:
- talks/general note.md            -> the home page (src/content/docs/index.mdx)
- talks/<Day NN> - <title>/note.md -> one raw-note page per talk, plus the notes index
- talks/talks-to-see-by-theme.md   -> "Talks I didn't see", minus the talks already noted

The vault notes are verbatim and partly in French. The English versions of the
French passages live in translations/<year>/<slug>.yml (`fr` block -> `en` block).
The script warns when a block no longer matches the note (stale translation) or
when a note still looks French (missing translation).

Everything under src/content/docs/ and src/sidebar.json is generated: don't edit it by hand.
"""
import json
import re
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
VAULT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT.parent
YEAR = sys.argv[2] if len(sys.argv) > 2 else "2026"
BASE = "/devoxx-notes"  # GitHub Pages project path, see astro.config.mjs
TALKS = VAULT / "talks"
DOCS = ROOT / "src/content/docs"
YEAR_DOCS = DOCS / YEAR
TRANSLATIONS = ROOT / "translations" / YEAR
CODE = re.compile(r"^(Mon|Tue|Wed|Thu|Fri) \d\d - ")
DAYS = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}
DATES = {"2026": {"Mon": "5 October", "Tue": "6 October", "Wed": "7 October", "Thu": "8 October", "Fri": "9 October"}}
LIST_ITEM = re.compile(r"^\s*([-*+]|\d+\.)\s")
FRENCH = re.compile(r"\b(les|des|est|pour|une|que|avec|dans|qui|nous|vous|ils|sont|mais|aussi|très|ça|où)\b"
                    r"|\b\w*(é|è|à|ù|ç|ê)\w*\b", re.I)
HTML_TAGS = {"a", "br", "details", "summary", "img", "div", "span", "sup", "sub", "kbd", "b", "i", "em", "strong"}
DISCLAIMER = ("These are raw notes, typed or handwritten live during the talk. "
              "Expect transcription errors, typos and video timestamps that can be a few minutes off.")


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def url(path):
    return f"{BASE}/{path.strip('/')}/" if path.strip("/") else f"{BASE}/"


def split_frontmatter(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return yaml.safe_load(text[4:end]) or {}, text[end + 5:]
    return {}, text


def frontmatter(data):
    return "---\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=10000) + "---\n\n"


# --- Markdown clean-up -------------------------------------------------------

def outside_code(text, fn):
    """Apply fn to the parts of text that are neither fenced code nor inline code."""
    out = []
    for i, part in enumerate(re.split(r"(^```.*?^```[^\n]*$)", text, flags=re.M | re.S)):
        if i % 2:
            out.append(part)
        else:
            out.append("".join(p if j % 2 else fn(p) for j, p in enumerate(re.split(r"(`[^`\n]+`)", part))))
    return "".join(out)


def escape_stray_tags(text):
    """`<XML>` in a note is text, not an HTML tag."""
    return re.sub(r"<(/?)([A-Za-z][\w-]*)",
                  lambda m: m.group(0) if m.group(2).lower() in HTML_TAGS else f"&lt;{m.group(1)}{m.group(2)}",
                  text)


def mdx_safe(text):
    return outside_code(text, lambda s: escape_stray_tags(s).replace("{", "&#123;").replace("}", "&#125;"))


def obsidianish(body):
    """Render like Obsidian: a single newline is a line break, a table or a list
    needs no blank line around it."""
    lines = body.split("\n")
    out, fence = [], False
    for i, line in enumerate(lines):
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if line.startswith("```"):
            fence = not fence
            out.append(line)
            continue
        if fence:
            out.append(line)
            continue
        prev = out[-1] if out else ""
        if LIST_ITEM.match(line) and prev.strip() and not LIST_ITEM.match(prev) \
                and not prev.startswith((" ", "\t", "#")):
            out.append("")
        is_table = line.lstrip().startswith("|")
        if is_table and nxt.strip() and not nxt.lstrip().startswith("|"):
            out += [line, ""]
            continue
        breakable = line.strip() and not line.startswith("#") and not is_table
        if breakable and nxt.strip() and not nxt.startswith(("#", "```")) \
                and not LIST_ITEM.match(nxt) and not nxt.lstrip().startswith("|"):
            line = line.rstrip() + "  "
        out.append(line)
    return "\n".join(out).rstrip() + "\n"


# --- Talk notes --------------------------------------------------------------

def translate(folder, body):
    """Replace the French passages with their English version from translations/."""
    path = TRANSLATIONS / f"{slug(folder.name)}.yml"
    if path.exists():
        for item in yaml.safe_load(path.read_text(encoding="utf-8")) or []:
            fr, en = item["fr"].rstrip("\n"), item["en"].rstrip("\n")
            if fr in body:
                body = body.replace(fr, en)
            else:
                print(f"  ⚠ stale translation in {path.name}: {fr[:60]!r}…")
    french = [l.strip() for l in body.splitlines()
              if not l.startswith("```") and "](" not in l
              and len(FRENCH.findall(re.sub(r"https?://\S+", "", l))) >= 3]
    if french:
        print(f"  ⚠ {folder.name}: {len(french)} line(s) still look French, add them to {path.name}:")
        for l in french[:3]:
            print(f"      {l[:90]}")
    return body


def talk_page(folder, meta, body):
    body = translate(folder, body)
    body = re.sub(r"\A\s*# .*\n", "", body, count=1)          # the H1 is the page title
    body = re.sub(r"\n## My take\s*\Z", "\n", body.rstrip() + "\n")  # hide an empty "My take"
    if meta.get("video"):
        button = (f'<a class="video-button" href="{meta["video"]}" target="_blank" rel="noopener">'
                  "▶ Watch the video</a>\n\n")
        body = button + body.lstrip("\n")
    body = obsidianish(outside_code(body, escape_stray_tags))
    data = {
        "title": meta.get("title", folder.name[5:]),
        "description": f"Raw notes from Devoxx Belgium {YEAR}: {', '.join(meta.get('speakers') or [])}",
        "banner": {"content": f'⚠️ {DISCLAIMER} <a href="{url(f"{YEAR}/notes")}#how-to-read-these-notes">More</a>'},
    }
    return frontmatter(data) + body


def collect_talks():
    talks = []
    for folder in sorted((p for p in TALKS.iterdir() if p.is_dir() and CODE.match(p.name)),
                         key=lambda p: (list(DAYS).index(p.name[:3]), p.name)):
        note = folder / "note.md"
        if note.exists():
            meta, body = split_frontmatter(note.read_text(encoding="utf-8"))
            talks.append({"folder": folder, "code": folder.name[:6], "slug": slug(folder.name),
                          "meta": meta, "body": body})
    return talks


def write_talks(talks, top):
    for t in talks:
        target = YEAR_DOCS / "notes" / t["slug"]
        target.mkdir(parents=True)
        (target / "index.md").write_text(talk_page(t["folder"], t["meta"], t["body"]), encoding="utf-8")
        if (t["folder"] / "images").is_dir():
            shutil.copytree(t["folder"] / "images", target / "images")


def card(t, rank=None):
    meta = t["meta"]
    return {"href": f"{YEAR}/notes/{t['slug']}", "code": t["code"], "slot": (meta.get("slot") or "")[:5],
            "title": meta.get("title", CODE.sub("", t["folder"].name)), "speakers": ", ".join(meta.get("speakers") or []),
            "format": meta.get("format") or "", "video": bool(meta.get("video")), "rank": rank}


def write_notes_index(talks, top):
    lines = [frontmatter({"title": "My raw notes",
                          "description": f"Everything I noted during the talks at Devoxx Belgium {YEAR}, day by day."}),
             "import { Aside } from '@astrojs/starlight/components';",
             "import TalkCard from '../../../../components/TalkCard.astro';", "",
             "## How to read these notes", "",
             f'<Aside type="caution" title="Raw notes">{DISCLAIMER} '
             "Each heading with a timestamp jumps to that minute of the video. "
             "The ⭐ cards are the talks I recommend first.</Aside>", ""]
    day = None
    for t in talks:
        if t["code"][:3] != day:
            if day:
                lines += ["</div>", ""]
            day = t["code"][:3]
            lines += [f"## {DAYS[day]} {DATES.get(YEAR, {}).get(day, '')}".rstrip(), "", '<div class="talk-grid">']
        lines.append(f"<TalkCard {{...{json.dumps(card(t, top.get(t['folder'].name)), ensure_ascii=False)}}} />")
    lines += ["</div>", ""]
    (YEAR_DOCS / "notes" / "index.mdx").write_text("\n".join(lines), encoding="utf-8")


# --- Talks I didn't see ------------------------------------------------------

def parse_talks_to_see():
    text = (TALKS / "talks-to-see-by-theme.md").read_text(encoding="utf-8")
    _, body = split_frontmatter(text)
    themes, theme, talk = [], None, None
    for line in body.splitlines():
        if line.startswith("# ") and not line.startswith("# Talks to see"):
            theme = {"name": line[2:].strip(), "intro": "", "talks": []}
            themes.append(theme)
        elif theme is None:
            continue
        elif line.startswith("## "):
            talk = {"title": line[3:].strip()}
            theme["talks"].append(talk)
        elif line.startswith("_") and not theme["talks"]:
            theme["intro"] = line.strip("_ ")
        elif talk is not None and (m := re.match(r"- \*\*(\w+):\*\* (.*)", line)):
            talk[m.group(1).lower()] = m.group(2).strip()
    return themes


def link_target(field):
    m = re.search(r"\]\((https?://[^)]+)\)", field or "")
    return m.group(1) if m else None


def write_missed(talks):
    seen_ids, seen_titles = set(), set()
    for t in talks:
        ids = t["meta"].get("devoxx_id")
        seen_ids.update(str(i) for i in (ids if isinstance(ids, list) else [ids]) if i)
        seen_ids.update(re.findall(r"/talks/(\d+)/", t["body"]))
        seen_titles.add(slug(t["meta"].get("title", "")))
    lines = [frontmatter({"title": "Talks I didn't see",
                          "description": "The talks I wanted to attend but could not, grouped by theme, with their videos."}),
             "import MissedTalk from '../../../components/MissedTalk.astro';", "",
             "I could not be everywhere. These are the talks I had selected but missed, grouped by theme — "
             "from the closest to AI adoption in the enterprise to general Java. "
             "Most of them have a recording: grab a coffee ☕", ""]
    count = 0
    for theme in parse_talks_to_see():
        missed = []
        for talk in theme["talks"]:
            schedule = link_target(talk.get("schedule"))
            tid = re.search(r"/talks/(\d+)/", schedule or "")
            if (tid and tid.group(1) in seen_ids) or slug(talk["title"].rstrip(".")) in seen_titles:
                continue
            missed.append({"title": talk["title"], "speakers": talk.get("speaker", ""),
                           "when": talk.get("when", ""), "schedule": schedule,
                           "video": link_target(talk.get("video")), "summary": talk.get("summary", "")})
        if not missed:
            continue
        count += len(missed)
        out_of_scope = "out of scope" in theme["name"].lower()
        name = re.sub(r"\s*\(out of scope\)", "", theme["name"])
        cards = ['<div class="missed-grid">',
                 *(f"<MissedTalk {{...{json.dumps(m, ensure_ascii=False)}}} />" for m in missed), "</div>"]
        intro = mdx_safe(theme["intro"])
        if out_of_scope:
            lines += [f"## {name}", "", f"_{intro}_", "",
                      '<details class="out-of-scope">', "", f"<summary>Out of my scope — show the {len(missed)} talks</summary>", "",
                      *cards, "", "</details>", ""]
        else:
            lines += [f"## {name}", "", f"_{intro}_", "", *cards, ""]
    (YEAR_DOCS / "talks-i-didnt-see.mdx").write_text("\n".join(lines), encoding="utf-8")
    return count


# --- Home page ---------------------------------------------------------------

def resolve_wikilinks(text, talks):
    by_folder = {t["folder"].name: t for t in talks}

    def repl(m):
        target, label = m.group(1), m.group(2)
        target = target.removeprefix("talks/")
        if target.endswith("/note") and target[:-5] in by_folder:
            href = url(f"{YEAR}/notes/{by_folder[target[:-5]]['slug']}")
        elif target == "talks-to-see-by-theme":
            href = url(f"{YEAR}/talks-i-didnt-see")
        elif target == "notes":
            href = url(f"{YEAR}/notes")
        else:
            print(f"  ⚠ unresolved link [[{m.group(1)}]] in general note")
            return label or target
        return f"[{label or target}]({href})"

    return re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", repl, text)


def top_talks(body):
    """Folder name -> rank, from the numbered list under '## Talks to share'."""
    section = re.search(r"^## Talks to share\n(.*?)(?=^## |\Z)", body, flags=re.M | re.S)
    ranks = {}
    for m in re.finditer(r"^(\d+)\. \[\[(?:talks/)?([^\]|]+)/note", section.group(1) if section else "", flags=re.M):
        ranks[m.group(2)] = int(m.group(1))
    return ranks


def home_top_section(section, talks):
    """'## Talks to share' as glowing cards instead of a numbered list."""
    by_folder = {t["folder"].name: t for t in talks}
    intro, cards = [], []
    for line in section.splitlines()[1:]:
        m = re.match(r"^(\d+)\. \[\[(?:talks/)?([^\]|]+)/note(?:\|([^\]]+))?\]\] — ([^.]+)\. (.*)$", line)
        if m and m.group(2) in by_folder:
            t = by_folder[m.group(2)]
            cards.append({**card(t, int(m.group(1))), "title": m.group(3) or t["meta"].get("title"),
                          "speakers": m.group(4), "why": m.group(5),
                          "videoUrl": t["meta"].get("video")})
        elif line.strip():
            intro.append(line)
    out = ["## Talks to share", "", *[mdx_safe(l) for l in intro], "", '<div class="top-grid">']
    out += [f"<TopTalk {{...{json.dumps(c, ensure_ascii=False)}}} />" for c in cards]
    return out + ["</div>", ""]


def write_home(talks, missed_count):
    meta, body = split_frontmatter((TALKS / "general note.md").read_text(encoding="utf-8"))
    sections = re.split(r"(?=^## )", body, flags=re.M)
    out = []
    for section in sections:
        if section.startswith("## Talks to share"):
            out += home_top_section(section, talks)
        elif section.startswith("## How to read this site"):
            lines = section.rstrip().splitlines()
            out += [lines[0], "", "<Steps>", "", mdx_safe(resolve_wikilinks("\n".join(lines[1:]).strip(), talks)),
                    "", "</Steps>", ""]
        else:
            out.append(mdx_safe(resolve_wikilinks(section, talks)).rstrip() + "\n")
    videos = sum(1 for t in talks if t["meta"].get("video"))
    stats = [{"value": len(talks), "label": "talks noted"}, {"value": videos, "label": "with video"},
             {"value": len(top_talks(body)), "label": "to share"}, {"value": missed_count, "label": "missed, to watch"}]
    data = {
        "title": meta.get("title", f"Devoxx Belgium {YEAR}"),
        "description": meta.get("tagline", ""),
        "template": "splash",
        "hero": {
            "title": f"Devoxx Belgium {YEAR}",
            "tagline": meta.get("tagline", ""),
            "actions": [
                {"text": "Talks to share", "link": "#talks-to-share", "icon": "star", "variant": "primary"},
                {"text": "My raw notes", "link": url(f"{YEAR}/notes"), "icon": "open-book", "variant": "secondary"},
                {"text": "Talks I didn't see", "link": url(f"{YEAR}/talks-i-didnt-see"), "icon": "right-arrow",
                 "variant": "minimal"},
            ],
        },
    }
    page = [frontmatter(data),
            "import { Steps } from '@astrojs/starlight/components';",
            "import Stats from '../../components/Stats.astro';",
            "import TopTalk from '../../components/TopTalk.astro';", "",
            f"<Stats items={{{json.dumps(stats)}}} />", "",
            *out]
    (DOCS / "index.mdx").write_text("\n".join(page), encoding="utf-8")


def write_sidebar(talks):
    days = []
    for t in talks:
        day = DAYS[t["code"][:3]]
        if not days or days[-1]["label"] != day:
            days.append({"label": day, "collapsed": True, "items": []})
        days[-1]["items"].append({"slug": f"{YEAR}/notes/{t['slug']}", "label": CODE.sub("", t["folder"].name)})
    sidebar = [{"label": f"Devoxx Belgium {YEAR}", "items": [
        {"label": "Start here", "link": "/"},
        {"slug": f"{YEAR}/talks-i-didnt-see"},
        {"label": "My raw notes", "items": [{"slug": f"{YEAR}/notes", "label": "All talks"}, *days]},
    ]}]
    (ROOT / "src/sidebar.json").write_text(json.dumps(sidebar, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    if YEAR_DOCS.exists():
        shutil.rmtree(YEAR_DOCS)
    (YEAR_DOCS / "notes").mkdir(parents=True)
    talks = collect_talks()
    _, general = split_frontmatter((TALKS / "general note.md").read_text(encoding="utf-8"))
    top = top_talks(general)
    write_talks(talks, top)
    write_notes_index(talks, top)
    missed = write_missed(talks)
    write_home(talks, missed)
    write_sidebar(talks)
    print(f"{len(talks)} talks, {missed} missed talks synced into {YEAR_DOCS}")


if __name__ == "__main__":
    main()
