#!/usr/bin/env python3
import argparse
import csv
import hashlib
from pathlib import Path

ROLE_HINTS = {
    'source_question': ['exam', 'question', 'quiz', '題庫', '考題', '歷屆', '作業'],
    'user_note': ['note', '筆記'],
    'instructor_material': ['lecture', 'slide', 'ppt', '課堂', '講義', '老師'],
    'report_project': ['report', '報告', 'project'],
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def infer_role(name):
    low = name.lower()
    for role, hints in ROLE_HINTS.items():
        if any(h.lower() in low for h in hints):
            return role
    return 'unclassified_review_required'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('material_dir')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    root = Path(args.material_dir)
    rows = []
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        rows.append({
            'path': str(p.relative_to(root)),
            'size_bytes': p.stat().st_size,
            'sha256': sha256(p),
            'role_hint': infer_role(p.name),
            'role_confirmed': '',
            'notes': '',
        })
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else ['path','size_bytes','sha256','role_hint','role_confirmed','notes'])
        w.writeheader(); w.writerows(rows)
    print(f'WROTE={out} FILES={len(rows)}')


if __name__ == '__main__':
    main()
