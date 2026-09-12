#!/usr/bin/env python3
"""Render DOCX to PDF and per-page PNGs with explicit external dependencies."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def find_executable(explicit, names, candidates=()):
    if explicit:
        path = Path(explicit)
        if path.is_file():
            return str(path)
        raise FileNotFoundError(f'EXPLICIT_EXECUTABLE_NOT_FOUND:{path}')
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    for candidate in candidates:
        path = Path(candidate)
        if path.is_file():
            return str(path)
    return None


def ps_quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def render_pdf_with_word(source, pdf):
    powershell = find_executable(None, ('pwsh', 'powershell'))
    if os.name != 'nt' or not powershell:
        return None
    command = f"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {{
  $doc = $word.Documents.Open({ps_quote(source)})
  $doc.ExportAsFixedFormat({ps_quote(pdf)}, 17)
  $doc.Close($false)
}} finally {{
  if ($doc) {{ [void][Runtime.InteropServices.Marshal]::ReleaseComObject($doc) }}
  $word.Quit()
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($word)
}}
"""
    subprocess.run(
        [powershell, '-NoProfile', '-NonInteractive', '-Command', command],
        check=True,
        capture_output=True,
        text=True,
    )
    return 'Microsoft Word COM via PowerShell'


def render(docx, out_dir, soffice=None, pdftoppm=None, dpi=150):
    source = Path(docx).resolve()
    if not source.is_file() or source.suffix.lower() != '.docx':
        raise ValueError(f'DOCX_NOT_FOUND:{source}')
    output = Path(out_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)

    office = find_executable(
        soffice,
        ('soffice', 'libreoffice'),
        (
            r'C:\Program Files\LibreOffice\program\soffice.exe',
            r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',
        ),
    )
    poppler = find_executable(pdftoppm, ('pdftoppm',))
    if not poppler:
        raise RuntimeError('PDFTOPPM_NOT_FOUND')

    pdf = output / f'{source.stem}.pdf'
    if pdf.exists():
        pdf.unlink()
    for stale_page in output.glob('page-*.png'):
        stale_page.unlink()
    if office:
        subprocess.run(
            [office, '--headless', '--convert-to', 'pdf', '--outdir', str(output), str(source)],
            check=True,
            capture_output=True,
            text=True,
        )
        renderer = office
    else:
        renderer = render_pdf_with_word(source, pdf)
        if not renderer:
            raise RuntimeError('OFFICE_RENDERER_NOT_FOUND')
    if not pdf.is_file():
        raise RuntimeError('PDF_RENDER_NOT_CREATED')

    prefix = output / 'page'
    subprocess.run(
        [poppler, '-png', '-r', str(int(dpi)), str(pdf), str(prefix)],
        check=True,
        capture_output=True,
        text=True,
    )
    pages = sorted(output.glob('page-*.png'))
    if not pages:
        raise RuntimeError('PNG_PAGES_NOT_CREATED')
    report = {
        'input': str(source),
        'input_sha256': sha256(source),
        'pdf': str(pdf),
        'pdf_sha256': sha256(pdf),
        'dpi': int(dpi),
        'pages': [str(x) for x in pages],
        'page_count': len(pages),
        'renderer': renderer,
        'rasterizer': poppler,
        'visual_inspection_required': True,
    }
    report_path = output / 'render_report.json'
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def main():
    ap = argparse.ArgumentParser(description='Render DOCX to PDF and one PNG per page.')
    ap.add_argument('docx')
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--soffice')
    ap.add_argument('--pdftoppm')
    ap.add_argument('--dpi', type=int, default=150)
    args = ap.parse_args()
    try:
        report = render(args.docx, args.out_dir, args.soffice, args.pdftoppm, args.dpi)
    except Exception as exc:
        print('FAIL RENDER_GATE', exc)
        return 2
    print(f"RENDERED_PAGES={report['page_count']}")
    print('PASS RENDER_GATE')
    print('VISUAL_GATE=PENDING_MANUAL_PAGE_INSPECTION')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
