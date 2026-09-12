#!/usr/bin/env python3
import argparse
from pathlib import Path
import yaml

TRUE_VALUES = {True, 1, 'true', 'yes', 'y', '1', '✓', 'pass', 'present'}
FALSE_VALUES = {False, 0, None, 'false', 'no', 'n', '0', '', '✗', 'missing'}


def as_bool(v):
    if isinstance(v, str):
        v = v.strip().lower()
    if v in TRUE_VALUES:
        return True
    if v in FALSE_VALUES:
        return False
    raise ValueError(f'UNRECOGNIZED_BOOLEAN:{v!r}')


def compute_row(row):
    if not isinstance(row, dict):
        raise ValueError('ROW_NOT_MAPPING')
    if 'status' in row or 'computed_status' in row:
        raise ValueError('HAND_ENTERED_STATUS_FORBIDDEN')
    required = ['knowledge_unit', 'source', 'note', 'l1_l2', 'l3_l4', 'pitfall']
    missing = [k for k in required if k not in row]
    if missing:
        raise ValueError('MISSING_' + ','.join(missing))
    source = as_bool(row['source'])
    note = as_bool(row['note'])
    l1_l2 = as_bool(row['l1_l2'])
    l3_required = as_bool(row.get('l3_l4_required', True))
    l3_l4 = as_bool(row['l3_l4']) if l3_required else True
    pitfall_required = as_bool(row.get('pitfall_required', True))
    pitfall = as_bool(row['pitfall']) if pitfall_required else True
    if not source or not note:
        status = 'GAP'
    elif l1_l2 and l3_l4 and pitfall:
        status = 'PASS'
    else:
        status = 'PARTIAL'
    out = dict(row)
    out['computed_status'] = status
    return out


def load_knowledge_ids(path):
    data = yaml.safe_load(Path(path).read_text(encoding='utf-8')) or {}
    rows = data.get('knowledge_units', []) or []
    ids, issues, seen = [], [], set()
    if not isinstance(rows, list) or not rows:
        return [], ['KNOWLEDGE_UNITS_EMPTY']
    for idx, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            issues.append(f'KNOWLEDGE_ROW_{idx}:NOT_MAPPING')
            continue
        ku_id = str(row.get('id', '')).strip()
        if not ku_id:
            issues.append(f'KNOWLEDGE_ROW_{idx}:MISSING_ID')
            continue
        if ku_id in seen:
            issues.append(f'KNOWLEDGE_DUPLICATE_ID:{ku_id}')
            continue
        seen.add(ku_id)
        ids.append(ku_id)
    return ids, issues


def audit(path, knowledge_path=None):
    data = yaml.safe_load(Path(path).read_text(encoding='utf-8')) or {}
    rows = data.get('coverage', [])
    if not isinstance(rows, list) or not rows:
        return [], ['COVERAGE_EMPTY']
    computed, issues, seen = [], [], set()
    for idx, row in enumerate(rows, 1):
        try:
            c = compute_row(row)
            computed.append(c)
            ku_id = str(c.get('knowledge_unit', '')).strip()
            if ku_id in seen:
                issues.append(f'DUPLICATE_COVERAGE_KU:{ku_id}')
            seen.add(ku_id)
            if c['computed_status'] != 'PASS':
                issues.append(f"{c.get('knowledge_unit','ROW'+str(idx))}:{c['computed_status']}")
        except Exception as exc:
            issues.append(f"ROW_{idx}:{exc}")
    if knowledge_path:
        expected, knowledge_issues = load_knowledge_ids(knowledge_path)
        issues.extend(knowledge_issues)
        expected_set = set(expected)
        for ku_id in sorted(expected_set - seen):
            issues.append(f'MISSING_COVERAGE_KU:{ku_id}')
        for ku_id in sorted(seen - expected_set):
            issues.append(f'UNKNOWN_COVERAGE_KU:{ku_id}')
    return computed, issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('coverage_yaml')
    ap.add_argument('--knowledge', help='knowledge_units.yaml; enables exact KU set validation')
    ap.add_argument('--out')
    args = ap.parse_args()
    computed, issues = audit(args.coverage_yaml, args.knowledge)
    if args.out:
        Path(args.out).write_text(yaml.safe_dump({'coverage': computed}, allow_unicode=True, sort_keys=False), encoding='utf-8')
        print(f'WROTE_COMPUTED_COVERAGE={args.out}')
    if issues:
        for x in issues:
            print('FAIL', x)
        return 2
    print(f'COVERAGE_ROWS={len(computed)}')
    print('PASS COVERAGE_COMPUTED_GATE')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
