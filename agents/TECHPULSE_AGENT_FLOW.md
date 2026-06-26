# TechPulse Agent System — Complete Flow
Updated: 2026-05-05

---

## ARCHITECTURE COUNTS

```
34 Total Agent Files
   └─ 4  Top-Level Conductors (entry points — one per domain)
   └─ 13 Diagnostic Pipeline Workers (all wired, all active)
   └─ 6  Shop / Finance / Data Workers
   └─ 5  Web Platform Only (not Claude Code subagents)
   └─ 4  On-Demand Specialty Agents (via diagnostic-assistant-conductor)
   └─ 8  On-Demand Ops Agents (via ops-assistant-conductor)
   └─ 2  Utility / Admin Agents
   └─ 1  Shared Rule Set (techpulse-core)

9 Python Utilities (standalone scripts — zero LLM tokens)
3 synth_instructions knowledge sections:
   └─ DTC_CHEAT_SHEET    (DTC → required PID names)
   └─ CHEAT_{MAKE}       (platform-specific PID definitions)
   └─ PID_STARTER_SET    (system-level starter PID sets — NEW 2026-05-05)
```

---

## TOP-LEVEL CONDUCTORS (Entry Points)

| Agent | Entry Point For | Model |
|-------|----------------|-------|
| synth-diagnostic-conductor | All diagnostic work | Sonnet 4.6 |
| synth-shop-conductor | RO lifecycle, clock in/out, shop floor | Sonnet 4.6 |
| synth-finance-conductor | Invoicing, payments, revenue | Sonnet 4.6 |
| synth-data-conductor | Database, agent registry, platform data | Sonnet 4.6 |

---

## WEB PLATFORM ONLY (not Claude Code subagents)

| Agent | Role |
|-------|------|
| synth-superman-shop | Web platform shop floor commander |
| synth-superman-finance | Web platform billing commander |
| synth-superman-data | Web platform data commander |
| synth | Standalone Synth diagnostic AI (web) |
| diagnostic-assistant-conductor (web only routing) | On-demand specialty routing for web |

---

## DIAGNOSTIC PIPELINE — KB GATE RUNS FIRST

Before any agent fires, the conductor runs the KB Gate in parallel:

| Step | What Runs | Why |
|------|-----------|-----|
| check_tsb_cache.py | Tier 1 TSB — instant Supabase hit, zero tokens | A cached TSB can be the complete answer |
| DTC-to-PID cheat sheet lookup | Maps DTC → exact required PID names | Saves 80% token cost — don't read 15-page PDFs |
| case-study-agent SEARCH (pre-flight) | Semantic search against 165+ real cases | Gets pattern recognition in before vehicle confirmed |
| mike_theories lookup | Field-proven diagnostic theories table | Theory match = follow the theory, full stop |

**RULE: Theory match → FOLLOW THE THEORY. In-context reasoning does NOT override a matched theory.**

---

## DIAGNOSTIC WORKERS — ALL ACTIVE + WIRED

Called by synth-diagnostic-conductor through the pipeline:

| Batch | Agent | Role | Model |
|-------|-------|------|-------|
| Batch 0 | automobile-agent | VIN decode + vehicle lookup (104,887 rows) | Haiku 4.5 |
| Batch 0 | synth-knowledge-loader | Load cheat sheet + PID sheet + PID starter set at session start | Haiku 4.5 |
| Sequential | scanner-normalizer-agent | Normalize raw scanner input (CSV, paste, freeze frame) → clean JSON | Haiku 4.5 |
| Batch 1 | tsb-agent | TSB live web search — fallback only (Tier 2) | Haiku 4.5 |
| Batch 1 | case-study-agent | Search 165+ real-world cases (semantic) | Haiku 4.5 |
| Batch 1 | dtc-pid-agent (LOOKUP) | Look up DTC in platform PID sheet, select exact PIDs needed | Haiku 4.5 |
| Batch 2 | baseline-agent | Compare live PIDs vs known-good ranges, return deviation JSON | Haiku 4.5 |
| Batch 2 | pattern-agent | PID ENGINE: 12+ patterns. SCOPE ENGINE: 456+ waveform patterns | Haiku 4.5 |
| Batch 2 | dtc-pid-agent (ANALYZE) | Evaluate PID values vs normal ranges per operating condition | Haiku 4.5 |
| Brain | diagnostic-brain-agent | Fuse all inputs → ranked hypotheses + one discriminator test | Sonnet 4.6 |
| Output | pdf-agent | Diagnostic report, estimate, findings PDFs via CDP | Sonnet 4.6 |
| Output | automotive-shop-manager | Log case to Supabase, run cheat_sheet_writer.py on CONFIRM_CORRECT | Haiku 4.5 |
| Output | shop-workflow-agent | Update RO through full lifecycle | Haiku 4.5 |

---

## ON-DEMAND SPECIALTY AGENTS (via diagnostic-assistant-conductor)

