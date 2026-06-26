---
name: techpulse-core
description: TechPulse shared rule set -- core diagnostic laws, flow rules, PID rules, bank rules, scope boundary, and confidence formula. Loaded once per session by synth-diagnostic-conductor. All worker agents apply these rules by reference -- do not embed rules inline.
tools: Read
model: claude-haiku-4-5-20251001
---

# TechPulse Core Rules

## Laws

Law 1 — Test before replacing
Law 2 — One step at a time
Law 3 — Ask what has been tested
Law 4 — Graph before number
Law 5 — Isolate the system
Law 6 — Test one sensor at a time
Law 7 — Verify power and ground before module replacement

## Diagnostic Flow

Pattern → Verification → Root Cause

## PID Rule

Two related PID deviations required before naming a direction.
STFT excluded from pattern qualification — use LTFT only for trend.

## Bank Rule

One bank abnormal → bank fault
Both banks abnormal → global system fault

## Scope Rule

Scope-agent identifies waveform condition only.
Root cause confirmed by conductor.

## Confidence Rule

Case similarity supports direction only.
Live PID data confirms diagnosis.

## Pattern Signature Format (LOCKED)

```
CONDITION | KEY PID VALUES | BASELINE DEVIATION | OBSERVATION
```

CONDITION: COLD_IDLE | WARM_IDLE | CRUISE | LOAD (uppercase, underscores)
KEY PID VALUES: "[PID name] [value] [unit]" comma-separated
BASELINE DEVIATION: explicit "[PID] +/-N [unit] above/below baseline ([range])" — never blank, never N/A
If no baseline: "No baseline — [platform] [condition]"

## Acceptance Criteria Format (LOCKED)

```
[MEASUREMENT] [TARGET] at [CONDITION] within [TIMEFRAME]
```

Minimum 2 entries. Set at diagnosis time. Never after repair. Null/[] = rejected.

## Confidence Score Formula (LOCKED)

```
score = (case_similarity × 0.35) + (baseline_deviation × 0.45) + (pattern_match × 0.20)
```

baseline_deviation: confirmed=1.00 | partial=0.50 | none=0.00
pattern_match: strong=1.00 | moderate=0.50 | weak=0.25 | no match=0.00

Thresholds: 0.90+ proceed | 0.70+ one verify test | 0.50+ more testing required | <0.50 STOP — flag to Mike

## How Agents Use This

Reference in agent prompt: `Apply TechPulse Core Rules.`
Conductor loads once per session. Worker agents inherit via context.
Do not re-embed these rules inside individual agent files.
