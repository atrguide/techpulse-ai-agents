# TechPulse Diagnostic Report PDF Standards

## LOCKED FORMAT - DO NOT MODIFY

### Header Layout (LOCKED — confirmed 2026-04-03)
```
┌─────────────────────────────────────────────────────────────────┐
│ [Shop Name Box]                    [TechPulse Box] [Synth Diag] │
│ dark navy, 13px, 7px 14px pad      dark navy box   blue text    │
│                                    [Date]                        │
├═══════════════════════════════════════════════════════════════──┤
│                     Diagnostic Report                           │
│               [Year] [Make] [Model] [System]                    │
├─────────────────────────────────────────────────────────────────┤
```

**PLATFORM BRANDING ONLY — NO SHOP LOGOS**
- All reports use TechPulse platform branding. No shop logos. No base64 image embedding.
- Shop name displayed as dark navy text box (left side header)
- Consistent across ALL shops — no switching, no logo management
- Decision confirmed by Mike Munson 2026-04-03

### Header CSS (LOCKED — confirmed 2026-04-03)
```css
.header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;   /* top-aligned — NOT center */
    padding-bottom: 12px;
    border-bottom: 2px solid #1a365d;
}

/* LEFT SIDE — Shop name text box (NO logo) */
.shop-name-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: white;
    font-size: 13px;
    font-weight: bold;
    padding: 7px 14px;
    border-radius: 6px;
    display: inline-block;
}

/* RIGHT SIDE */
.header-right { text-align: right; }

.techpulse-row {
    display: flex;
    align-items: center;
    gap: 10px;
    justify-content: flex-end;
}

.techpulse-badge {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    padding: 10px 16px;
    border-radius: 6px;
}
.techpulse-badge span {
    color: #94a3b8;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 0.5px;
}

.synth-label {
    color: #2c5282;
    font-size: 13px;
    font-weight: 600;
}

.header-date {
    font-size: 11px;
    color: #4a5568;
    margin-top: 6px;
    text-align: right;
}
```

### Header HTML Template (LOCKED)
```html
<div class="header">
    <div class="shop-name-box">[Shop Name]</div>
    <div class="header-right">
        <div class="techpulse-row">
            <div class="techpulse-badge">
                <span>TechPulse</span>
            </div>
            <span class="synth-label">Synth Diagnostic AI</span>
        </div>
        <div class="header-date">[Month DD, YYYY]</div>
    </div>
</div>
```

### NEVER INCLUDE IN PDFs (CRITICAL)

