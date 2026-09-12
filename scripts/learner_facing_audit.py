#!/usr/bin/env python3
"""Mechanical learner-facing checks for Study Note Compiler v2.3.0.

This catches template dumping, repeated meta prose, cloned question stems, and raw
archive locators in the reading layer. It does not replace the required manual
read-aloud READABILITY_GATE.
"""
import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


KU_MARKER_RE = re.compile(r'<!--\s*ku:\s*([A-Za-z0-9_.-]+)\s*-->', re.I)
VISIBLE_LABEL_RE = re.compile(
    r'^\s*(?:[-*]\s*)?(?:\*\*)?'
    r'(?:What|Why|How|Relationships?|Application|Pitfalls?|Recall|Active Recall|'
    r'PE\s*/\s*PI\s*Application|工程關係鏈|工程關係|一句話核心)'
    r'(?:\*\*)?\s*[:：]',
    re.I,
)
RAW_LOCATOR_PATTERNS = [
    re.compile(r'\.zip::', re.I),
    re.compile(r'(?:static_resources|static-resources|static_resources\\|static-resources\\)[/\\]', re.I),
    re.compile(r'\b[0-9a-f]{20,}_[^\s/\\]+\.pdf\b', re.I),
]


def extract_ku_blocks(md):
    assessment = re.search(r'^##\s+B(?:｜|\||\s)', md, flags=re.M | re.I)
    note_end = assessment.start() if assessment else len(md)
    matches = list(KU_MARKER_RE.finditer(md[:note_end]))
    blocks = []
    for idx, match in enumerate(matches):
        end = matches[idx + 1].start() if idx + 1 < len(matches) else note_end
        blocks.append((match.group(1), md[match.end():end]))
    return blocks


def clean_sentence(text):
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.S)
    text = re.sub(r'[`*_>#|]', ' ', text)
    text = re.sub(r'^\s*(?:What|Why|How|Relationships?|Application|Pitfalls?|Recall|'
                  r'Active Recall|PE\s*/\s*PI\s*Application|工程關係鏈|工程關係)\s*[:：]\s*',
                  '', text, flags=re.I)
    # Normalize the demonstrated cross-topic filler while preserving substantive sentences.
    text = re.sub(r'^.*?是本教材用來', '是本教材用來', text)
    return re.sub(r'\s+', ' ', text).strip().lower()


def repeated_long_sentences(blocks):
    owners = defaultdict(set)
    originals = {}
    for ku_id, block in blocks:
        for sentence in re.split(r'[。！？!?]\s*', block):
            normalized = clean_sentence(sentence)
            if len(normalized) < 30:
                continue
            owners[normalized].add(ku_id)
            originals.setdefault(normalized, re.sub(r'\s+', ' ', sentence).strip())
    return [
        {'sentence': originals[s], 'knowledge_units': sorted(ids)}
        for s, ids in owners.items() if len(ids) >= 2
    ]


def question_shapes(md):
    start = re.search(r'^##\s+C(?:｜|\||\s)', md, flags=re.M | re.I)
    if not start:
        return [], {}
    end = re.search(r'^##\s+D(?:｜|\||\s)', md[start.end():], flags=re.M | re.I)
    section = md[start.end():start.end() + end.start()] if end else md[start.end():]
    shapes = []
    for raw in section.splitlines():
        line = raw.strip()
        if not line or re.match(r'^(?:答|answer)\s*[:：]', line, re.I):
            continue
        if not (re.search(r'(?:^|[_-])Q\d+\b', line, re.I) or re.match(r'^(?:題目\s*)?\d+\s*[.、:：]', line)):
            continue
        norm = re.sub(r'\b[A-Za-z0-9_-]*Q\d+\b\s*(?:\([^)]*\))?', 'Q', line, flags=re.I)
        norm = re.sub(r'^(?:題目\s*)?\d+\s*[.、:：]?', 'Q ', norm)
        norm = re.sub(r'[「『][^」』]+[」』]', '「KU」', norm)
        norm = re.sub(r'"[^"]+"', '「KU」', norm)
        norm = re.sub(r'\s+', ' ', norm).strip().lower()
        shapes.append(norm)
    counts = Counter(shapes)
    repeated = {shape: count for shape, count in counts.items() if count >= 3}
    return shapes, repeated


def audit(note_md):
    md = Path(note_md).read_text(encoding='utf-8')
    blocks = extract_ku_blocks(md)
    issues = []
    details = {}

    if not blocks:
        issues.append('LEARNER_FACING_NO_KU_MARKERS')

    label_counts = {}
    label_grid_blocks = []
    for ku_id, block in blocks:
        count = sum(bool(VISIBLE_LABEL_RE.match(line)) for line in block.splitlines())
        label_counts[ku_id] = count
        if count >= 4:
            label_grid_blocks.append(ku_id)
    label_grid_ratio = len(label_grid_blocks) / max(1, len(blocks))
    if label_grid_ratio >= 0.5:
        issues.append('TEMPLATE_VISIBLE_LABEL_GRID')

    repeated_sentences = repeated_long_sentences(blocks)
    if repeated_sentences:
        issues.append('TEMPLATE_REPEATED_LONG_SENTENCE')

    shapes, repeated_shapes = question_shapes(md)
    repeated_question_count = max(repeated_shapes.values(), default=0)
    repeated_question_ratio = repeated_question_count / max(1, len(shapes))
    if repeated_question_count >= 3 and repeated_question_ratio >= 0.25:
        issues.append('TEMPLATE_REPEATED_QUESTION_STEM')

    raw_locator_hits = []
    for pattern in RAW_LOCATOR_PATTERNS:
        raw_locator_hits.extend(sorted(set(pattern.findall(md))))
    if raw_locator_hits:
        issues.append('LEARNER_FACING_RAW_ARCHIVE_LOCATOR')

    ku_ids = [ku_id for ku_id, _ in blocks]
    if len(ku_ids) <= 3:
        sample = ku_ids
    elif ku_ids:
        sample = [ku_ids[0], ku_ids[len(ku_ids) // 2], ku_ids[-1]]
    else:
        sample = []

    details.update({
        'knowledge_unit_blocks': len(blocks),
        'visible_label_counts': label_counts,
        'label_grid_blocks': label_grid_blocks,
        'label_grid_ratio': round(label_grid_ratio, 4),
        'repeated_long_sentences': repeated_sentences,
        'question_count_detected': len(shapes),
        'repeated_question_shapes': repeated_shapes,
        'repeated_question_ratio': round(repeated_question_ratio, 4),
        'raw_locator_hit_count': len(raw_locator_hits),
        'manual_readability_sample_ku_ids': sample,
    })
    return {
        'automatic_status': 'PASS' if not issues else 'FAIL',
        'issues': sorted(set(issues)),
        'details': details,
        'manual_readability_gate': 'REQUIRED',
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('note_md')
    ap.add_argument('--json-out')
    args = ap.parse_args()
    result = audit(args.note_md)
    if result['issues']:
        for issue in result['issues']:
            print('FAIL', issue)
    else:
        print('PASS TEMPLATE_REPETITION_GATE')
        print('PASS LEARNER_FACING_GATE')
    sample = ','.join(result['details']['manual_readability_sample_ku_ids'])
    print(f'MANUAL_READABILITY_SAMPLE={sample}')
    print('READABILITY_GATE=MANUAL_REVIEW_REQUIRED')
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0 if not result['issues'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
