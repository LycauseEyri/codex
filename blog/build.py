#!/usr/bin/env python3
"""Codex Blog: Static site generator for GitHub Pages.

Writes output to _site/ by default.
"""

import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader

# 鈹€鈹€ Paths 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
DEST = ROOT.parent / "_site"

# 鈹€鈹€ Helpers 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€


def parse_post(path: Path) -> dict:
    """Parse a markdown post with YAML-style frontmatter."""
    text = path.read_text(encoding="utf-8")
    meta = {"title": "", "date": "", "tags": [], "slug": path.stem}

    # Simple frontmatter parser (--- ... ---)
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if m:
        front, body = m.group(1), m.group(2)
        for line in front.strip().splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip().lower()
                val = val.strip().strip('"').strip("'")
                if key == "tags":
                    meta["tags"] = [t.strip() for t in val.split(",") if t.strip()]
                elif key in ("title", "date"):
                    meta[key] = val
    else:
        body = text

    meta["body"] = body
    meta["html"] = markdown.markdown(body, extensions=["fenced_code", "codehilite"])

    # Infer date from filename if not in frontmatter
    if not meta["date"]:
        m2 = re.match(r"(\d{4}-\d{2}-\d{2})", path.stem)
        if m2:
            meta["date"] = m2.group(1)

    return meta


def url_for(endpoint: str, path: str = "/") -> str:
    """Resolve a URL path for the static site."""
    return path


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


# 鈹€鈹€ Build 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€


def main():
    ensure_dir(DEST)
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    env.globals["url_for"] = url_for

    # 鈹€鈹€ 1. Collect & sort posts 鈹€鈹€
    posts = []
    for f in sorted(POSTS_DIR.glob("*.md"), reverse=True):
        post = parse_post(f)
        posts.append(post)

    # Sort by date descending
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)

    # 鈹€鈹€ 2. Generate individual post pages 鈹€鈹€
    tmpl_post = env.get_template("post.html")
    for post in posts:
        out_dir = DEST / "posts" / post["slug"]
        ensure_dir(out_dir)
        html = tmpl_post.render(post=post, posts=posts)
        (out_dir / "index.html").write_text(html, encoding="utf-8")

    # 鈹€鈹€ 3. Generate index (home) page 鈹€鈹€
    tmpl_index = env.get_template("index.html")
    index_html = tmpl_index.render(posts=posts)
    (DEST / "index.html").write_text(index_html, encoding="utf-8")

    # 鈹€鈹€ 4. Copy static assets 鈹€鈹€
    if STATIC_DIR.exists():
        dest_static = DEST / "static"
        if dest_static.exists():
            shutil.rmtree(dest_static)
        shutil.copytree(STATIC_DIR, dest_static)

    print(f"鉁?Built {len(posts)} post(s) 鈫?{DEST}")


if __name__ == "__main__":
    main()

