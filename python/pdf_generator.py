"""
pdf_generator.py — TechPulse Diagnostic Report PDF Generator

Generates a professional diagnostic report PDF using ReportLab.
Matches TechPulse locked brand standards (PDF_REPORT_STANDARDS.md).
Returns PDF as bytes — caller handles base64 encoding or file write.

Supports report types:
  - diagnostic   : Full diagnostic report with findings, root cause, recommendation
  - estimate     : Customer-facing estimate with parts, labor, cost breakdown
  - findings     : Plain-English findings summary (no pricing)
"""

from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable

# ── Brand colors (locked — PDF_REPORT_STANDARDS.md) ───────────────────────────
C_PRIMARY    = HexColor('#1a365d')   # dark navy
C_SECONDARY  = HexColor('#2c5282')   # blue
C_BADGE_BG   = HexColor('#0f172a')   # badge background
C_RED_BG     = HexColor('#fed7d7')
C_RED_FG     = HexColor('#c53030')
C_GREEN_BG   = HexColor('#d1fae5')
C_GREEN_FG   = HexColor('#059669')
C_YELLOW_BG  = HexColor('#fef3c7')
C_YELLOW_FG  = HexColor('#d97706')
C_BLUE_BG    = HexColor('#ebf8ff')
C_BLUE_FG    = HexColor('#3182ce')
C_COST_BG    = HexColor('#276749')
C_RULE       = HexColor('#1a365d')
C_LIGHT_GRAY = HexColor('#f7fafc')
C_MID_GRAY   = HexColor('#e2e8f0')
C_TEXT       = HexColor('#2d3748')
C_MUTED      = HexColor('#4a5568')


def _styles():
    """Return a dict of named ParagraphStyles."""
    base = dict(fontName='Helvetica', fontSize=10, leading=14, textColor=C_TEXT)
    return {
        'body':     ParagraphStyle('body',     **base),
        'bold':     ParagraphStyle('bold',     fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=C_TEXT),
        'small':    ParagraphStyle('small',    fontName='Helvetica', fontSize=8, leading=11, textColor=C_MUTED),
        'label':    ParagraphStyle('label',    fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=C_MUTED),
        'h1':       ParagraphStyle('h1',       fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=C_PRIMARY, alignment=TA_CENTER),
        'h2':       ParagraphStyle('h2',       fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=C_SECONDARY, alignment=TA_CENTER),
        'h3':       ParagraphStyle('h3',       fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=C_PRIMARY),
        'section':  ParagraphStyle('section',  fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=C_SECONDARY),
        'red_head': ParagraphStyle('red_head', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=C_RED_FG),
        'grn_head': ParagraphStyle('grn_head', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=C_GREEN_FG),
        'ylw_head': ParagraphStyle('ylw_head', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=C_YELLOW_FG),
        'blu_head': ParagraphStyle('blu_head', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=C_BLUE_FG),
        'right':    ParagraphStyle('right',    fontName='Helvetica', fontSize=10, leading=14, alignment=TA_RIGHT, textColor=C_MUTED),
        'center':   ParagraphStyle('center',   fontName='Helvetica', fontSize=10, leading=14, alignment=TA_CENTER, textColor=C_TEXT),
        'cost':     ParagraphStyle('cost',     fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=white, alignment=TA_CENTER),
        'cost_sub': ParagraphStyle('cost_sub', fontName='Helvetica', fontSize=9, leading=12, textColor=HexColor('#a7f3d0'), alignment=TA_CENTER),
        'footer':   ParagraphStyle('footer',   fontName='Helvetica', fontSize=8, leading=11, textColor=C_MUTED, alignment=TA_CENTER),
        'badge':    ParagraphStyle('badge',    fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=HexColor('#94a3b8')),
        'synth':    ParagraphStyle('synth',    fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=C_SECONDARY),
        'date_txt': ParagraphStyle('date_txt', fontName='Helvetica', fontSize=9, leading=12, textColor=C_MUTED, alignment=TA_RIGHT),
        'shop_box': ParagraphStyle('shop_box', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=white),
    }


