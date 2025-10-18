# Agent YAML Frontmatter Guide

Proper format for Claude Code agents with complete tool and model configuration.

## Claude Code Agent Format

Every agent markdown file must start with YAML frontmatter:

```yaml
---
name: agent-name
description: Clear description of when to use this agent
tools: tool1, tool2, tool3
model: sonnet
---

# Agent Title

Your system prompt here...
```

## Available Tools

All tools available to Claude Code agents:

| Tool | Description | Use Case |
|------|-------------|----------|
| **Bash** | Execute shell commands | Running tests, builds, deployment |
| **Edit** | Make targeted file edits | Code modifications |
| **Glob** | Find files by pattern | File discovery |
| **Grep** | Search file contents | Code/pattern searching |
| **NotebookEdit** | Modify Jupyter cells | Notebook operations |
| **NotebookRead** | Read notebooks | Notebook analysis |
| **Read** | Read file contents | Code review, analysis |
| **SlashCommand** | Run custom commands | Special operations |
| **Task** | Delegate to sub-agents | Complex multi-step tasks |
| **TodoWrite** | Manage task lists | Progress tracking |
| **WebFetch** | Fetch web content | Research |
| **WebSearch** | Search web | Information gathering |
| **Write** | Create/overwrite files | File creation |

## Model Aliases

Three model options:

| Alias | Model | Use Case |
|-------|-------|----------|
| **sonnet** | Claude 3.5 Sonnet | Balanced speed/capability (default) |
| **opus** | Claude 3 Opus | Complex reasoning |
| **haiku** | Claude 3 Haiku | Fast, simple tasks |

Special value: `'inherit'` - Use same model as main conversation

## Current Agent Configuration

### All Agents Get:

- **Tools:** All 13 tools (agents decide which to use)
- **Model:** sonnet (fast & capable)

### Tool List for Agents

```yaml
tools: Bash, Edit, Glob, Grep, NotebookEdit, NotebookRead, Read, SlashCommand, Task, TodoWrite, WebFetch, WebSearch, Write
```

Or more concisely:
```yaml
tools: [Bash, Edit, Glob, Grep, NotebookEdit, NotebookRead, Read, SlashCommand, Task, TodoWrite, WebFetch, WebSearch, Write]
```

## Agent Configuration Examples

### Minimal Agent
```yaml
---
name: simple-agent
description: Does one specific thing
tools: Read, Write
model: sonnet
---

# Simple Agent

Your prompt...
```

### Full-Featured Agent
```yaml
---
name: complex-agent
description: Handles complex multi-step tasks with full capabilities
tools: Bash, Edit, Glob, Grep, Read, Write, Task, WebSearch, WebFetch
model: sonnet
---

# Complex Agent

Your prompt...
```

### Our Implementation

**All 7 agents currently configured with:**
```yaml
tools: Bash, Edit, Glob, Grep, NotebookEdit, NotebookRead, Read, SlashCommand, Task, TodoWrite, WebFetch, WebSearch, Write
model: sonnet
```

This gives agents maximum flexibility while:
- Agents self-select which tools to actually use
- Sonnet provides good speed/capability balance
- Task tool enables sub-agent delegation

## Building Agents

The `build_agents.py` script reads YAML configs and generates proper markdown frontmatter:

**Input:** `.claude/agents/[name].yaml`
```yaml
source_file: path/to/template.md.j2
meta:
  name: agent-name
  description: Description
  tools: Bash, Edit, ...
  model: sonnet
  context_budgets: |
    - Phase 1: 20%
    - Phase 2: 80%
```

**Output:** `.claude/agents/[name].md`
```markdown
---
name: agent-name
description: Description
tools: Bash, Edit, ...
model: sonnet
---

# Agent Title

[Generated from template with variables substituted]
```

## Best Practices

### 1. Tool Selection
- Include tools you'll actually use
- Include Task if delegating to other agents
- Include WebSearch/WebFetch if doing research
- Minimal tools = clearer intent

### 2. Model Selection
- **sonnet** - Default for most tasks
- **opus** - Complex reasoning, architectural decisions
- **haiku** - Simple, fast tasks

### 3. Description
- 1-2 sentences
- Focus on WHEN to use (trigger conditions)
- Include key capabilities

### 4. Frontmatter Order
Keep consistent order:
1. name
2. description
3. tools
4. model

## Integration with Agent-Smith

Agent-Smith's agent building system:

```
.claude/agents/[name].yaml
  ↓ (build_agents.py)
  ↓ Reads YAML config
  ↓ Loads template: [meta.source_file]
  ↓ Generates YAML frontmatter
  ↓ Substitutes {{ meta.* }} variables
  ↓ Renders {% include %} components
  ↓
.claude/agents/[name].md
  ↓ Output: Complete agent with proper frontmatter
```

## Checklist: Proper Agent Format

- [ ] YAML frontmatter at top
- [ ] `---` delimiters present
- [ ] `name` field (lowercase, hyphenated)
- [ ] `description` field (1-2 sentences)
- [ ] `tools` field (list or comma-separated)
- [ ] `model` field (sonnet/opus/haiku or inherit)
- [ ] System prompt after `---`
- [ ] Clear role and mission
- [ ] Process steps defined
- [ ] Output format specified

## Example: Complete Agent

```yaml
---
name: solution-architect-agent
description: Senior architect with 15+ years experience. Creates detailed technical architecture from project requirements. Minimalist SOLID approach.
tools: Bash, Edit, Glob, Grep, Read, Write, WebFetch
model: sonnet
---

# Solution Architect Agent

Senior technical architect with 15+ years experience designing scalable systems.

## Mission

Transform project requirements into detailed technical architecture.

## Key Responsibilities

- Break requirements into components
- Choose optimal tech stack
- Design data models
- Plan implementation strategy
- Document architecture decisions

## Process

### Phase 1: Understand Requirements (15% context)
1. Read project plan
2. Extract MUST-have features
3. Identify constraints
4. List success criteria

### Phase 2: Design Architecture (40% context)
1. Break into components
2. Define interfaces
3. Choose tech stack
4. Design data models

...
```

## Reading This Guide

Use this guide to:
- Understand YAML frontmatter format
- Check tool availability
- Verify model options
- Validate agent configuration
- Build new agents properly
