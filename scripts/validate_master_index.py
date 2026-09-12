#!/usr/bin/env python3
import argparse
from validate_output import validate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('md')
    ap.add_argument('docx')
    args = ap.parse_args()
    issues, stats = validate(args.md, args.docx, 'master_index')
    for k, v in stats.items():
        print(f'{k.upper()}={v}')
    if issues:
        for x in issues:
            print('FAIL', x)
        return 2
    print('PASS MASTER_INDEX_GATE')
    print('PASS WORD_A4_PAGE_SIZE_GATE')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
