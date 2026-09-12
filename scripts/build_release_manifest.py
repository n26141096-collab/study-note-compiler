#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
from pathlib import Path

IGNORE_PARTS = {'.pytest_cache', '__pycache__', 'qa'}
SELF = 'RELEASE_MANIFEST.json'
MANIFEST = 'manifest.txt'


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def included(root, p):
    rel = p.relative_to(root)
    return p.is_file() and not any(part in IGNORE_PARTS for part in rel.parts)


def skill_version(root):
    text = (root / 'SKILL.md').read_text(encoding='utf-8')
    match = re.search(r'^\s{2}version:\s*["\']?([^"\'\s]+)', text, flags=re.M)
    return match.group(1) if match else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    args = ap.parse_args()
    root = Path(args.root).resolve()
    # First build a stable path list. RELEASE_MANIFEST is listed but self-hash is omitted.
    paths = sorted(str(p.relative_to(root)).replace('\\','/') for p in root.rglob('*') if included(root, p) and p.name not in {MANIFEST, SELF})
    paths += [MANIFEST, SELF]
    paths = sorted(set(paths))
    (root / MANIFEST).write_text('\n'.join(paths) + '\n', encoding='utf-8')

    entries = []
    for rel in paths:
        if rel == SELF:
            continue
        p = root / rel
        entries.append({'path': rel, 'size': p.stat().st_size, 'sha256': sha256(p)})
    version = skill_version(root)
    payload = {
        'format': 1,
        'release': f'{root.name}-v{version}' if version else root.name,
        'version': version,
        'self_omitted_from_hash_entries': True,
        'manifest_path': MANIFEST,
        'entries': entries,
    }
    (root / SELF).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'RELEASE_MANIFEST_BUILT={len(entries)}_HASHED_FILES')


if __name__ == '__main__':
    main()
