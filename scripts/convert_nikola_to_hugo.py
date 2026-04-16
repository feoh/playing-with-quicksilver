#!/home/feoh/.openclaw/workspace/.venv/bin/python
from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

import yaml
from markdownify import markdownify as md

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / 'posts'
CONTENT_DIR = ROOT / 'content'
CONTENT_POSTS_DIR = CONTENT_DIR / 'posts'
STATIC_IMAGES_DIR = ROOT / 'static' / 'images'
IMAGES_DIR = ROOT / 'images'

MD_META_RE = re.compile(r'^<!--\n(?P<meta>.*?)\n-->\n*', re.S)
MD_FIELD_RE = re.compile(r'^\.\.\s+(?P<key>[a-z_]+):\s*(?P<value>.*)$')
PEL_FIELD_RE = re.compile(r'^(?P<key>[A-Za-z_][A-Za-z0-9_]*):\s*(?P<value>.*)$')
SKIP_SLUGS = {'article-template', 'article_template'}


def slugify(name: str) -> str:
    return re.sub(r'[^a-z0-9-]+', '-', name.lower()).strip('-')


def clean_value(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def normalize_date(value: str | None) -> str | None:
    value = clean_value(value)
    if not value:
        return None
    normalized = value.replace(' UTC-05:00', '-05:00').replace(' UTC-04:00', '-04:00')
    normalized = re.sub(r'^0(\d{4}-)', r'\1', normalized)
    for fmt in ('%Y-%m-%d %H:%M:%S %z', '%Y-%m-%d %H:%M:%S%z', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S'):
        try:
            dt = datetime.strptime(normalized, fmt)
            if dt.tzinfo is None:
                return dt.strftime('%Y-%m-%dT%H:%M:%S')
            return dt.strftime('%Y-%m-%dT%H:%M:%S%z')[:-2] + ':' + dt.strftime('%z')[-2:]
        except ValueError:
            pass
    return value


def clean_markdown_body(text: str) -> str:
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip() + '\n'


def normalize_meta(meta: dict[str, object], fallback_slug: str) -> dict[str, object]:
    slug = clean_value(str(meta.get('slug') or fallback_slug)) or fallback_slug
    raw_tags = clean_value(str(meta.get('tags') or ''))
    tags = list(dict.fromkeys(t.strip() for t in raw_tags.split(',') if t.strip())) if raw_tags else []
    return {
        'title': clean_value(str(meta.get('title') or fallback_slug.replace('-', ' ').title())) or fallback_slug,
        'slug': slugify(slug),
        'date': normalize_date(str(meta.get('date') or '')),
        'author': clean_value(str(meta.get('author') or meta.get('authors') or '')),
        'description': clean_value(str(meta.get('description') or meta.get('summary') or '')),
        'tags': tags,
    }


def parse_markdown(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text()
    meta: dict[str, object] = {}
    body = text
    m = MD_META_RE.match(text)
    if m:
        for line in m.group('meta').splitlines():
            line = line.strip()
            m2 = MD_FIELD_RE.match(line)
            if m2:
                meta[m2.group('key')] = m2.group('value')
        body = text[m.end():].lstrip()
    else:
        lines = text.splitlines()
        idx = 0
        while idx < len(lines):
            line = lines[idx]
            if not line.strip():
                idx += 1
                break
            m2 = PEL_FIELD_RE.match(line)
            if not m2:
                break
            meta[m2.group('key').lower()] = m2.group('value')
            idx += 1
        if meta:
            body = '\n'.join(lines[idx:]).lstrip()
    body = md(body, heading_style='ATX') if '<' in body else body
    return normalize_meta(meta, path.stem), clean_markdown_body(body)


def write_page(path: Path, meta: dict[str, object], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    front = {'title': meta['title'], 'slug': meta['slug']}
    if meta.get('date'):
        front['date'] = meta['date']
    if meta.get('author'):
        front['author'] = meta['author']
    if meta.get('description'):
        front['description'] = meta['description']
    if meta.get('tags'):
        front['tags'] = meta['tags']
    text = '---\n' + yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip() + '\n---\n\n' + body.strip() + '\n'
    path.write_text(text)


def make_home_page() -> None:
    (CONTENT_DIR / '_index.md').write_text('''---
title: Playing With Quicksilver
type: home
---

Personal writing from Chris Patti.
''')
    (CONTENT_POSTS_DIR / '_index.md').write_text('''---
title: Archive
---

A chronological list of posts from Playing With Quicksilver.
''')


def ensure_image_aliases() -> None:
    if not STATIC_IMAGES_DIR.exists():
        return
    by_lower = {p.name.lower(): p for p in STATIC_IMAGES_DIR.iterdir() if p.is_file()}
    referenced = set()
    for md_file in CONTENT_DIR.rglob('*.md'):
        text = md_file.read_text(errors='ignore')
        for ref in re.findall(r'\((/images/[^)]+)\)', text):
            referenced.add(Path(ref).name)
    for name in sorted(referenced):
        target = STATIC_IMAGES_DIR / name
        if target.exists():
            continue
        source = by_lower.get(name.lower())
        if source and source.exists():
            shutil.copy2(source, target)


def main() -> None:
    if CONTENT_DIR.exists():
        shutil.rmtree(CONTENT_DIR)
    CONTENT_POSTS_DIR.mkdir(parents=True, exist_ok=True)
    STATIC_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    if IMAGES_DIR.exists():
        shutil.copytree(IMAGES_DIR, STATIC_IMAGES_DIR, dirs_exist_ok=True)

    for path in sorted(POSTS_DIR.iterdir()):
        if not path.is_file():
            continue
        stem = slugify(path.stem)
        if stem in SKIP_SLUGS:
            continue
        if path.suffix != '.md':
            continue
        meta, body = parse_markdown(path)
        meta['slug'] = slugify(str(meta.get('slug') or stem))
        write_page(CONTENT_POSTS_DIR / f"{meta['slug']}.md", meta, body)
    make_home_page()
    ensure_image_aliases()


if __name__ == '__main__':
    main()