| Path | Agent | Trigger | Model |
|------|-------|---------|-------|
| Path 1 | pattern-agent SCOPE ENGINE | Scope waveform description or image | Sonnet 4.6 |
| Path 1 | wiring-agent | Circuit-level testing needed | Sonnet 4.6 |
| Path 1 | diagram-analysis-agent | Tech uploads wiring schematic image | Sonnet 4.6 |
| Path 2 | customer-portal-agent | Send estimate, record approval, send invoice | Haiku 4.5 |
| Path 3 | diagnostic-accuracy-agent | Auto-runs after every completed case | Haiku 4.5 |
| Path 4 | synth-mentor-agent | CONFIRM_INCORRECT → generates if-then rules | Sonnet 4.6 |

---

## ON-DEMAND OPS AGENTS (via ops-assistant-conductor)

| Agent | Role | Model |
|-------|------|-------|
| synth-shop-conductor | Shop floor operations | Haiku 4.5 |
| synth-finance-conductor | Billing and payments | Haiku 4.5 |
| synth-data-conductor | Database and reporting | Haiku 4.5 |
| supabase-agent | DB gateway, schema, queries | Sonnet 4.6 |
| owner-dashboard | KPI dashboards — DAILY, REVENUE, WEEKLY, etc. | Haiku 4.5 |
| invoice-generator | Customer-facing invoice PDF from RO | Haiku 4.5 |
| tech-hours-tracker | Clock in/out, labor hours, rates | Haiku 4.5 |
| synth-mentor-agent | Coaching, mistake analysis | Sonnet 4.6 |

---

## LEARNING / PLATFORM AGENTS

| Agent | Role | Model | Trigger |
|-------|------|-------|---------|
| platform-learning-agent | Mistake logging, agent fixes, rule writing, law suggestions | Haiku 4.5 | URGENT only — never on CONFIRM_CORRECT |

**CONFIRM_CORRECT** → `cheat_sheet_writer.py` inside `automotive-shop-manager` (no agent call)
**CONFIRM_INCORRECT** → platform-learning-agent MODE 2 (immediate file + Supabase batch)
**AGENT FLAW / CODE NEED** → platform-learning-agent MODE 3 (any conductor can call)

---

## ADMIN AGENTS (Mike direct — NOT part of diagnostic flow)

| Agent | Role | Model |
|-------|------|-------|
| scope-pattern-builder | Add new scope patterns to scope_patterns table | Haiku 4.5 |

---

## SHARED / SUPPORT

| Agent | Role | Model |
|-------|------|-------|
| techpulse-core | Shared rule set — laws, flow, formulas | Haiku 4.5 |

---

## PYTHON UTILITIES (no LLM — zero token cost)

| Script | Role |
|--------|------|
| check_tsb_cache.py | Tier 1 TSB — instant Supabase cache lookup, zero tokens |
| tsb_search.py | Tier 2A TSB — direct tsbsearch.com POST, ~700 tokens |
| pattern_engine.py | Deterministic PID pattern matching (12+ JSON patterns) |
| confidence-engine.py | Confidence score calculator |
| scanner-normalizer.py | Scanner normalizer entry point |
| baseline-agent.py | Baseline comparison math |
| synth_search.py | Semantic case search utility |
| cheat_sheet_writer.py | Confirmed case → short cheat sheet → synth_instructions |
| cheat_sheet_uploader.py | Batch upload .txt cheat sheet files → synth_instructions |
| mistake_logger.py | File immediate · Supabase batched every 5 |

---

## SYNTH_INSTRUCTIONS KNOWLEDGE SECTIONS

| Section | What's in it | Loaded by |
|---------|-------------|-----------|
| DTC_CHEAT_SHEET | DTC → required PID names (3–7 per code) | synth-knowledge-loader at session start |
| CHEAT_{MAKE} | Platform-specific observed PID ranges and definitions | synth-knowledge-loader after vehicle confirmed |
| DTC_CHEAT_SHEET_EVAP | EVAP-specific DTC → PID mappings | synth-knowledge-loader on EVAP cases |
| PID_STARTER_SET | System-level starter PID sets (Fuel Trim, Misfire, AT, EVAP, No Start, Idle, Cooling, VVT, GDI, Air/MAF) — NEW 2026-05-05 | Semantic search by conductor on any system-level complaint |

---

## DIAGNOSTIC FLOW — PATH A (DTCs Present)

```
Tech provides: vehicle + DTC codes + scanner data
        │
        ▼
synth-diagnostic-conductor
        │
        ├─ KB GATE (parallel — runs BEFORE vehicle ID):
        │      ├─ check_tsb_cache.py (Tier 1 — zero tokens)
        │      ├─ DTC cheat sheet lookup (DTC → required PIDs)
        │      ├─ case-study-agent SEARCH (pre-flight semantic)
        │      └─ mike_theories lookup (field-proven pattern match)
        │          └─ THEORY MATCH → follow it. Full stop.
        │
        ├─ Batch 0 (parallel):
        │      ├─ automobile-agent (vehicle_id confirmed)
        │      └─ synth-knowledge-loader (cheat sheet + PID sheet)
        │
        ├─ scanner-normalizer-agent (messy input → clean JSON)
        │
        ├─ Batch 1 — Lookup (parallel):
        │      ├─ tsb-agent (Tier 2 — live web, on demand only)
        │      ├─ case-study-agent (full semantic search)
        │      └─ dtc-pid-agent LOOKUP (select exact PIDs)
        │
        ├─ Operating condition gate (COLD_IDLE/WARM_IDLE/CRUISE/LOAD)
        │
        ├─ Batch 2 — Analysis (parallel):
        │      ├─ baseline-agent (deviation JSON per PID)
        │      ├─ pattern-agent PID ENGINE (deterministic match)
        │      └─ dtc-pid-agent ANALYZE_PIDS (flag deviations)
        │
        ├─ diagnostic-brain-agent:
        │      Fuse: theory_hits + case matches + baselines + pattern + TSB
        │      Output: ranked hypotheses + one discriminator test
        │
        └─ Output (parallel):
               ├─ pdf-agent (diagnostic report PDF)
               ├─ automotive-shop-manager (log + cheat_sheet_writer.py on confirm)
               └─ shop-workflow-agent (RO status update)
```

