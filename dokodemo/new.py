#!/usr/bin/env python3
"""Create today's post and register it in posts.json.

usage: python3 dokodemo/new.py <paper|book|concept> "Title"
"""
import datetime, json, pathlib, sys

TEMPLATES = {
    "paper": "**Paper**: \n**Link**: \n\n## One-line summary\n\n## Key idea\n\n## What I want to remember\n",
    "book": "**Book**: \n\n> \n\n## Thoughts\n",
    "concept": "## Definition\n\n## Why it matters\n\n## Example\n",
}

if len(sys.argv) != 3 or sys.argv[1] not in TEMPLATES:
    sys.exit(__doc__)
tag, title = sys.argv[1], sys.argv[2]

root = pathlib.Path(__file__).parent
index = root / "posts.json"
posts = json.loads(index.read_text()) if index.exists() else []

date = datetime.date.today().isoformat()
n = sum(p["date"] == date for p in posts) + 1
slug = f"{date}-{n}"

path = root / "posts" / f"{slug}.md"
path.parent.mkdir(exist_ok=True)
path.write_text(TEMPLATES[tag])

posts.append({"slug": slug, "date": date, "tag": tag, "title": title})
index.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + "\n")
print(path)
