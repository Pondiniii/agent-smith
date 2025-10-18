# Agent Memory System

Persistent learning system for agents. Each agent builds knowledge from experience.

## Purpose

- **Skills:** Reusable techniques and patterns discovered
- **Notes:** Observations and insights from execution
- **Issues:** Known problems and their solutions
- **Patterns:** Design patterns and best practices

## Structure

```
.claude/memory/
├── shared/              # Cross-agent reusable knowledge
│   ├── skills.md       # Universal techniques
│   ├── patterns.md     # General design patterns
│   └── learnings.md    # Common insights
│
├── agents/             # Per-agent specialization
│   ├── orchestrator-agent/
│   ├── coding-agent/
│   ├── solution-architect-agent/
│   ├── docs-agent/
│   ├── code-smoke-tester-agent/
│   ├── project-auditor-agent/
│   └── codex-project-auditor-agent/
│
└── sessions/           # Per-job learnings (future)
```

## For Agents

### Reading Memory
Before or during work, check:
- `shared/skills.md` - Reusable techniques
- `agents/[your-name]/skills.md` - Your specialization
- `agents/[other]/notes.md` - Learn from peers

### Writing Memory
After completing a task, update:
- `agents/[your-name]/skills.md` - New technique discovered?
- `agents/[your-name]/notes.md` - Observations and insights
- `agents/[your-name]/issues.md` - Problem encountered?
- `agents/[your-name]/patterns.md` - Effective pattern found?

**Rule:** Only update if you discovered something REUSABLE. Don't pollute memory with noise.

## Format Standards

### skills.md
```markdown
## Skill Name

**When to use:** [conditions/triggers]

**Technique:**
[How to do it]

**Code Pattern:**
```
[example if applicable]
```

**Benefits:** [why it works]

**Gotchas:** [edge cases, pitfalls]

**Discovered:** [date, agent, context]
```

### issues.md
```markdown
## Issue Name

**Symptom:** [what goes wrong]

**Root Cause:** [why it happens]

**Fix:**
[Solution steps]

**Prevention:** [how to avoid in future]

**Discovered:** [date, agent, when occurred]
```

### patterns.md
```markdown
## Pattern Name

**Problem:** [what problem does this solve?]

**Solution:**
[The pattern]

**Tradeoffs:** [pros/cons]

**When to use:** [conditions]

**Example:**
```
[code/config example]
```

**Discovered:** [date, agent, context]
```

### notes.md
```markdown
## Topic / Observation

[Free-form observations, learnings, gotchas]
- Point 1
- Point 2

## Another Finding

[More insights]

**Date:** [when discovered]
**Agent:** [who discovered]
```

## Version Control

Memory is git-tracked:
```bash
git add .claude/memory/
git commit -m "Update agent memory: [agent] learned [skill/pattern]"
```

## Querying Memory

Agents can search:
```bash
grep -r "database connection" .claude/memory/agents/
grep -r "timeout" .claude/memory/shared/
```

## Regular Maintenance

- **Monthly:** Review and consolidate learnings
- **Quarterly:** Move generic findings to `shared/`
- **Yearly:** Archive session learnings

## Integrations

Memory helps:
- Future agents avoid known issues
- Quick reference for common problems
- Building agent expertise over time
- Cross-agent knowledge sharing
