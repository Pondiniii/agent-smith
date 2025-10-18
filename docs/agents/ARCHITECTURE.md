# Agent Architecture: Why Split agents-src/ vs agents/templates/?

## Current Structure

```
.claude/
├── agents-src/          ← YAML configs
│   ├── orchestrator.yaml
│   ├── coding-agent.yaml
│   └── codex-auditor.yaml
│
├── agents/
│   ├── templates/       ← Jinja2 templates
│   │   ├── orchestrator.md.j2
│   │   ├── coding_agent.md.j2
│   │   └── validator_codex.md.j2
│   │
│   └── *.md            ← Generated output
│       ├── orchestrator.md
│       ├── coding-agent.md
│       └── codex-auditor.md
```

## The Question: Why Not Just Use agents-src/?

**TL;DR:** Split is better for **flexibility and reuse**, but if you want **simplicity**, consolidating is fine.

## Reasons FOR Splitting

### 1. **Template Reuse**
Multiple agents can use the same template with different configs:

```yaml
# agents-src/coding-agent.yaml
source_file: .claude/agents/templates/base_agent.md.j2

# agents-src/test-agent.yaml
source_file: .claude/agents/templates/base_agent.md.j2  ← SAME template!
```

**Benefit:** Update template once → all agents using it get updated

### 2. **Separation of Concerns**
- **Config** (YAML) = what to build (name, tools, model)
- **Template** (Jinja2) = how to render (structure, format)
- **Output** (MD) = final agent prompt

**Benefit:** Easier to understand, maintain, and modify each part independently

### 3. **Template Versioning**
You might want multiple versions of agent templates:

```
agents/templates/
├── base_agent.md.j2           ← Current version
├── base_agent_v1.md.j2        ← Old version (reference)
└── base_agent_experimental.md.j2  ← In development
```

**Benefit:** Easy rollback, A/B testing without duplicating configs

### 4. **Shared Components**
Jinja2 templates can include components:

```
agents/templates/
├── components/
│   ├── pre_work.md.j2
│   ├── work.md.j2
│   └── post_work.md.j2
└── coding_agent.md.j2         ← Includes components
```

**Benefit:** DRY - reuse common sections across multiple agents

## Reasons AGAINST Splitting (For Simplicity)

### If You Go: "Just Keep Everything in agents-src/"

```
.claude/agents-src/
├── orchestrator.yaml
├── orchestrator.md.j2          ← Keep template here too
├── coding-agent.yaml
├── coding-agent.md.j2
└── codex-auditor.yaml
└── codex-auditor.md.j2
```

**Pros:**
- Simpler structure
- Everything is co-located
- Fewer directories to manage
- Each agent is self-contained

**Cons:**
- Harder to reuse templates
- Can't share components easily
- Mix of config and template in same dir

## Recommendation

### **Option A: Keep Current Split** ✅
**When:**
- You plan to reuse templates
- Multiple agents will share structure
- You want component library (pre/work/post sections)

**Cost:** One more directory to manage

### **Option B: Consolidate to agents-src/** ✅ (SIMPLER)
**When:**
- Each agent is unique
- You want minimal complexity
- Each agent has its own template

**Benefit:** Fewer directories, simpler mental model

## Proposed Consolidated Structure (If You Want Simplicity)

```
.claude/agents-src/
├── orchestrator/
│   ├── config.yaml
│   └── prompt.md.j2
├── coding-agent/
│   ├── config.yaml
│   └── prompt.md.j2
└── codex-auditor/
    ├── config.yaml
    └── prompt.md.j2
```

**Then:**
```python
# build_agents.py
config = load_yaml(f".claude/agents-src/{agent_name}/config.yaml")
template = f".claude/agents-src/{agent_name}/prompt.md.j2"
output = render(template, config)
write(output, f".claude/agents/{agent_name}.md")
```

## Hybrid Approach (Best of Both)

```
.claude/agents-src/
├── orchestrator/
│   ├── config.yaml
│   ├── prompt.md.j2      ← Custom per agent
│   └── components/        ← Shared includes
│       └── state_tracking.j2
├── coding-agent/
│   ├── config.yaml
│   └── prompt.md.j2
```

- Each agent has its own config + template
- Templates can reference shared components
- Still organized and reusable
- Less "magic" than the split structure

## What I Recommend

**CONSOLIDATE** agents into `agents-src/` organized by agent:

```
.claude/agents-src/
├── orchestrator/
│   ├── config.yaml
│   ├── template.md.j2
│   └── README.md
├── coding-agent/
│   ├── config.yaml
│   ├── template.md.j2
│   └── README.md
└── codex-auditor/
    ├── config.yaml
    ├── template.md.j2
    └── README.md

.claude/agents/ ← (generated from build_agents.py)
├── orchestrator.md
├── coding-agent.md
└── codex-auditor.md
```

**Benefits:**
- Simple, flat structure
- Everything self-contained
- Still buildable with script
- Easy to add new agents (copy existing agent dir)
- Per-agent documentation (README.md in each dir)

## Refactoring Steps (If You Want to Do It)

```bash
# 1. Create agent directories
mkdir -p .claude/agents-src/orchestrator
mkdir -p .claude/agents-src/coding-agent
mkdir -p .claude/agents-src/codex-auditor

# 2. Move configs
mv .claude/agents-src/orchestrator.yaml .claude/agents-src/orchestrator/config.yaml
mv .claude/agents-src/coding-agent.yaml .claude/agents-src/coding-agent/config.yaml
mv .claude/agents-src/codex-auditor.yaml .claude/agents-src/codex-auditor/config.yaml

# 3. Move templates
mv .claude/agents/templates/orchestrator.md.j2 .claude/agents-src/orchestrator/template.md.j2
mv .claude/agents/templates/coding_agent.md.j2 .claude/agents-src/coding-agent/template.md.j2
mv .claude/agents/templates/validator_codex.md.j2 .claude/agents-src/codex-auditor/template.md.j2

# 4. Update build_agents.py to read from new structure
# 5. Rebuild
python3 build_agents.py
```

## Decision: What Should We Do?

1. **Keep current split** - if template reuse matters
2. **Consolidate to agents-src/** - if simplicity matters (RECOMMENDED)
3. **Hybrid** - keep per-agent structure but share components

What's your preference?
