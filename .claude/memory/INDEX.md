# Memory System Index

Quick navigation for all agent learnings.

## Shared Knowledge

**Common reusable techniques and patterns:**
- [shared/skills.md](./shared/skills.md) - Techniques all agents can use
- [shared/patterns.md](./shared/patterns.md) - Design patterns that work
- [shared/learnings.md](./shared/learnings.md) - General insights

See: [shared/INDEX.md](./shared/INDEX.md)

## Agent-Specific Memory

Each agent maintains specialization knowledge:

### Routers
- [orchestrator-agent memory](./agents/orchestrator-agent/INDEX.md) - Routing, state detection, pipeline logic

### Architects & Generators
- [solution-architect-agent memory](./agents/solution-architect-agent/INDEX.md) - Architecture patterns, design decisions
- [coding-agent memory](./agents/coding-agent/INDEX.md) - Implementation techniques, code patterns
- [docs-agent memory](./agents/docs-agent/INDEX.md) - Documentation patterns, structure

### Reviewers & Validators
- [code-smoke-tester-agent memory](./agents/code-smoke-tester-agent/INDEX.md) - Test detection, quick validation
- [project-auditor-agent memory](./agents/project-auditor-agent/INDEX.md) - Quality checks, structure validation
- [codex-project-auditor-agent memory](./agents/codex-project-auditor-agent/INDEX.md) - Compliance checking, final validation

## Recent Learnings

| Date | Agent | Discovery | Link |
|------|-------|-----------|------|
| (none yet) | - | - | - |

## How to Use This System

### For Agents
1. Check `shared/skills.md` before starting
2. Check `agents/[your-name]/` for specialization
3. After work, update your memory with new skills/issues/patterns
4. Only write if it's reusable!

### For Humans
1. Browse agent memory to understand what they've learned
2. Check shared knowledge for common patterns
3. Use INDEX.md files for quick navigation

## Adding Memory

**Update when you discover:**
- ✅ **New skill** - Technique that works, reusable
- ✅ **Pattern** - Design that solves problem
- ✅ **Issue** - Problem + solution for future
- ⚠️ **Note** - Only if truly insightful

**DON'T add:**
- ❌ Obvious information (already in docs)
- ❌ One-off hacks (not reusable)
- ❌ Noise (pollutes system)

## System Health

Memory grows over time. Periodically:
- Move generic findings from agent folders to `shared/`
- Archive old session learnings
- Consolidate duplicate patterns

This keeps memory signal-to-noise ratio high.
