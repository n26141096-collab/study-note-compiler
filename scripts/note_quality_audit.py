#!/usr/bin/env python3
"""Mechanical professional-note audit for v2.3.0.

This gate checks structure, provenance, modeling completeness, assessment coverage,
and obvious placeholder/redundancy defects. It does NOT claim to prove the semantic
truth of source paraphrases; source-aware human/agent review remains part of SOURCE_GATE.
"""
import argparse
import json
import re
from pathlib import Path
import yaml

from source_locator_audit import validate_locator
from coverage_audit import audit as audit_coverage
from learner_facing_audit import audit as audit_learner_facing

PLACEHOLDER_PATTERNS = [
    r'\bTODO\b', r'\bTBD\b', r'\bPLACEHOLDER\b', r'\bLOREM\b', r'\bXXX\b',
    r'完全沒有任何實質內容', r'待補', r'待填', r'此處填入',
]
MAJOR = {'critical','high'}
LAYER_FIELDS = ['core','what','why','how','relationships','application','pitfalls','recall']
KU_MARKER_RE = re.compile(r'<!--\s*ku:\s*([A-Za-z0-9_.-]+)\s*-->', re.I)


def text_len(v):
    if isinstance(v, list):
        return sum(len(str(x).strip()) for x in v)
    if isinstance(v, dict):
        return sum(text_len(x) for x in v.values())
    return len(str(v or '').strip())


def substantive(v, min_chars=12):
    return text_len(v) >= min_chars


def locator_ok_list(locs, allow_synthetic=False, min_evidence=12):
    if not isinstance(locs, list) or not locs:
        return False
    return all(not validate_locator(x, min_evidence, allow_synthetic) for x in locs)


def duplicate_paragraph_ratio(md):
    paras = []
    for raw in md.splitlines():
        s = raw.strip()
        if not s or s.startswith(('#','<!--',':::','|')) or s == '---':
            continue
        if len(s) < 20:
            continue
        norm = re.sub(r'\s+', ' ', re.sub(r'[`*_]', '', s)).lower()
        paras.append(norm)
    if len(paras) < 2:
        return 0.0
    duplicates = len(paras) - len(set(paras))
    return duplicates / len(paras)


def extract_ku_blocks(md):
    """Return explicit KU marker blocks before the assessment section."""
    assessment = re.search(r'^##\s+B(?:｜|\||\s)', md, flags=re.M | re.I)
    note_end = assessment.start() if assessment else len(md)
    matches = list(KU_MARKER_RE.finditer(md[:note_end]))
    blocks, duplicates = {}, []
    for idx, match in enumerate(matches):
        ku_id = match.group(1)
        end = matches[idx + 1].start() if idx + 1 < len(matches) else note_end
        raw = md[match.end():end]
        plain = re.sub(r'<!--.*?-->', ' ', raw, flags=re.S)
        plain = re.sub(r'[#>*`_|-]+', ' ', plain)
        plain = re.sub(r'\s+', ' ', plain).strip()
        if ku_id in blocks:
            duplicates.append(ku_id)
        else:
            blocks[ku_id] = plain
    return blocks, sorted(set(duplicates))


