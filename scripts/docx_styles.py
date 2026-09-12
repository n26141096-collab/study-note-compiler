from docx.shared import Pt, Mm, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def _set_fonts(style_or_run, east_asia, latin):
    """Set East-Asian and Latin fonts independently for portable mixed text."""
    style_or_run.font.name = latin
    rpr = getattr(style_or_run._element, 'rPr', None)
    if rpr is None:
        rpr = style_or_run._element.get_or_add_rPr()
    rfonts = rpr.rFonts
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.insert(0, rfonts)
    rfonts.set(qn('w:eastAsia'), east_asia)
    rfonts.set(qn('w:ascii'), latin)
    rfonts.set(qn('w:hAnsi'), latin)
    rfonts.set(qn('w:cs'), latin)


def set_cell_shading(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn('w:shd'))
    if shd is None:
        shd = OxmlElement('w:shd')
        tcPr.append(shd)
    shd.set(qn('w:fill'), fill)


def set_paragraph_shading(paragraph, fill):
    pPr = paragraph._p.get_or_add_pPr()
    shd = pPr.find(qn('w:shd'))
    if shd is None:
        shd = OxmlElement('w:shd')
        pPr.append(shd)
    shd.set(qn('w:fill'), fill)


def apply_base_styles(doc, cfg):
    styles = doc.styles
    body_font = cfg['fonts']['body']
    heading_font = cfg['fonts']['heading']
    latin_font = cfg['fonts']['latin']

    normal = styles['Normal']
    _set_fonts(normal, body_font, latin_font)
    normal.font.size = Pt(cfg['styles']['body']['size_pt'])
    normal.paragraph_format.space_after = Pt(cfg['styles']['body']['space_after_pt'])
    normal.paragraph_format.line_spacing = cfg['styles']['body']['line_spacing']
    normal.paragraph_format.widow_control = True

    for sname, key in [('Title', 'title'), ('Heading 1', 'heading1'), ('Heading 2', 'heading2'), ('Heading 3', 'heading3')]:
        style = styles[sname]
        spec = cfg['styles'][key]
        _set_fonts(style, heading_font, latin_font)
        style.font.size = Pt(spec['size_pt'])
        style.font.bold = spec.get('bold', False)
        style.font.color.rgb = RGBColor(0, 0, 0)
        rpr = style._element.get_or_add_rPr()
        color = rpr.find(qn('w:color'))
        if color is None:
            color = OxmlElement('w:color'); rpr.append(color)
        color.set(qn('w:val'), '000000')
        for attr in (qn('w:themeColor'), qn('w:themeShade'), qn('w:themeTint')):
            if attr in color.attrib:
                del color.attrib[attr]
        ppr = style._element.get_or_add_pPr()
        pbdr = ppr.find(qn('w:pBdr'))
        if pbdr is not None:
            ppr.remove(pbdr)
        style.paragraph_format.space_before = Pt(spec.get('space_before_pt', 0))
        style.paragraph_format.space_after = Pt(spec.get('space_after_pt', 0))
        style.paragraph_format.keep_with_next = spec.get('keep_with_next', False)
        style.paragraph_format.widow_control = True

    custom = {
        'Meta': ('meta', False),
        'KeySentence': ('body', True),
        'Question': ('question', True),
        'Answer': ('answer', False),
        'Compact': ('body', False),
    }
    for name, (key, bold) in custom.items():
        if name not in styles:
            styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        st = styles[name]
        spec = cfg['styles'].get(key, cfg['styles']['body'])
        east = heading_font if name == 'Question' else body_font
        _set_fonts(st, east, latin_font)
        st.font.size = Pt(spec['size_pt'])
        st.font.bold = bold or spec.get('bold', False)
        st.font.color.rgb = RGBColor(0, 0, 0)
        st.paragraph_format.space_after = Pt(spec.get('space_after_pt', 0.5))
        st.paragraph_format.line_spacing = cfg['styles']['body']['line_spacing']
        st.paragraph_format.widow_control = True
    styles['Answer'].paragraph_format.left_indent = Mm(cfg['styles']['answer']['left_indent_mm'])