def _colored_box(content_rows, bg_color, border_color, styles, head_style_key='bold'):
    """Wrap a list of Paragraphs in a colored background box table."""
    inner = [[p] for p in content_rows]
    t = Table(inner, colWidths=[6.5 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',  (0, 0), (-1, -1), bg_color),
        ('LINEABOVE',   (0, 0), (-1,  0), 2, border_color),
        ('LINEBELOW',   (0,-1), (-1, -1), 1, border_color),
        ('LINEBEFORE',  (0, 0), (-1, -1), 2, border_color),
        ('LINEAFTER',   (0, 0), (-1, -1), 1, border_color),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',(0, 0), (-1, -1), 10),
        ('TOPPADDING',  (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING',(0,0), (-1, -1), 8),
        ('VALIGN',      (0, 0), (-1, -1), 'TOP'),
    ]))
    return KeepTogether([t])


def _header_table(shop_name, date_str, s):
    """Build the locked header: shop name box (left) | TechPulse badge + date (right)."""
    shop_cell = Table([[Paragraph(shop_name, s['shop_box'])]], colWidths=[2.5 * inch])
    shop_cell.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), C_BADGE_BG),
        ('LEFTPADDING',  (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING',   (0,0), (-1,-1), 7),
        ('BOTTOMPADDING',(0,0), (-1,-1), 7),
        ('ROUNDEDCORNERS', [6]),
    ]))

    badge_cell = Table([[Paragraph('TechPulse', s['badge'])]], colWidths=[1.5 * inch])
    badge_cell.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), C_BADGE_BG),
        ('LEFTPADDING',  (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING',   (0,0), (-1,-1), 8),
        ('BOTTOMPADDING',(0,0), (-1,-1), 8),
    ]))

    right_inner = Table([
        [badge_cell, Paragraph('Synth Diagnostic AI', s['synth'])],
        ['', Paragraph(date_str, s['date_txt'])],
    ], colWidths=[1.7*inch, 2.3*inch])
    right_inner.setStyle(TableStyle([
        ('VALIGN',       (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING',  (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING',   (0,0), (-1,-1), 0),
        ('BOTTOMPADDING',(0,0), (-1,-1), 2),
    ]))

    header = Table([[shop_cell, right_inner]], colWidths=[3.5*inch, 3.0*inch])
    header.setStyle(TableStyle([
        ('VALIGN',       (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING',  (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING',   (0,0), (-1,-1), 0),
        ('BOTTOMPADDING',(0,0), (-1,-1), 0),
    ]))
    return header


def _vehicle_table(vehicle: dict, complaint: str, s):
    """Two-column vehicle info table."""
    year  = vehicle.get('year', '')
    make  = vehicle.get('make', '')
    model = vehicle.get('model', '')
    engine= vehicle.get('engine', '')
    mileage = vehicle.get('mileage', '')

    rows = [
        [Paragraph('Vehicle', s['label']),  Paragraph(f'{year} {make} {model}', s['bold']),
         Paragraph('Engine',  s['label']),  Paragraph(engine or '—', s['bold'])],
        [Paragraph('Complaint',s['label']), Paragraph(complaint or '—', s['body']),
         Paragraph('Mileage', s['label']),  Paragraph(mileage or '—', s['body'])],
    ]
    t = Table(rows, colWidths=[1.0*inch, 2.2*inch, 0.9*inch, 2.4*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), C_LIGHT_GRAY),
        ('GRID',         (0,0), (-1,-1), 0.5, C_MID_GRAY),
        ('LEFTPADDING',  (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING',   (0,0), (-1,-1), 6),
        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
        ('VALIGN',       (0,0), (-1,-1), 'TOP'),
    ]))
    return t


def _dtc_table(dtcs: list, s):
    """Compact DTC code table."""
    if not dtcs:
        return None
    rows = [[Paragraph('DTC Code', s['label']), Paragraph('Description', s['label'])]]
    for dtc in dtcs:
        code = dtc if isinstance(dtc, str) else dtc.get('code', '')
        desc = '' if isinstance(dtc, str) else dtc.get('description', '')
        rows.append([Paragraph(code, s['bold']), Paragraph(desc or '—', s['body'])])
    t = Table(rows, colWidths=[1.3*inch, 5.2*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0),  C_PRIMARY),
        ('TEXTCOLOR',    (0,0), (-1,0),  white),
        ('BACKGROUND',   (0,1), (-1,-1), C_LIGHT_GRAY),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [C_LIGHT_GRAY, white]),
        ('GRID',         (0,0), (-1,-1), 0.5, C_MID_GRAY),
        ('LEFTPADDING',  (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING',   (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0), (-1,-1), 5),
        ('VALIGN',       (0,0), (-1,-1), 'TOP'),
    ]))
    return t


