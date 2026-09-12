from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_schema_version_and_source_locators():
    s = yaml.safe_load((ROOT / 'config' / 'note_schema.yaml').read_text(encoding='utf-8'))
    assert s['version'] == '2.3.0'
    assert 'source_locators' in s['knowledge_unit']['required']
    assert s['coverage_matrix']['forbid_hand_entered_status'] is True
    assert s['assessment']['formal_topic_minimum']['total'] == 20
    assert s['eight_layer_model']['sidecar_complete_but_not_visible_template'] is True


def test_word_layout_a4_and_columns_required():
    c = yaml.safe_load((ROOT / 'config' / 'word_layout.yaml').read_text(encoding='utf-8'))
    assert c['page']['size'] == 'A4'
    assert c['page']['width_mm'] == 210
    assert c['page']['height_mm'] == 297
    assert c['columns']['default_topic_columns'] == 2
    assert c['visual_rules']['require_a4_physical_page_size'] is True
    assert c['visual_rules']['require_real_two_column_section'] is True


def test_source_governance_no_silent_fill():
    c = yaml.safe_load((ROOT / 'config' / 'content_rules.yaml').read_text(encoding='utf-8'))
    assert c['source_governance']['forbid_silent_model_fill'] is True
    assert c['source_governance']['require_structured_source_locator_for_major_units'] is True
    assert c['coverage']['status_must_be_computed'] is True
    assert c['learner_facing']['forbid_visible_eight_layer_dump'] is True
    assert c['learner_facing']['require_read_aloud_review'] is True
    assert c['learner_facing']['readable_revision_preserve_governance_hashes'] is True
    assert len(c['learner_facing']['readable_revision_audit_dimensions']) == 12
    assert c['learner_facing']['readable_release_pass_min'] == 85
    assert c['profiles']['engineering']['optional'] is True
