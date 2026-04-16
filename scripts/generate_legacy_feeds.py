#!/home/feoh/.openclaw/workspace/.venv/bin/python
from __future__ import annotations

import html
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / 'content' / 'posts'
PUBLIC = ROOT / 'public'
BASE = 'https://playingwithquicksilver.net/'
SITE_TITLE = 'Playing With Quicksilver'
SITE_DESC = 'Personal writing from Chris Patti.'


def parse_post(path: Path):
    text = path.read_text()
    if not text.startswith('---\n'):
        return None
    _, fm, body = text.split('---\n', 2)
    data = yaml.safe_load(fm) or {}
    slug = data.get('slug') or path.stem
    title = data.get('title') or slug.replace('-', ' ').title()
    date = data.get('date')
    if not date:
        return None
    summary = data.get('description') or body.strip().split('\n\n', 1)[0].strip()
    url = f"{BASE}posts/{slug}/"
    return {
        'title': title,
        'url': url,
        'date': datetime.fromisoformat(str(date).replace('Z', '+00:00')),
        'summary': summary,
        'id': url,
    }


posts = [p for p in (parse_post(path) for path in sorted(CONTENT.glob('*.md'))) if p]
posts.sort(key=lambda p: p['date'], reverse=True)
updated = posts[0]['date'] if posts else datetime.now(timezone.utc)
PUBLIC.mkdir(parents=True, exist_ok=True)
out = PUBLIC / 'feed.atom'
with out.open('w', encoding='utf-8') as fh:
    fh.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
    fh.write('<feed xmlns="http://www.w3.org/2005/Atom">\n')
    fh.write(f'  <title>{html.escape(SITE_TITLE)}</title>\n')
    fh.write(f'  <id>{BASE}</id>\n')
    fh.write(f'  <updated>{updated.astimezone(timezone.utc).isoformat()}</updated>\n')
    fh.write(f'  <link href="{BASE}feed.atom" rel="self" />\n')
    fh.write(f'  <link href="{BASE}" rel="alternate" />\n')
    fh.write(f'  <subtitle>{html.escape(SITE_DESC)}</subtitle>\n')
    for post in posts[:20]:
        fh.write('  <entry>\n')
        fh.write(f'    <title>{html.escape(post["title"])}</title>\n')
        fh.write(f'    <link href="{post["url"]}" />\n')
        fh.write(f'    <id>{post["id"]}</id>\n')
        fh.write(f'    <updated>{post["date"].astimezone(timezone.utc).isoformat()}</updated>\n')
        fh.write(f'    <published>{post["date"].astimezone(timezone.utc).isoformat()}</published>\n')
        fh.write(f'    <summary>{html.escape(post["summary"])}</summary>\n')
        fh.write('  </entry>\n')
    fh.write('</feed>\n')
print(out)