def _cost_box(amount, s):
    """Dark green cost box."""
    rows = [
        [Paragraph(f'${amount:,.0f}' if isinstance(amount, (int, float)) else str(amount), s['cost'])],
        [Paragraph('Estimated Repair Cost', s['cost_sub'])],
    ]
    t = Table(rows, colWidths=[6.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), C_COST_BG),
        ('LEFTPADDING',  (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING',   (0,0), (-1,-1), 10),
        ('BOTTOMPADDING',(0,0), (-1,-1), 10),
        ('LINEABOVE',    (0,0), (-1,0),  2, C_GREEN_FG),
        ('LINEBELOW',    (0,-1),(-1,-1), 1, C_GREEN_FG),
        ('LINEBEFORE',   (0,0), (-1,-1), 2, C_GREEN_FG),
        ('LINEAFTER',    (0,0), (-1,-1), 1, C_GREEN_FG),
    ]))
    return KeepTogether([t])


def _footer(s):
    rows = [
        [Paragraph('TechPulse  —  Synth Diagnostic AI', s['footer'])],
        [Paragraph('Diagnostic Analysis Powered by Synth AI', s['footer'])],
    ]
    t = Table(rows, colWidths=[6.5*inch])
    t.setStyle(TableStyle([
        ('LINEABOVE',    (0,0), (-1,0), 1, C_MID_GRAY),
        ('LEFTPADDING',  (0,0),(-1,-1), 0),
        ('TOPPADDING',   (0,0),(-1,-1), 6),
        ('BOTTOMPADDING',(0,0),(-1,-1), 4),
    ]))
    return t


# ── Public API ─────────────────────────────────────────────────────────────────

def generate_diagnostic_report(data: dict) -> bytes:
    """
    Generate a Diagnostic Report PDF.

    Expected keys in data:
      shop_name     : str
      vehicle       : {year, make, model, engine, mileage}
      complaint     : str
      dtcs          : list of str or {code, description}
      findings      : str   — key findings / critical data
      root_cause    : str   — root cause analysis
      recommendation: str   — repair recommendation
      cost_estimate : int|float|str  (optional)
      technician    : str   (optional)
    """
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.65*inch,  bottomMargin=0.65*inch
    )
    s = _styles()
    story = []

    shop_name  = data.get('shop_name', 'TechPulse Shop')
    vehicle    = data.get('vehicle', {})
    complaint  = data.get('complaint', '')
    dtcs       = data.get('dtcs', [])
    findings   = data.get('findings', '')
    root_cause = data.get('root_cause', '')
    rec        = data.get('recommendation', '')
    cost       = data.get('cost_estimate')
    tech       = data.get('technician', '')
    date_str   = datetime.now().strftime('%B %d, %Y')

    year  = vehicle.get('year', '')
    make  = vehicle.get('make', '')
    model = vehicle.get('model', '')

    # ── Header ────────────────────────────────────────────────────────────────
    story.append(_header_table(shop_name, date_str, s))
    story.append(HRFlowable(width='100%', thickness=2, color=C_PRIMARY, spaceAfter=8))

    # ── Center title ──────────────────────────────────────────────────────────
    story.append(HRFlowable(width='100%', thickness=2, color=C_PRIMARY, spaceBefore=4, spaceAfter=6))
    story.append(Paragraph('Diagnostic Report', s['h1']))
    vehicle_line = ' '.join(p for p in [year, make, model] if p)
    if vehicle_line:
        story.append(Paragraph(vehicle_line, s['h2']))
    story.append(HRFlowable(width='100%', thickness=2, color=C_PRIMARY, spaceBefore=6, spaceAfter=10))

    # ── Vehicle info ──────────────────────────────────────────────────────────
    story.append(Paragraph('Vehicle Information', s['h3']))
    story.append(Spacer(1, 4))
    story.append(_vehicle_table(vehicle, complaint, s))
    story.append(Spacer(1, 10))

    # ── DTC codes ─────────────────────────────────────────────────────────────
    if dtcs:
        story.append(Paragraph('Fault Codes', s['h3']))
        story.append(Spacer(1, 4))
        story.append(_dtc_table(dtcs, s))
        story.append(Spacer(1, 10))

    # ── Key findings (red / critical box) ─────────────────────────────────────
    if findings:
        story.append(Paragraph('Key Findings', s['h3']))
        story.append(Spacer(1, 4))
        story.append(_colored_box(
            [Paragraph('Critical Finding', s['red_head']),
             Spacer(1, 4),
             Paragraph(findings, s['body'])],
            C_RED_BG, C_RED_FG, s
        ))
        story.append(Spacer(1, 10))

    # ── Root cause (yellow box) ────────────────────────────────────────────────
    if root_cause:
        story.append(Paragraph('Root Cause Analysis', s['h3']))
        story.append(Spacer(1, 4))
        story.append(_colored_box(
            [Paragraph('Root Cause', s['ylw_head']),
             Spacer(1, 4),
             Paragraph(root_cause, s['body'])],
            C_YELLOW_BG, C_YELLOW_FG, s
        ))
        story.append(Spacer(1, 10))

    # ── Recommendation (green box) ─────────────────────────────────────────────
    if rec:
        story.append(Paragraph('Repair Recommendation', s['h3']))
        story.append(Spacer(1, 4))
        story.append(_colored_box(
            [Paragraph('Recommended Repair', s['grn_head']),
             Spacer(1, 4),
             Paragraph(rec, s['body'])],
            C_GREEN_BG, C_GREEN_FG, s
        ))
        story.append(Spacer(1, 10))

    # ── Cost estimate ──────────────────────────────────────────────────────────
    if cost is not None:
        story.append(_cost_box(cost, s))
        story.append(Spacer(1, 10))

    # ── Technician line ────────────────────────────────────────────────────────
    if tech:
        story.append(Paragraph(f'Diagnosed by: {tech}', s['small']))
        story.append(Spacer(1, 6))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 12))
    story.append(_footer(s))

    doc.build(story)
    return buf.getvalue()


