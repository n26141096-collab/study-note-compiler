#!/usr/bin/env python3
import argparse
from pathlib import Path
import yaml

ALLOWED_TYPES = {'page','slide','section','line_range','sheet_cell','timestamp','synthetic','unavailable'}
ALLOWED_CONF = {'HIGH','MEDIUM','LOW'}
PLACEHOLDERS = {'', 'todo', 'tbd', 'unknown', 'n/a', 'na', 'xxx', 'placeholder'}


def substantive(value, min_chars=1):
    if value is None:
        return False
    text = str(value).strip()
    return len(text) >= min_chars and text.lower() not in PLACEHOLDERS


def validate_locator(loc, min_evidence=12, allow_synthetic=False):
    issues = []
    if not isinstance(loc, dict):
        return ['LOCATOR_NOT_MAPPING']
    for key in ('file','locator_type','locator','evidence','confidence'):
        if key not in loc:
            issues.append(f'MISSING_{key.upper()}')
    if issues:
        return issues
    ltype = str(loc['locator_type'])
    if ltype not in ALLOWED_TYPES:
        issues.append('INVALID_LOCATOR_TYPE')
    if str(loc['confidence']).upper() not in ALLOWED_CONF:
        issues.append('INVALID_CONFIDENCE')
    if not substantive(loc['file'], 2):
        issues.append('INVALID_FILE')
    if not substantive(loc['locator'], 1):
        issues.append('INVALID_LOCATOR')
    if not substantive(loc['evidence'], min_evidence):
        issues.append('EVIDENCE_TOO_SHORT')
    if ltype == 'unavailable':
        issues.append('SOURCE_UNAVAILABLE')
    if ltype == 'synthetic' and not allow_synthetic:
        issues.append('SYNTHETIC_SOURCE_NOT_ALLOWED_IN_FORMAL_RELEASE')
    if bool(loc.get('visual_check_required')) and 'VISUAL_CHECK_REQUIRED' not in str(loc.get('notes','')):
        issues.append('VISUAL_CHECK_MARKER_MISSING')
    return issues


def iter_locators(data):
    for ku in data.get('knowledge_units', []) or []:
        for loc in ku.get('source_locators', []) or []:
            yield f"KU:{ku.get('id','UNKNOWN')}", loc
    for q in data.get('questions', []) or []:
        for loc in q.get('source_locators', []) or []:
            yield f"Q:{q.get('id','UNKNOWN')}", loc


def audit_file(path, min_evidence=12, allow_synthetic=False):
    data = yaml.safe_load(Path(path).read_text(encoding='utf-8')) or {}
    issues = []
    count = 0
    auditable = 0

    for kind, rows in (
        ('KU', data.get('knowledge_units', []) or []),
        ('Q', data.get('questions', []) or []),
    ):
        if not isinstance(rows, list):
            issues.append(f'{kind}_COLLECTION_NOT_LIST')
            continue
        seen_ids = set()
        for idx, row in enumerate(rows, 1):
            auditable += 1
            if not isinstance(row, dict):
                issues.append(f'{kind}:ROW_{idx}:NOT_MAPPING')
                continue
            owner_id = str(row.get('id', '')).strip() or f'ROW_{idx}'
            owner = f'{kind}:{owner_id}'
            if owner_id in seen_ids:
                issues.append(f'{owner}:DUPLICATE_ID')
            seen_ids.add(owner_id)
            required = kind == 'Q' or str(row.get('importance', '')).lower() in {'critical', 'high'}
            locs = row.get('source_locators')
            if locs is None:
                locs = []
            if not isinstance(locs, list):
                issues.append(f'{owner}:SOURCE_LOCATORS_NOT_LIST')
                continue
            if required and not locs:
                issues.append(f'{owner}:MISSING_SOURCE_LOCATORS')
            for loc in locs:
                count += 1
                for issue in validate_locator(loc, min_evidence, allow_synthetic):
                    issues.append(f'{owner}:{issue}')

    if auditable == 0:
        issues.append('NO_AUDITABLE_ITEMS')
    elif count == 0 and not any('MISSING_SOURCE_LOCATORS' in x for x in issues):
        issues.append('NO_SOURCE_LOCATORS')
    return issues, count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('yaml_file')
    ap.add_argument('--min-evidence', type=int, default=12)
    ap.add_argument('--allow-synthetic', action='store_true')
    args = ap.parse_args()
    issues, count = audit_file(args.yaml_file, args.min_evidence, args.allow_synthetic)
    print(f'SOURCE_LOCATORS={count}')
    if issues:
        for x in issues:
            print('FAIL', x)
        return 2
    print('PASS SOURCE_LOCATOR_GATE')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
