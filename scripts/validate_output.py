#!/usr/bin/env python3
import argparse
import re
import zipfile
from pathlib import Path
from lxml import etree

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
A4_W_TWIPS = 11906  # 210 mm, rounded in OOXML
A4_H_TWIPS = 16838  # 297 mm, rounded in OOXML


def page_size_stats(xml):
    sizes = []
    for sect in xml.xpath('//w:sectPr', namespaces=NS):
        pgsz = sect.find('{%s}pgSz' % NS['w'])
        if pgsz is None:
            sizes.append((None, None))
        else:
            sizes.append((int(pgsz.get('{%s}w' % NS['w'], '0')), int(pgsz.get('{%s}h' % NS['w'], '0'))))
    return sizes


def is_a4(size, tol=4):
    w, h = size
    return w is not None and abs(w - A4_W_TWIPS) <= tol and abs(h - A4_H_TWIPS) <= tol


def validate(md_path, docx_path, profile='topic'):
    md = Path(md_path).read_text(encoding='utf-8')
    issues = []
    if profile == 'topic':
        if '<!-- columns: 2 -->' not in md:
            issues.append('MARKDOWN_TWO_COLUMN_MARKER_MISSING')
        if '<!-- columns: 1 -->' not in md:
            issues.append('MARKDOWN_FULL_WIDTH_MARKER_MISSING')
        if 'Coverage Matrix' not in md:
            issues.append('COVERAGE_MATRIX_MISSING')
        if not re.search(r'核心主軸|一句話核心', md, flags=re.I):
            issues.append('PROFESSIONAL_NOTE_CORE_LAYER_MISSING')
    elif profile == 'master_index':
        for label, pat in [
            ('KEYWORD_LOOKUP', r'關鍵字.*查|快速查找'),
            ('ROUTE', r'申論|面試|答題.*路線|建議順序'),
            ('CONFUSION', r'易混淆'),
            ('CRAM', r'最後速背|速背'),
            ('SOURCE_MAP', r'來源對照|主題與來源'),
        ]:
            if not re.search(pat, md, flags=re.I):
                issues.append(f'MASTER_INDEX_{label}_MISSING')
        if '<!-- columns: 1 -->' not in md:
            issues.append('MASTER_INDEX_FULL_WIDTH_MARKER_MISSING')
    else:
        raise ValueError('profile must be topic or master_index')

    p = Path(docx_path)
    if not p.exists() or p.stat().st_size < 2000:
        issues.append('DOCX_INVALID_OR_TOO_SMALL')
        return issues, {}

    stats = {'sections': 0, 'two_column_sections': 0, 'one_column_sections': 0, 'tables': 0, 'a4_sections': 0, 'non_a4_sections': 0}
    with zipfile.ZipFile(p) as z:
        xml = etree.fromstring(z.read('word/document.xml'))
        sects = xml.xpath('//w:sectPr', namespaces=NS)
        stats['sections'] = len(sects)
        sizes = page_size_stats(xml)
        for sect in sects:
            cols = sect.find('{%s}cols' % NS['w'])
            num = int(cols.get('{%s}num' % NS['w'], '1')) if cols is not None else 1
            if num == 2:
                stats['two_column_sections'] += 1
            elif num == 1:
                stats['one_column_sections'] += 1
        stats['tables'] = len(xml.xpath('//w:tbl', namespaces=NS))
        stats['a4_sections'] = sum(is_a4(x) for x in sizes)
        stats['non_a4_sections'] = len(sizes) - stats['a4_sections']

    if stats['non_a4_sections']:
        issues.append('WORD_A4_PAGE_SIZE_GATE_FAIL')
    if profile == 'topic':
        if stats['two_column_sections'] < 1:
            issues.append('WORD_REAL_TWO_COLUMN_SECTION_MISSING')
        if stats['one_column_sections'] < 1:
            issues.append('WORD_ONE_COLUMN_SECTION_MISSING')
    else:
        if stats['one_column_sections'] < 1:
            issues.append('MASTER_INDEX_ONE_COLUMN_SECTION_MISSING')
        if stats['tables'] < 2:
            issues.append('MASTER_INDEX_TABLE_STRUCTURE_TOO_THIN')
    return issues, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('md')
    ap.add_argument('docx')
    ap.add_argument('--profile', choices=['topic','master_index'], default='topic')
    args = ap.parse_args()
    issues, stats = validate(args.md, args.docx, args.profile)
    for k, v in stats.items():
        print(f'{k.upper()}={v}')
    if issues:
        for x in issues:
            print('FAIL', x)
        return 2
    print('PASS MD_GATE')
    print('PASS DOCX_GATE')
    print('PASS WORD_A4_PAGE_SIZE_GATE')
    if args.profile == 'topic':
        print('PASS WORD_REAL_TWO_COLUMN_GATE')
        print('PASS WORD_MIXED_LAYOUT_STRUCTURE_GATE')
    else:
        print('PASS MASTER_INDEX_GATE')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
