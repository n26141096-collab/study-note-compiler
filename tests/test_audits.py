from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from coverage_audit import audit as audit_coverage
from note_quality_audit import audit as audit_note
from source_locator_audit import audit_file
from audit_release_manifest import audit as audit_manifest, sha256
from learner_facing_audit import audit as audit_learner_facing
import json


def test_false_manual_coverage_pass_is_rejected(tmp_path):
    p = tmp_path/'bad.yaml'
    p.write_text(yaml.safe_dump({'coverage':[{
        'knowledge_unit':'KU_BAD','source':False,'note':False,'l1_l2':False,'l3_l4':False,'pitfall':False,'status':'PASS'
    }]}), encoding='utf-8')
    _, issues = audit_coverage(p)
    assert any('HAND_ENTERED_STATUS_FORBIDDEN' in x for x in issues)


def test_computed_coverage_passes_fixture():
    computed, issues = audit_coverage(
        ROOT/'examples/sample_coverage.yaml',
        ROOT/'examples/sample_knowledge_units.yaml',
    )
    assert issues == []
    assert all(x['computed_status']=='PASS' for x in computed)


def test_coverage_rejects_missing_known_kus(tmp_path):
    p = tmp_path/'partial.yaml'
    p.write_text(yaml.safe_dump({'coverage':[{
        'knowledge_unit':'KU_PROBLEM','source':True,'note':True,'l1_l2':True,'l3_l4':True,'pitfall':True
    }]}), encoding='utf-8')
    _, issues = audit_coverage(p, ROOT/'examples/sample_knowledge_units.yaml')
    assert any('MISSING_COVERAGE_KU:KU_COMMONALITY' in x for x in issues)


def test_keyword_only_fake_note_fails_quality_gate(tmp_path):
    fake = tmp_path/'fake.md'
    fake.write_text('核心主軸 必背關鍵字 先翻順序 最後速背 What Why 因果 Pitfall L1 L2 L3 L4 Active Recall Feynman Coverage Matrix', encoding='utf-8')
    # Good sidecars cannot make a keyword shell into a release-ready note.
    result = audit_note(fake, ROOT/'examples/sample_knowledge_units.yaml', ROOT/'examples/sample_assessment.yaml', ROOT/'examples/sample_coverage.yaml', True)
    assert result['status'] == 'FAIL'
    assert 'NOTE_KU_COVERAGE_INCOMPLETE' in result['blockers']


def test_sample_note_reaches_release_ready():
    result = audit_note(ROOT/'examples/sample_topic.md', ROOT/'examples/sample_knowledge_units.yaml', ROOT/'examples/sample_assessment.yaml', ROOT/'examples/sample_coverage.yaml', True)
    assert result['status'] == 'RELEASE_READY'
    assert result['score'] >= 90
    assert result['details']['Source Fidelity'] >= 16
    assert result['details']['Knowledge Modeling'] >= 16


def test_synthetic_locator_rejected_by_default_and_allowed_for_fixture():
    issues, _ = audit_file(ROOT/'examples/sample_knowledge_units.yaml', allow_synthetic=False)
    assert any('SYNTHETIC_SOURCE_NOT_ALLOWED_IN_FORMAL_RELEASE' in x for x in issues)
    issues2, _ = audit_file(ROOT/'examples/sample_knowledge_units.yaml', allow_synthetic=True)
    assert issues2 == []


def test_missing_locator_on_one_major_ku_is_rejected(tmp_path):
    p = tmp_path/'knowledge.yaml'
    good = {
        'file':'source.pdf','locator_type':'page','locator':'1',
        'evidence':'足夠長度的來源證據說明文字','confidence':'HIGH'
    }
    p.write_text(yaml.safe_dump({'knowledge_units':[
        {'id':'KU_OK','importance':'critical','source_locators':[good]},
        {'id':'KU_MISSING','importance':'high','source_locators':[]},
    ]}, allow_unicode=True), encoding='utf-8')
    issues, _ = audit_file(p)
    assert 'KU:KU_MISSING:MISSING_SOURCE_LOCATORS' in issues


def test_release_manifest_rejects_unlisted_files(tmp_path):
    data = tmp_path/'a.txt'
    data.write_text('release data', encoding='utf-8')
    skill = tmp_path/'SKILL.md'
    skill.write_text('---\nname: fixture\ndescription: fixture\nmetadata:\n  version: "2.1.1"\n---\n', encoding='utf-8')
    manifest = tmp_path/'manifest.txt'
    manifest.write_text('RELEASE_MANIFEST.json\nSKILL.md\na.txt\nmanifest.txt\n', encoding='utf-8')
    payload = {
        'format': 1,
        'release': f'{tmp_path.name}-v2.1.1',
        'version': '2.1.1',
        'self_omitted_from_hash_entries': True,
        'manifest_path': 'manifest.txt',
        'entries': [
            {'path':'SKILL.md','size':skill.stat().st_size,'sha256':sha256(skill)},
            {'path':'a.txt','size':data.stat().st_size,'sha256':sha256(data)},
            {'path':'manifest.txt','size':manifest.stat().st_size,'sha256':sha256(manifest)},
        ],
    }
    (tmp_path/'RELEASE_MANIFEST.json').write_text(json.dumps(payload), encoding='utf-8')
    (tmp_path/'unexpected.bin').write_bytes(b'not listed')
    issues, _ = audit_manifest(tmp_path)
    assert 'UNLISTED_FILE:unexpected.bin' in issues


def test_sample_note_passes_automatic_learner_facing_gates():
    result = audit_learner_facing(ROOT/'examples/sample_topic.md')
    assert result['automatic_status'] == 'PASS'
    assert result['issues'] == []
    assert len(result['details']['manual_readability_sample_ku_ids']) == 3


def test_template_dump_and_raw_locator_are_rejected(tmp_path):
    bad = tmp_path/'bad_reader_note.md'
    repeated = '''
**What**：這是固定欄位。
**Why**：是本教材用來連結製程步驟、結構轉換與可量測結果的知識單元。
**How**：這是固定欄位。
**Application**：這是固定欄位。
**Pitfall**：這是固定欄位。
來源定位：course.zip::static_resources/9878a7acdd9632caa5afb8b4b96a6f39_lecture2.pdf p.20
'''
    md = '<!-- columns: 2 -->\n# bad\n## A｜專業重點筆記\n'
    for ku in ('KU_A','KU_B','KU_C'):
        md += f'<!-- ku: {ku} -->\n### {ku}\n{repeated}\n'
    md += '''
## B｜L1–L2 基礎題
## C｜L3–L4 情境題
01_Q11（L3）FAB 出現與「A」相符的症狀時，應如何開始拆解？
01_Q12（L3）FAB 出現與「B」相符的症狀時，應如何開始拆解？
01_Q13（L3）FAB 出現與「C」相符的症狀時，應如何開始拆解？
## D｜Active Recall
'''
    bad.write_text(md, encoding='utf-8')
    result = audit_learner_facing(bad)
    assert result['automatic_status'] == 'FAIL'
    assert 'TEMPLATE_VISIBLE_LABEL_GRID' in result['issues']
    assert 'TEMPLATE_REPEATED_LONG_SENTENCE' in result['issues']
    assert 'TEMPLATE_REPEATED_QUESTION_STEM' in result['issues']
    assert 'LEARNER_FACING_RAW_ARCHIVE_LOCATOR' in result['issues']