def audit(note_md, knowledge_yaml, assessment_yaml, coverage_yaml, allow_synthetic=False):
    md = Path(note_md).read_text(encoding='utf-8')
    kd = yaml.safe_load(Path(knowledge_yaml).read_text(encoding='utf-8')) or {}
    ad = yaml.safe_load(Path(assessment_yaml).read_text(encoding='utf-8')) or {}
    kus = kd.get('knowledge_units', []) or []
    qs = ad.get('questions', []) or []
    majors = [x for x in kus if str(x.get('importance','')).lower() in MAJOR]
    blockers = []
    details = {}

    for pat in PLACEHOLDER_PATTERNS:
        if re.search(pat, md, flags=re.I):
            blockers.append('PLACEHOLDER_CONTENT_DETECTED')
            break
    if not majors:
        blockers.append('NO_MAJOR_KNOWLEDGE_UNITS')

    ku_blocks, duplicate_markers = extract_ku_blocks(md)
    major_ids = [str(x.get('id', '')).strip() for x in majors if str(x.get('id', '')).strip()]
    missing_ku_blocks = sorted(x for x in major_ids if x not in ku_blocks)
    thin_ku_blocks = sorted(x for x in major_ids if x in ku_blocks and len(ku_blocks[x]) < 120)
    if duplicate_markers or missing_ku_blocks or thin_ku_blocks:
        blockers.append('NOTE_KU_COVERAGE_INCOMPLETE')
    details['note_ku_markers'] = len(ku_blocks)
    details['missing_note_kus'] = missing_ku_blocks
    details['thin_note_kus'] = thin_ku_blocks
    details['duplicate_note_ku_markers'] = duplicate_markers

    # Source Fidelity 20: 14 KU + 6 assessment.
    ku_source_ratio = (sum(locator_ok_list(x.get('source_locators'), allow_synthetic) for x in majors) / len(majors)) if majors else 0
    q_source_ratio = (sum(locator_ok_list(x.get('source_locators'), allow_synthetic) for x in qs) / len(qs)) if qs else 0
    source_score = round(14 * ku_source_ratio + 6 * q_source_ratio)
    details['Source Fidelity'] = source_score
    if source_score < 16:
        blockers.append('SOURCE_FIDELITY_BELOW_16')
    if any(not locator_ok_list(x.get('source_locators'), allow_synthetic) for x in majors):
        blockers.append('MAJOR_KU_SOURCE_LOCATOR_INCOMPLETE')
    if any(not locator_ok_list(x.get('source_locators'), allow_synthetic) for x in qs):
        blockers.append('QUESTION_SOURCE_LOCATOR_INCOMPLETE')

    # Knowledge Modeling 20: eight substantive layers for every major KU.
    layer_total = max(1, len(majors) * len(LAYER_FIELDS))
    layer_good = sum(substantive(ku.get(field), 12) for ku in majors for field in LAYER_FIELDS)
    layer_ratio = layer_good / layer_total
    note_ku_ratio = sum(
        ku_id in ku_blocks and len(ku_blocks[ku_id]) >= 120 for ku_id in major_ids
    ) / max(1, len(major_ids))
    modeling_score = round(14 * layer_ratio + 6 * note_ku_ratio)
    details['Knowledge Modeling'] = modeling_score
    if modeling_score < 16:
        blockers.append('KNOWLEDGE_MODELING_BELOW_16')

    # Relationships & Causality 15.
    rel_good = sum(substantive(ku.get('relationships'), 12) and substantive(ku.get('how'), 12) for ku in majors)
    relation_score = round(15 * rel_good / max(1, len(majors)))
    details['Relationships & Causality'] = relation_score

    # Retrieval Usefulness 15: deterministic retrieval anchors in the note.
    retrieval_checks = [
        bool(re.search(r'核心主軸|一句話核心', md, re.I)),
        bool(re.search(r'必背關鍵字|關鍵字', md, re.I)),
        bool(re.search(r'先翻順序|閱讀路徑|快速查', md, re.I)),
        bool(re.search(r'本章快速複習|最後速背|考前.*速背', md, re.I)),
        bool(re.search(r'Active Recall|Feynman', md, re.I)),
    ]
    retrieval_score = 3 * sum(retrieval_checks)
    details['Retrieval Usefulness'] = retrieval_score

    # Assessment 15: 20 total, 10 L1/L2 + 10 L3/L4, complete fields, all KUs known.
    known = {x.get('id') for x in kus}
    q_ids = [str(q.get('id', '')).strip() for q in qs if str(q.get('id', '')).strip()]
    if len(q_ids) != len(set(q_ids)):
        blockers.append('ASSESSMENT_DUPLICATE_ID')
    l12 = [q for q in qs if q.get('difficulty') in ('L1','L2')]
    l34 = [q for q in qs if q.get('difficulty') in ('L3','L4')]
    count_score = 5 if len(qs) >= 20 and len(l12) >= 10 and len(l34) >= 10 else round(5 * min(1, len(qs)/20) * min(1, (len(l12)+len(l34))/20))
    required = ['id','difficulty','knowledge_unit','expected_keywords','question','answer','source_locators']
    complete = 0
    for q in qs:
        ok = all(q.get(k) not in (None,'',[]) for k in required)
        ok = ok and q.get('knowledge_unit') in known and q.get('difficulty') in ('L1','L2','L3','L4')
        ok = ok and locator_ok_list(q.get('source_locators'), allow_synthetic)
        complete += bool(ok)
    field_score = round(5 * complete / max(1, len(qs)))
    levels_present = {q.get('difficulty') for q in qs}
    level_score = 5 if {'L1','L2','L3','L4'}.issubset(levels_present) else round(5 * len(levels_present & {'L1','L2','L3','L4'}) / 4)
    assessment_score = count_score + field_score + level_score
    details['Assessment Quality'] = assessment_score
    if len(l12) < 10 or len(l34) < 10:
        blockers.append('FORMAL_ASSESSMENT_MINIMUM_NOT_MET')

    # Pitfalls 10.
    pit_good = sum(substantive(ku.get('pitfalls'), 12) for ku in majors)
    pit_score = round(10 * pit_good / max(1, len(majors)))
    details['Pitfalls & Discrimination'] = pit_score

    # Compression 5: no placeholders + low exact paragraph duplication.
    dup_ratio = duplicate_paragraph_ratio(md)
    compression_score = 5 if not any(x == 'PLACEHOLDER_CONTENT_DETECTED' for x in blockers) and dup_ratio <= 0.10 else (3 if dup_ratio <= 0.20 else 0)
    details['Compression without Distortion'] = compression_score
    details['duplicate_paragraph_ratio'] = round(dup_ratio, 4)

    learner = audit_learner_facing(note_md)
    details['Learner-facing automatic status'] = learner['automatic_status']
    details['learner_facing_issues'] = learner['issues']
    details['manual_readability_sample_ku_ids'] = learner['details']['manual_readability_sample_ku_ids']
    blockers.extend(learner['issues'])

    computed, cov_issues = audit_coverage(coverage_yaml, knowledge_yaml)
    if cov_issues:
        blockers.append('COVERAGE_NOT_FULL_PASS')
    # Cross-check the visible Markdown Coverage Matrix against computed status.
    matrix_issues = []
    table_lines = [x.strip() for x in md.splitlines() if x.strip().startswith('|')]
    for row in computed:
        ku_id = str(row.get('knowledge_unit',''))
        matches = [x for x in table_lines if ku_id and ku_id in x]
        if not matches:
            matrix_issues.append(f'{ku_id}:MISSING_FROM_MD_MATRIX')
            continue
        cells = [c.strip() for c in matches[0].strip('|').split('|')]
        visible_status = cells[-1] if cells else ''
        if visible_status != row['computed_status']:
            matrix_issues.append(f"{ku_id}:VISIBLE_{visible_status}_COMPUTED_{row['computed_status']}")
    if matrix_issues:
        blockers.append('VISIBLE_COVERAGE_MATRIX_MISMATCH')
    details['coverage_rows'] = len(computed)
    details['coverage_issues'] = cov_issues
    details['coverage_matrix_issues'] = matrix_issues

    total = sum(v for k, v in details.items() if k in {
        'Source Fidelity','Knowledge Modeling','Relationships & Causality','Retrieval Usefulness',
        'Assessment Quality','Pitfalls & Discrimination','Compression without Distortion'
    })
    if blockers:
        status = 'FAIL'
    elif total >= 90:
        status = 'RELEASE_READY'
    elif total >= 80:
        status = 'PASS_WITH_MINOR_FIXES'
    elif total >= 70:
        status = 'REWORK_REQUIRED'
    else:
        status = 'FAIL'
    return {'score': total, 'status': status, 'blockers': sorted(set(blockers)), 'details': details}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('note_md')
    ap.add_argument('--knowledge', required=True)
    ap.add_argument('--assessment', required=True)
    ap.add_argument('--coverage', required=True)
    ap.add_argument('--allow-synthetic', action='store_true')
    ap.add_argument('--json-out')
    args = ap.parse_args()
    result = audit(args.note_md, args.knowledge, args.assessment, args.coverage, args.allow_synthetic)
    print(f"QUALITY_SCORE={result['score']}/100")
    for k, v in result['details'].items():
        if isinstance(v, (int, float)) and k not in ('duplicate_paragraph_ratio','coverage_rows'):
            print(f'{k.upper().replace(" ","_").replace("&","AND")}={v}')
    if result['blockers']:
        for x in result['blockers']:
            print('FAIL', x)
    print('QUALITY_STATUS=' + result['status'])
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return 0 if result['status'] == 'RELEASE_READY' else 2


if __name__ == '__main__':
    raise SystemExit(main())
