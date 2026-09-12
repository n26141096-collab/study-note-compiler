#!/usr/bin/env python3
"""Create a deterministic build scaffold.

Source reading and semantic knowledge modeling are performed by the source-aware
agent/reviewer. This helper only creates the canonical files and never summarizes
materials with hidden heuristics.
"""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    out = Path(args.out)
    for sub in ['drafts', 'models', 'coverage', 'audits', 'docx']:
        (out / sub).mkdir(parents=True, exist_ok=True)
    copies = [
        (ROOT/'templates/topic_note.md', out/'drafts/_topic_template.md'),
        (ROOT/'templates/master_index.md', out/'drafts/_master_index_template.md'),
        (ROOT/'templates/knowledge_units.yaml', out/'models/knowledge_units.yaml'),
        (ROOT/'templates/assessment.yaml', out/'models/assessment.yaml'),
        (ROOT/'templates/coverage.yaml', out/'coverage/coverage.yaml'),
        (ROOT/'config/note_schema.yaml', out/'note_schema.yaml'),
        (ROOT/'config/content_rules.yaml', out/'content_rules.yaml'),
        (ROOT/'config/word_layout.yaml', out/'word_layout.yaml'),
    ]
    for src, dst in copies:
        shutil.copy2(src, dst)
    print(f'BUILD_SCAFFOLD_READY={out}')


if __name__ == '__main__':
    main()
