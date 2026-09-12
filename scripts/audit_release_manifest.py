#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
from pathlib import Path

SELF = 'RELEASE_MANIFEST.json'
IGNORE_PARTS = {'.pytest_cache', '__pycache__', 'qa'}


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def included(root, path):
    rel = path.relative_to(root)
    return path.is_file() and not any(part in IGNORE_PARTS for part in rel.parts)


def skill_version(root):
    skill = root / 'SKILL.md'
    if not skill.is_file():
        return None
    text = skill.read_text(encoding='utf-8')
    match = re.search(r'^\s{2}version:\s*["\']?([^"\'\s]+)', text, flags=re.M)
    return match.group(1) if match else None


def audit(root):
    root = Path(root).resolve()
    manifest_file = root / 'manifest.txt'
    release_file = root / SELF
    issues = []
    if not manifest_file.exists() or not release_file.exists():
        return ['RELEASE_MANIFEST_FILES_MISSING'], {}
    listed = [x.strip() for x in manifest_file.read_text(encoding='utf-8').splitlines() if x.strip()]
    if len(listed) != len(set(listed)):
        issues.append('MANIFEST_DUPLICATE_PATHS')
    for rel in listed:
        if not (root / rel).is_file():
            issues.append(f'MANIFEST_PATH_MISSING:{rel}')
    try:
        data = json.loads(release_file.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError) as exc:
        return [f'RELEASE_MANIFEST_INVALID:{exc}'], {'manifest_paths': len(listed)}
    if not data.get('self_omitted_from_hash_entries'):
        issues.append('SELF_OMISSION_POLICY_MISSING')
    version = skill_version(root)
    if not version:
        issues.append('SKILL_VERSION_MISSING')
    expected_release = f'{root.name}-v{version}' if version else root.name
    if data.get('version') != version or data.get('release') != expected_release:
        issues.append('RELEASE_ID_MISMATCH')
    entries = {x['path']: x for x in data.get('entries', [])}
    expected_entries = set(listed) - {SELF}
    if set(entries) != expected_entries:
        issues.append('HASH_ENTRY_SET_MISMATCH')
    actual_files = {
        str(p.relative_to(root)).replace('\\', '/')
        for p in root.rglob('*') if included(root, p)
    }
    listed_files = set(listed)
    for rel in sorted(actual_files - listed_files):
        issues.append(f'UNLISTED_FILE:{rel}')
    for rel in sorted(listed_files - actual_files):
        issues.append(f'LISTED_FILE_MISSING:{rel}')
    for rel in sorted(expected_entries & set(entries)):
        p = root / rel
        e = entries[rel]
        if not p.is_file():
            continue
        if e['size'] != p.stat().st_size:
            issues.append(f'SIZE_MISMATCH:{rel}')
        if e['sha256'] != sha256(p):
            issues.append(f'SHA256_MISMATCH:{rel}')
    return issues, {'manifest_paths': len(listed), 'hash_verified': len(entries)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    args = ap.parse_args()
    issues, stats = audit(args.root)
    if issues:
        for x in issues:
            print('FAIL', x)
        return 2
    print(f"MANIFEST_PATHS={stats['manifest_paths']}")
    print(f"HASH_VERIFIED={stats['hash_verified']}")
    print('PASS RELEASE_MANIFEST_GATE')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
