# Synth Agents

Canonical live agent definitions for the TechPulse / Synth platform. 34 agents + 1 architecture doc (`TECHPULSE_AGENT_FLOW.md`).

These are the source-of-truth agent files. Each one has frontmatter declaring its model, tools, and routing role. The Claude Code platform loads these from `~/.claude/agents/` at session start. Daniel's Flask API and Sidd's app should mirror the model assignments and routing rules from each agent's frontmatter.

## Model tier split

**Sonnet 4.6 — heavy reasoning (8 agents):**
- `synth.md` — core diagnostic mentor
- `synth-diagnostic-conductor.md` — top-level diagnostic orchestrator
- `diagnostic-brain-agent.md` — probability fusion + hypothesis ranking
- `pattern-agent.md` — waveform / scope pattern matching
- `diagram-analysis-agent.md` — wiring schematic vision
- `tsb-agent.md` — live TSB web search
- `wiring-agent.md` — wiring procedures + field tests
- `synth-mentor-agent.md` — rule generation from confirmed mistakes

**Haiku 4.5 — operations + lookups + structured ops (26 agents):**
- Conductors (data / finance / shop / diagnostic-assistant / ops-assistant)
- Superman tier auditors (data / finance / shop)
- Knowledge / data agents (scanner-normalizer, knowledge-loader, baseline, case-study, supabase, scope-pattern-builder)
- Shop ops (shop-workflow, automotive-shop-manager, tech-hours-tracker, customer-portal)
- Billing / docs (invoice-generator, pdf-agent, owner-dashboard, automobile-agent)
- Learning / improvement (platform-learning, diagnostic-accuracy)
- Code reference (techpulse-core, dtc-pid-agent)

**Never Opus on the platform.** Opus 4.7 only used during dev workstation troubleshooting when stuck — never deployed to per-tech surfaces because of cost.

## Cost rationale

| Model | Input | Output | Where it runs |
|---|---|---|---|
| Sonnet 4.6 | $3 / M | $15 / M | 8 heavy-reasoning agents |
| Haiku 4.5 | $1 / M | $5 / M | 26 ops / lookup / format agents |

5x cost difference between tiers. Putting routine ops on Haiku is what makes per-tech daily budget viable for shops.

## What Daniel and Sidd need to mirror

For every Anthropic API call in their respective platforms, the `model` parameter must match the agent's declared model in this folder. The agent's role (its description and tools list) tells you which surface or backend job it corresponds to.

If an agent file says `model: claude-sonnet-4-6` in its frontmatter, the equivalent code path on Render or in the mobile app uses `claude-sonnet-4-6`. Same for Haiku. Same agent role = same model = consistent behavior across all three platforms.

## Refresh

When agents change locally (model swap, prompt update, tool list change), copy the updated files from `~/.claude/agents/` here and commit. This folder is the canonical version Daniel and Sidd pull from.

Backup folder `backup_20260305/` contains historical snapshots — kept for reference, not actively loaded.