- ❌ **NO Law references** (Law #1, Law #21, etc.)
- ❌ **NO Rule references**
- ❌ **NO Internal methodology numbers**
- ❌ **NO Supabase references**
- ❌ **NO Training data references**
- ❌ **NO "Per Law #X" language**

**Rationale**: Laws/rules are internal methodology - customer reports show results, not process.

---

## Branding — Platform Only (LOCKED 2026-04-03)

**NO shop logos. NO base64 image embedding. NO logo fetching.**

All reports use TechPulse platform text branding only. This applies to ALL shops, ALL report types.

### Header (left — shop name box)
```html
<div class="shop-name-box">[Shop Name]</div>
```
- Dark navy gradient box, white bold text, 13px, 7px 14px padding

### Header (right — TechPulse badge + label)
```html
<div class="techpulse-row">
    <div class="techpulse-badge"><span>TechPulse</span></div>
    <span class="synth-label">Synth Diagnostic AI</span>
</div>
```
- Badge: dark navy gradient, 14px bold, #94a3b8 text
- Label: #2c5282, 13px, 600 weight

### Footer (centered)
```html
<div class="footer-brand">
    <span style="color: #1a365d; font-weight: bold; font-size: 13px;">TechPulse</span>
    <span class="footer-brand-text"> — Synth Diagnostic AI</span>
</div>
<p>Diagnostic Analysis Powered by Synth AI</p>
<p>Report Generated: [DATE]</p>
```
- Text color: #1a365d

---

## Report Structure (LOCKED)

### Standard Sections
1. **Vehicle Information & Complaint** - Basic vehicle data table
2. **Critical Finding** - Red-bordered box with key data
3. **Symptom Correlation Analysis** - Customer symptoms to data mapping
4. **Additional Data Points** - Supporting parameters table
5. **Root Cause Analysis** - Yellow-bordered conclusion
6. **Diagnostic Verification** - Test steps (NO law references)
7. **Recommendation** - Green-bordered repair recommendation + cost box
8. **Diagnostic Methodology** - Pattern applied (NO law numbers)

### Center Title (LOCKED)
```html
<div class="center-title">
    <h1>Diagnostic Report</h1>
    <h2>[Year] [Make] [Model] [System]</h2>
</div>
```
- Bordered top and bottom: 3px solid #1a365d
- h1: 1.8em, color #1a365d
- h2: 1.3em, color #2c5282

---

## Color Scheme (LOCKED)

| Element | Color |
|---------|-------|
| Primary Blue | #1a365d |
| Secondary Blue | #2c5282 |
| Highlight Red | #fed7d7 / #c53030 |
| Highlight Green | #c6f6d5 / #276749 |
| Highlight Yellow | #fefcbf / #975a16 |
| Key Finding Box | #ebf8ff / #3182ce |
| Root Cause Box | #fef3c7 / #d97706 |
| Recommendation Box | #d1fae5 / #059669 |
| Critical Box | #fed7d7 / #c53030 |
| Cost Box | #276749 → #38a169 |
| TechPulse Badge | #0f172a → #1e293b |

---

## Page Break Rules (REQUIRED)

Every colored box must have `break-inside: avoid; page-break-inside: avoid;` — no box ever splits across pages.

```css
/* Apply to ALL box classes: critical-box, root-cause-box, warning-box,
   rec-box, cost-box, comparison-grid, conclusion-box, plain-english-box, etc. */
.any-box {
    break-inside: avoid;
    page-break-inside: avoid;
}
```

Also apply to `.section`, `.footer`, `.comparison-grid`, `.center-title`.

---

## Report Length (locked 2026-05-08)

| Document type | Page limit |
|---|---|
| Customer handout (before/after, plain English) | 1 page |
| Tech reference (TSB, findings, signal note) | 1 page |
| Estimate | 1 page |
| Full diagnostic report | 2 pages |

- **Exception**: Images/photos added to the report may push beyond the limit — acceptable.
- **Never exceed the limit** for text-only reports — cut data tables or methodology sections if needed.
- **Priority**: Diagnosis > Data Tables > Methodology.

---

## PDF Generation Method — CDP REQUIRED

**Edge 145+ ignores `--print-to-pdf-no-header` — the file path URL appears in the footer.**

**Use CDP only.** The `html_to_pdf_cdp()` function in pdf-agent (locked, line ~185) is the standard. Key parameter: `"displayHeaderFooter": False`.

```python
# CDP call — removes all headers/footers including file path URL
ws.send(json.dumps({"id": 3, "method": "Page.printToPDF", "params": {
    "displayHeaderFooter": False, "printBackground": True,
    "paperWidth": 8.5, "paperHeight": 11,
    "marginTop": 0.6, "marginBottom": 0.6,
    "marginLeft": 0.65, "marginRight": 0.65, "preferCSSPageSize": True,
}}))
```

**DO NOT USE** the old Edge command-line approach:
```
# ❌ BROKEN — Edge 145 ignores this flag, file path shows in footer
msedge.exe --headless --print-to-pdf-no-header --print-to-pdf=...
```

---

## File Organization
```
D:\_ORGANIZED\Customer_Cases\
└── [Customer Name]\
    └── [Year] [Make] [Model] [DTC or Issue]\
        ├── [Customer]_Diagnostic_Report.html
        ├── [Customer]_Diagnostic_Report.pdf
        └── (supporting files)
```

---

## Template Location
```
D:\_ORGANIZED\PDF_Templates\DIAGNOSTIC_REPORT_TEMPLATE.html
```

---

## Quick Reference

| Setting | Value |
|---------|-------|
| Logo max-height | 140px |
| Logo max-width | 520px |
| Logo margin-top | -8px (raises logo up one click) |
| Header align-items | flex-start (top-aligned) |
| Date margin-top | 16px (drops badge down from top) |
| Default page limit | 1 page handout / 1 page reference / 1 page estimate / 2 pages full diagnostic |
| Image format | Base64 embedded |
| PDF generator | Edge headless |
| TechPulse badge height (header) | 28px |
| TechPulse logo height (footer) | 35px |
| Body font size | 11px |
| Table font size | 10px |
| Law references in PDF | ❌ NEVER |