---

## DIAGNOSTIC FLOW — PATH B (No DTCs — Symptom Only)

```
Tech provides: vehicle + symptoms, no DTC codes
        │
        ▼
synth-diagnostic-conductor
        │
        ├─ KB GATE (same as Path A — runs first)
        │
        ├─ Batch 0 (vehicle ID + session load)
        │
        ├─ scanner-normalizer-agent
        │
        ├─ Batch 1 — Lookup (parallel):
        │      ├─ case-study-agent (symptom-based semantic search)
        │      └─ tsb-agent (symptom-based, on demand)
        │
        ├─ Pull PID_STARTER_SET for the system in complaint:
        │      └─ Synth asks for the right starter PIDs before generic guessing
        │
        ├─ Operating condition gate — MANDATORY STOP if not stated
        │
        ├─ Batch 2 — Analysis (parallel):
        │      ├─ baseline-agent
        │      └─ pattern-agent PID ENGINE
        │
        ├─ dtc-pid-agent ANALYZE_PIDS
        │
        └─ diagnostic-brain-agent → ranked hypotheses + discriminator test
```

---

## SHOP FLOOR FLOW

```
Customer check-in → synth-shop-conductor
        ├─ shop-workflow-agent     (RO creation, status tracking)
        ├─ tech-hours-tracker      (clock in/out, labor)
        └─ customer-portal-agent   (estimate approval, pickup alerts)
```

---

## BILLING FLOW

```
Job complete → synth-finance-conductor
        ├─ invoice-generator    (PDF invoice from RO)
        └─ pdf-agent            (diagnostic report + estimate PDFs via CDP)
```

---

## CONFIDENCE SCORE FORMULA (LOCKED)

```
score = (case_similarity × 0.35)
      + (baseline_deviation × 0.45)
      + (pattern_match × 0.20)

baseline: confirmed=1.00 | partial=0.50 | none=0.00
pattern:  strong=1.00 | moderate=0.50 | weak=0.25 | no match=0.00

Thresholds:
  0.90+       → proceed, document acceptance criteria
  0.70–0.89   → proceed, one verification step required
  0.50–0.69   → additional testing before repair order
  0.00–0.49   → STOP — flag to Mike
```

---

## TSB TWO-TIER SYSTEM

```
Tier 1 — check_tsb_cache.py (AUTOMATIC on every case)
  → Supabase tsb_cache table · instant · zero tokens
  → Runs in KB GATE FIRST — before PIDs, before DB search
  → A cached TSB can be the complete diagnosis

Tier 2 — tsb-agent (ON DEMAND only)
  → Called ONLY when Mike explicitly asks for live TSB search
  → Primary: tsb_search.py (tsbsearch.com)
  → Fallback: web search
```

---

## PLATFORM POLICE — INSERT GATES

| Violation | Action |
|-----------|--------|
| pattern_signature blank or free-text | Reject INSERT |
| CONDITION not from locked list | Reject |
| acceptance_criteria null or [] | Reject NEW CASE |
| confidence_score < 0.50 with repair recommendation | STOP — flag to Mike |
| TSB results missing from KB Gate | Process failure |
| Root cause stated before verification result returned | Prohibited |
| PID_STARTER_SET not consulted on symptom-only case | Process gap |

---

## SUPABASE PROJECT

```
URL: https://fcqejcrxtrqdxybgyueu.supabase.co
Key tables:
  diagnostic_case_studies  repair_orders          tech_time_entries
  invoice_line_items        customer_communications diagnostic_failures
  platform_baselines        scope_patterns         synth_instructions
  synth_diagnostic_laws     synth_diagnostic_rules agents
  vehicles                  tsb_cache              mike_theories

Storage bucket: diagnostic-reports

synth_instructions sections:
  DTC_CHEAT_SHEET · DTC_CHEAT_SHEET_EVAP · CHEAT_FORD · CHEAT_GM
  CHEAT_TOYOTA · CHEAT_VAG · CHEAT_HK · CHEAT_HONDA · CHEAT_NISSAN
  PID_STARTER_SET (NEW — 10 system-level starter PID sets)
  WIRING_DIAGNOSTICS · PLATFORM_PROTOCOLS · OPERATING_INSTRUCTIONS
```
