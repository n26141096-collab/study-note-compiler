from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_public_interface_and_mit_license():
    interface = yaml.safe_load((ROOT / 'agents' / 'openai.yaml').read_text(encoding='utf-8'))
    assert interface['interface']['display_name'] == 'Study Note Compiler'
    assert '$study-note-compiler' in interface['interface']['default_prompt']

    license_text = (ROOT / 'LICENSE').read_text(encoding='utf-8')
    assert 'MIT License' in license_text
    assert 'Copyright (c) 2026 JYUN' in license_text


def test_v23_readable_revision_resources_exist():
    for relative in (
        'references/readable_revision.md',
        'references/engineering_learning_profile.md',
        'templates/readable_revision_report.md',
    ):
        assert (ROOT / relative).is_file(), relative

