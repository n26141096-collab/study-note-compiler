from pathlib import Path
import sys
import zipfile
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from md_to_docx import build
from validate_output import validate

NS = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def _sizes(xml):
    vals=[]
    for sect in xml.xpath('//w:sectPr', namespaces=NS):
        pgsz=sect.find('{%s}pgSz' % NS['w'])
        vals.append((int(pgsz.get('{%s}w' % NS['w'])), int(pgsz.get('{%s}h' % NS['w']))))
    return vals


def test_renderer_creates_real_two_column_full_width_and_a4(tmp_path):
    md = (ROOT / 'examples' / 'sample_topic.md').read_text(encoding='utf-8')
    out = tmp_path / 'sample.docx'
    build(md, out, course='QA')
    with zipfile.ZipFile(out) as z:
        document_xml = z.read('word/document.xml')
        xml = etree.fromstring(document_xml)
    assert b'ku:' not in document_xml
    nums = []
    for sect in xml.xpath('//w:sectPr', namespaces=NS):
        cols = sect.find('{%s}cols' % NS['w'])
        nums.append(int(cols.get('{%s}num' % NS['w'], '1')) if cols is not None else 1)
    assert 2 in nums and 1 in nums
    for w,h in _sizes(xml):
        assert abs(w - 11906) <= 4
        assert abs(h - 16838) <= 4
    issues, stats = validate(ROOT/'examples/sample_topic.md', out, 'topic')
    assert issues == []
    assert stats['a4_sections'] == stats['sections']


def test_renderer_two_panel_master_index_a4(tmp_path):
    md = (ROOT / 'examples' / 'sample_master_index.md').read_text(encoding='utf-8')
    out = tmp_path / 'index.docx'
    build(md, out, course='Study')
    issues, stats = validate(ROOT/'examples/sample_master_index.md', out, 'master_index')
    assert issues == []
    assert stats['tables'] >= 3
    assert stats['a4_sections'] == stats['sections']
    with zipfile.ZipFile(out) as z:
        xml = etree.fromstring(z.read('word/document.xml'))
    fixed_tables = xml.xpath('//w:tbl[w:tblPr/w:tblLayout[@w:type="fixed"]]', namespaces=NS)
    assert len(fixed_tables) == 1
    grid_widths = [
        int(node.get('{%s}w' % NS['w']))
        for node in fixed_tables[0].xpath('./w:tblGrid/w:gridCol', namespaces=NS)
    ]
    assert len(grid_widths) == 2
    assert abs(grid_widths[0] - grid_widths[1]) <= 1
    assert sum(grid_widths) > 10000