def generate_findings_report(data: dict) -> bytes:
    """
    Plain-English Findings Summary — no pricing, no DTC codes.

    Expected keys:
      shop_name  : str
      vehicle    : {year, make, model, engine, mileage}
      complaint  : str
      findings   : str  — plain English, no codes
      what_it_means : str  — impact on vehicle / customer
      recommendation : str  — what needs to be done
      technician : str  (optional)
    """
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.65*inch,  bottomMargin=0.65*inch
    )
    s = _styles()
    story = []

    shop_name  = data.get('shop_name', 'TechPulse Shop')
    vehicle    = data.get('vehicle', {})
    complaint  = data.get('complaint', '')
    findings   = data.get('findings', '')
    meaning    = data.get('what_it_means', '')
    rec        = data.get('recommendation', '')
    tech       = data.get('technician', '')
    date_str   = datetime.now().strftime('%B %d, %Y')

    year  = vehicle.get('year', '')
    make  = vehicle.get('make', '')
    model = vehicle.get('model', '')

    story.append(_header_table(shop_name, date_str, s))
    story.append(HRFlowable(width='100%', thickness=2, color=C_PRIMARY, spaceAfter=8))
    story.append(HRFlowable(width='100%', thickness=2, color=C_PRIMARY, spaceBefore=4, spaceAfter=6))
    story.append(Paragraph('Diagnostic Findings', s['h1']))
    vehicle_line = ' '.join(p for p in [year, make, model] if p)
    if vehicle_line:
        story.append(Paragraph(vehicle_line, s['h2']))
    story.append(HRFlowable(width='100%', thickness=2, color=C_PRIMARY, spaceBefore=6, spaceAfter=10))

    story.append(_vehicle_table(vehicle, complaint, s))
    story.append(Spacer(1, 12))

    if findings:
        story.append(_colored_box(
            [Paragraph('What We Found', s['blu_head']),
             Spacer(1, 4),
             Paragraph(findings, s['body'])],
            C_BLUE_BG, C_BLUE_FG, s
        ))
        story.append(Spacer(1, 10))

    if meaning:
        story.append(_colored_box(
            [Paragraph('What This Means', s['ylw_head']),
             Spacer(1, 4),
             Paragraph(meaning, s['body'])],
            C_YELLOW_BG, C_YELLOW_FG, s
        ))
        story.append(Spacer(1, 10))

    if rec:
        story.append(_colored_box(
            [Paragraph('What We Recommend', s['grn_head']),
             Spacer(1, 4),
             Paragraph(rec, s['body'])],
            C_GREEN_BG, C_GREEN_FG, s
        ))
        story.append(Spacer(1, 10))

    if tech:
        story.append(Paragraph(f'Diagnosed by: {tech}', s['small']))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))
    story.append(_footer(s))
    doc.build(story)
    return buf.getvalue()


