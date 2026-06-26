# TechPulse AI Agents

**Owner:** Mike Munson / atrguide  
**Purpose:** Shared AI agent definitions, diagnostic config, and Python utilities for the TechPulse platform.

This repo is the single source of truth for all Synth agent `.md` files. It is separate from the Vercel deployment (`techpulse-agents`). Connect here — not there.

---

## Folder Structure

```
techpulse-ai-agents/
├── agents/          ← All Synth agent .md definitions (35+ agents)
├── config/          ← Platform standards (laws, PDF standards, identity)
├── python/          ← Shared Python utilities
└── README.md
```

---

## Key Files for Flask Integration

| File | Purpose |
|------|---------|
| `agents/synth-diagnostic-conductor.md` | Main diagnostic AI system prompt |
| `agents/synth.md` | Synth core identity |
| `config/LAWS_RULES.md` | 30 diagnostic laws + 98 rules |
| `config/PDF_REPORT_STANDARDS.md` | Locked PDF format standards |
| `config/TECHPULSE_IDENTITY.md` | Platform identity and tone |
| `python/pdf_generator.py` | TechPulse branded PDF generator (ReportLab) |
| `python/check_tsb_cache.py` | TSB cache lookup utility |

---

## Integration

See the integration guide document provided by Mike for complete setup instructions.

Do not push changes to `agents/` without Mike's approval. Agent files are updated by Mike's Claude Code environment only.
