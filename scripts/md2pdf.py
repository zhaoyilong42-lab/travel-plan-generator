#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md2pdf.py — 跨平台 Markdown 旅行攻略 → (Markdown + PDF) 导出工具

读取一份 Markdown 攻略，同时产出：
  - 一份 .md 文档（原文，便于再编辑 / 分享）
  - 一份 .pdf 文档（用 reportlab 渲染，中文正确显示）

字体自动探测（无需写死路径）：
  - Windows : 微软雅黑 msyh.ttc / msyhbd.ttc、SimSun、SimHei
  - macOS   : 苹方 PingFang.ttc、Arial Unicode
  - Linux   : Noto Sans CJK、文泉驿 wqy

用法：
  python md2pdf.py 路线.md
  python md2pdf.py 路线.md --out out_dir/
  python md2pdf.py 路线.md --out 路线.pdf
  python md2pdf.py 路线.md --font /path/to/font.ttc

依赖：pip install reportlab
"""
import re, os, sys, argparse

# ---------------------------------------------------------------------------
# 1) 依赖检查
# ---------------------------------------------------------------------------
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                    TableStyle, HRFlowable, KeepTogether)
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
except ImportError:
    sys.stderr.write(
        "❌ 缺少依赖 reportlab。请先安装：\n"
        "    pip install reportlab\n"
        "（Windows 用户可用 WorkBuddy 自带 python 的 venv；其余系统 pip 安装即可）\n")
    sys.exit(1)


# ---------------------------------------------------------------------------
# 2) 跨平台中文字体探测
# ---------------------------------------------------------------------------
def find_cjk_font():
    """返回找到的第一个中文字体文件路径，找不到返回 None。"""
    candidates = []

    if os.name == 'nt':
        windir = os.environ.get('SystemRoot', 'C:/Windows')
        fdir = os.path.join(windir, 'Fonts')
        candidates += [
            os.path.join(fdir, 'msyh.ttc'),
            os.path.join(fdir, 'msyh.ttf'),
            os.path.join(fdir, 'msyhbd.ttc'),
            os.path.join(fdir, 'simsun.ttc'),
            os.path.join(fdir, 'simhei.ttf'),
            os.path.join(fdir, 'yahei.ttf'),
        ]
    # macOS
    candidates += [
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
        '/Library/Fonts/Arial Unicode.ttf',
    ]
    # Linux
    candidates += [
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
    ]
    for c in candidates:
        if os.path.exists(c):
            return c

    # 没命中硬编码列表 → 扫描常见字体目录，按文件名关键字匹配
    search_dirs = []
    if os.name == 'nt':
        search_dirs.append(os.path.join(os.environ.get('SystemRoot', 'C:/Windows'), 'Fonts'))
    else:
        search_dirs += ['/usr/share/fonts', '/Library/Fonts',
                        os.path.expanduser('~/Library/Fonts'),
                        os.path.expanduser('~/.fonts'),
                        os.path.expanduser('~/.local/share/fonts')]
    keys = ('noto', 'wqy', 'pingfang', 'hei', 'song', 'ming', 'cjk',
            'yahei', 'simsun', 'arphic', 'fireflysung', 'sourcehan')
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        for root, _, files in os.walk(d):
            for f in files:
                low = f.lower()
                if low.endswith(('.ttc', '.ttf', '.otf')) and any(k in low for k in keys):
                    return os.path.join(root, f)
    return None


def find_bold_font(reg):
    """在同一目录里找一个粗体变体（文件名含 bold/bd/heavy/black）。"""
    if not reg:
        return None
    d = os.path.dirname(reg)
    ext = os.path.splitext(reg)[1]
    base = os.path.splitext(os.path.basename(reg))[0].lower()
    try:
        for f in os.listdir(d):
            fl = f.lower()
            if fl.endswith(ext) and ('bold' in fl or 'bd' in fl or 'heavy' in fl or 'black' in fl):
                if os.path.splitext(f)[0].lower() != base:
                    return os.path.join(d, f)
    except OSError:
        pass
    return None


def register_fonts(regular, bold=None):
    if not regular or not os.path.exists(regular):
        return False
    pdfmetrics.registerFont(TTFont('CJK', regular, subfontIndex=0))
    if bold and os.path.exists(bold):
        pdfmetrics.registerFont(TTFont('CJK-Bold', bold, subfontIndex=0))
    else:
        pdfmetrics.registerFont(TTFont('CJK-Bold', regular, subfontIndex=0))
    registerFontFamily('CJK', normal='CJK', bold='CJK-Bold',
                       italic='CJK', boldItalic='CJK-Bold')
    return True


# ---------------------------------------------------------------------------
# 3) Markdown 解析与渲染（兼容标题/表格/引用/列表/链接，emoji 在 PDF 中剥离）
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = A4
MARGIN = 16 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

def mk(name, **kw):
    base = dict(fontName='CJK', fontSize=10, leading=15, wordWrap='CJK')
    base.update(kw)
    return ParagraphStyle(name, **base)

styles = {
    'h1': mk('h1', fontName='CJK-Bold', fontSize=17, leading=23, spaceBefore=4,
             spaceAfter=10, alignment=1, textColor=colors.HexColor('#14315c')),
    'h2': mk('h2', fontName='CJK-Bold', fontSize=13.5, leading=19, spaceBefore=12,
             spaceAfter=6, textColor=colors.HexColor('#14315c')),
    'h3': mk('h3', fontName='CJK-Bold', fontSize=11.5, leading=16, spaceBefore=9,
             spaceAfter=5, textColor=colors.HexColor('#2563a8')),
    'body': mk('body', fontSize=10, leading=15, spaceAfter=6),
    'quote': mk('quote', fontSize=9.3, leading=14, textColor=colors.HexColor('#3a3a3a')),
    'cell': mk('cell', fontSize=8.6, leading=12),
    'cellh': mk('cellh', fontName='CJK-Bold', fontSize=8.6, leading=12,
                textColor=colors.white),
    'list': mk('list', fontSize=10, leading=15, spaceAfter=2),
}

EMOJI_RE = re.compile(
    "[" "\u2600-\u27BF" "\u2B00-\u2BFF"
    "\U0001F000-\U0001FAFF"
    "\uFE00-\uFE0F" "\u200D" "]+", re.UNICODE)

def inline(text):
    for i in range(1, 21):
        text = text.replace(chr(0x245F + i), "(%d)" % i)
    text = EMOJI_RE.sub('', text)  # PDF 无法显示 emoji，剥离避免方框
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    def lr(m):
        t = m.group(1)
        u = m.group(2).replace('\\&amp;', '&amp;').replace('\\&', '&amp;')
        return '<a href="%s">%s</a>' % (u, t)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lr, text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'~~(.+?)~~', r'<font color="#9a9a9a">\1</font>', text)
    return text

def parse(lines):
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        s = lines[i].strip()
        if s == '':
            i += 1; continue
        if s == '---':
            blocks.append(('hr', None)); i += 1; continue
        m = re.match(r'^(#{1,6})\s+(.*)$', s)
        if m:
            lvl = min(len(m.group(1)), 3)
            blocks.append(('h%d' % lvl, inline(m.group(2)).lstrip())); i += 1; continue
        if s.startswith('>'):
            buf = []
            while i < n and lines[i].strip().startswith('>'):
                c = lines[i].strip()
                buf.append('' if c == '>' else c[1:].strip())
                i += 1
            blocks.append(('quote', '<br/>'.join(inline(x) for x in buf))); continue
        if s.startswith('|'):
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append(lines[i].strip()); i += 1
            def split_row(r):
                r = r.strip()
                if r.startswith('|'): r = r[1:]
                if r.endswith('|'): r = r[:-1]
                return [c.strip() for c in r.split('|')]
            header = split_row(rows[0])
            body = [split_row(r) for r in rows[2:]]
            blocks.append(('table', (header, body))); continue
        if re.match(r'^\s*[-*]\s+', s) or re.match(r'^\s*\d+\.\s+', s):
            items = []
            ordered = bool(re.match(r'^\s*\d+\.\s+', s))
            while i < n:
                ls = lines[i]
                if re.match(r'^\s*[-*]\s+', ls.strip()) or re.match(r'^\s*\d+\.\s+', ls.strip()):
                    mm = re.match(r'^\s*(?:[-*]|\d+\.)\s+(.*)$', ls)
                    items.append(inline(mm.group(1)))
                    i += 1
                else:
                    break
            blocks.append(('list', (ordered, items))); continue
        buf = []
        while i < n:
            ls = lines[i].strip()
            if (ls == '' or ls.startswith(('---', '#', '>', '|'))
                    or re.match(r'^\s*[-*]\s+', ls)
                    or re.match(r'^\s*\d+\.\s+', ls)):
                break
            buf.append(lines[i]); i += 1
        blocks.append(('p', inline(' '.join(buf))))
    return blocks

def build_table(header, body):
    ncol = len(header)
    for r in body:
        while len(r) < ncol: r.append('')
    weights = [0] * ncol
    for r in [header] + body:
        for c in range(ncol):
            plain = re.sub(r'<[^>]+>', '', inline(r[c]))
            weights[c] = max(weights[c], len(plain))
    minw = 14.0
    colw = [minw] * ncol
    if header and re.sub(r'<[^>]+>', '', inline(header[0])).strip() == '时间':
        colw[0] = 54.0
    remaining = CONTENT_W - sum(colw)
    wsum = sum(weights) or 1
    for i in range(ncol):
        colw[i] += remaining * weights[i] / wsum
    data = [[Paragraph(inline(h), styles['cellh']) for h in header]]
    for r in body:
        data.append([Paragraph(inline(c), styles['cell']) for c in r])
    t = Table(data, colWidths=colw, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#14315c')),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#c9d3e0')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#eef3fa')]),
    ]))
    return t

def emit(kind, val, out):
    if kind == 'hr':
        out.append(Spacer(1, 4))
        out.append(HRFlowable(width='100%', thickness=0.6,
                              color=colors.HexColor('#b8c4d6'), spaceBefore=2, spaceAfter=6))
    elif kind in ('h1', 'h2', 'h3'):
        out.append(Paragraph(val, styles[kind]))
    elif kind == 'p':
        out.append(Paragraph(val, styles['body']))
    elif kind == 'quote':
        t = Table([[Paragraph(val, styles['quote'])]], colWidths=[CONTENT_W])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f3f6fa')),
            ('LINEBEFORE', (0, 0), (0, -1), 3, colors.HexColor('#2563a8')),
            ('LEFTPADDING', (0, 0), (-1, -1), 9),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        out.append(t); out.append(Spacer(1, 4))
    elif kind == 'table':
        out.append(build_table(*val)); out.append(Spacer(1, 6))
    elif kind == 'list':
        ordered, items = val
        lstyle = ParagraphStyle('listitem', parent=styles['list'],
                                leftIndent=18, firstLineIndent=-18,
                                spaceBefore=1, spaceAfter=3)
        for idx, t in enumerate(items):
            prefix = ('<font color="#14315c"><b>%d.</b></font> ' % (idx + 1)) if ordered else \
                     '<font color="#14315c">\u2022</font>  '
            out.append(Paragraph(prefix + t, lstyle))
        out.append(Spacer(1, 4))

def group_blocks(blocks):
    groups = []
    cur = None
    for kind, val in blocks:
        if kind in ('h1', 'h2', 'h3'):
            if cur is None:
                cur = [(kind, val)]
            elif cur[-1][0] in ('h1', 'h2', 'h3'):
                cur.append((kind, val))
            else:
                groups.append(cur); cur = [(kind, val)]
        else:
            if cur is None:
                cur = []
            cur.append((kind, val))
    if cur is not None:
        groups.append(cur)
    return groups

def build_flowables(blocks):
    flow = []
    for grp in group_blocks(blocks):
        inner = []
        for kind, val in grp:
            emit(kind, val, inner)
        if not inner:
            continue
        flow.append(KeepTogether(inner))
    return flow

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('CJK', 8)
    canvas.setFillColor(colors.HexColor('#888888'))
    canvas.drawRightString(PAGE_W - MARGIN, 10 * mm, "第 %d 页" % doc.page)
    canvas.restoreState()


# ---------------------------------------------------------------------------
# 4) 主流程
# ---------------------------------------------------------------------------
def resolve_outputs(src, out_arg):
    """根据 --out 推断 pdf / md 输出路径。"""
    base = os.path.splitext(os.path.basename(src))[0]
    if out_arg:
        if out_arg.lower().endswith('.pdf'):
            pdf = out_arg
            outdir = os.path.dirname(pdf) or '.'
        else:
            outdir = out_arg
            pdf = os.path.join(outdir, base + '.pdf')
    else:
        outdir = os.path.dirname(src) or '.'
        pdf = os.path.join(outdir, base + '.pdf')
    md = os.path.join(outdir, base + '.md')
    return pdf, md

def main():
    p = argparse.ArgumentParser(description="Markdown 旅行攻略 → (MD + PDF) 跨平台导出")
    p.add_argument('src', help='输入 Markdown 文件')
    p.add_argument('--out', default=None, help='输出 PDF 路径，或输出目录（默认与源同目录）')
    p.add_argument('--font', default=None, help='手动指定中文字体文件路径（跳过自动探测）')
    args = p.parse_args()

    if not os.path.exists(args.src):
        sys.stderr.write("❌ 找不到输入文件：%s\n" % args.src)
        sys.exit(1)

    regular = args.font or find_cjk_font()
    bold = find_bold_font(regular) if regular else None
    if not regular or not register_fonts(regular, bold):
        sys.stderr.write(
            "❌ 未找到可用的中文字体，无法正确渲染中文。\n"
            "   • Windows：确保存在 微软雅黑（msyh.ttc）\n"
            "   • macOS  ：系统自带苹方（PingFang）\n"
            "   • Linux  ：安装 fonts-noto-cjk 或 fonts-wqy-zenhei\n"
            "   也可用 --font /path/to/font.ttc 手动指定。\n")
        sys.exit(1)

    pdf_path, md_path = resolve_outputs(args.src, args.out)
    os.makedirs(os.path.dirname(pdf_path) or '.', exist_ok=True)

    # 写出 .md 文档（原文）
    with open(args.src, encoding='utf-8') as f:
        md_text = f.read()
    if os.path.abspath(md_path) != os.path.abspath(args.src):
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_text)

    # 渲染 .pdf 文档
    lines = md_text.split('\n')
    blocks = parse(lines)
    flow = build_flowables(blocks)
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=MARGIN, bottomMargin=16 * mm,
                            title=os.path.splitext(os.path.basename(args.src))[0])
    doc.build(flow, onFirstPage=footer, onLaterPages=footer)

    print("✅ MD  :", md_path, "(%d bytes)" % (len(md_text.encode('utf-8')) if os.path.abspath(md_path) != os.path.abspath(args.src) else os.path.getsize(args.src)))
    print("✅ PDF :", pdf_path, "(%d bytes)" % os.path.getsize(pdf_path))
    print("   字体 :", regular + ("  (粗体:%s)" % bold if bold else "  (无独立粗体, 复用常规)"))

if __name__ == '__main__':
    main()