def generate_estimate(data: dict) -> bytes:
    """
    Customer-facing Estimate PDF.

    Expected keys:
      shop_name    : str
      vehicle      : {year, make, model, engine, mileage}
      complaint    : str
      findings     : str
      line_items   : list of {description, parts, labor}
      subtotal     : float  (optional — calculated if omitted)
      tax_rate     : float  (optional — default 0)
      total        : float  (optional — calculated if omitted)
      warranty     : str    (optional)
      technician   : str    (optional)
    """
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.65*inch,  bottomMargin=0.65*inch
    )
    s = _styles()
    story = []

    shop_name  = data.get('shop_name', 'TechPulse Shop')
    vehicle    = data.get('vehicle', {})
    complaint  = data.get('complaint', '')
    findings   = data.get('findings', '')
    items      = data.get('line_items', [])
    tax_rate   = float(data.get('tax_rate', 0))
    warranty   = data.get('warranty', '')
    tech       = data.get('technician', '')
    date_str   = datetime.now().strftime('%B %d, %Y')

    year  = vehicle.get('year', '')
    make  = vehicle.get('make', '')
    model = vehicle.get('model', '')

    # Calculate totals
    subtotal = sum(float(i.get('parts', 0)) + float(i.get('labor', 0)) for i in items)
    tax      = subtotal * tax_rate
    total    = data.get('total', subtotal + tax)

    story.append(_header_table(shop_name, date_str, s))
    story.append(HRFlowable(width='100%', thickness=2, color=C_PRIMARY, spaceAfter=8))
    story.append(HRFlowable(width='100%', thickness=2, color=C_PRIMARY, spaceBefore=4, spaceAfter=6))
    story.append(Paragraph('Repair Estimate', s['h1']))
    vehicle_line = ' '.join(p for p in [year, make, model] if p)
    if vehicle_line:
        story.append(Paragraph(vehicle_line, s['h2']))
    story.append(HRFlowable(width='100%', thickness=2, color=C_PRIMARY, spaceBefore=6, spaceAfter=10))

    story.append(_vehicle_table(vehicle, complaint, s))
    story.append(Spacer(1, 10))

    if findings:
        story.append(_colored_box(
            [Paragraph('Diagnostic Findings', s['blu_head']),
             Spacer(1, 4),
             Paragraph(findings, s['body'])],
            C_BLUE_BG, C_BLUE_FG, s
        ))
        story.append(Spacer(1, 10))

    # Line items table
    if items:
        story.append(Paragraph('Estimate Breakdown', s['h3']))
        story.append(Spacer(1, 4))
        rows = [[
            Paragraph('Service / Repair', s['label']),
            Paragraph('Parts', s['label']),
            Paragraph('Labor', s['label']),
            Paragraph('Total', s['label']),
        ]]
        for item in items:
            parts  = float(item.get('parts', 0))
            labor  = float(item.get('labor', 0))
            rows.append([
                Paragraph(item.get('description', ''), s['body']),
                Paragraph(f'${parts:,.2f}', s['body']),
                Paragraph(f'${labor:,.2f}', s['body']),
                Paragraph(f'${parts+labor:,.2f}', s['bold']),
            ])

        # Totals rows
        rows.append(['', '', Paragraph('Subtotal', s['bold']), Paragraph(f'${subtotal:,.2f}', s['bold'])])
        if tax_rate > 0:
            rows.append(['', '', Paragraph(f'Tax ({tax_rate*100:.1f}%)', s['body']), Paragraph(f'${tax:,.2f}', s['body'])])
        rows.append(['', '', Paragraph('TOTAL', s['bold']),     Paragraph(f'${total:,.2f}', s['bold'])])

        t = Table(rows, colWidths=[3.3*inch, 1.0*inch, 1.1*inch, 1.1*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,0),  C_PRIMARY),
            ('TEXTCOLOR',     (0,0), (-1,0),  white),
            ('ROWBACKGROUNDS',(0,1),(-1, len(items)), [C_LIGHT_GRAY, white]),
            ('LINEABOVE',     (0, len(items)+1), (-1, len(items)+1), 1, C_PRIMARY),
            ('GRID',          (0,0), (-1,-1), 0.5, C_MID_GRAY),
            ('LEFTPADDING',   (0,0), (-1,-1), 8),
            ('RIGHTPADDING',  (0,0), (-1,-1), 8),
            ('TOPPADDING',    (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('ALIGN',         (1,0), (-1,-1), 'RIGHT'),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t)
        story.append(Spacer(1, 10))

        story.append(_cost_box(total, s))
        story.append(Spacer(1, 10))

    if warranty:
        story.append(_colored_box(
            [Paragraph('Warranty', s['grn_head']),
             Spacer(1, 4),
             Paragraph(warranty, s['body'])],
            C_GREEN_BG, C_GREEN_FG, s
        ))
        story.append(Spacer(1, 10))

    if tech:
        story.append(Paragraph(f'Prepared by: {tech}', s['small']))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))
    story.append(_footer(s))
    doc.build(story)
    return buf.getvalue()
