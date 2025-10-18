# Agent Smith Documentation

Main documentation hub for the agent-smith project.

## Contents

### Agents
- [agents/](./agents/) - Agent system documentation
  - [BUILD_AGENTS.md](./agents/BUILD_AGENTS.md) - Template builder and agent regeneration guide

### .claude/ System

The `.claude/` directory contains the Claude Code workflow infrastructure:

- `.claude/agents-src/` - Agent source configurations (YAML)
- `.claude/agents/templates/` - Jinja2 templates for agent generation
- `.claude/agents/` - Generated agent markdown files
- `.claude/commands/` - Claude Code commands (`/plan`, `/implement_this`, etc.)
- `.claude/jobs/` - Implementation job management
  - `scheduled/` - Pending jobs with PRD + plan
  - `completed/` - Archived/completed jobs
- `.claude/docs/` - .claude-specific documentation (deprecated, see root `docs/`)

### Quick Start

1. **Create a job:**
   ```bash
   /plan
   ```
   Answers interview → generates `jobs/scheduled/<slug>/PRD.md` + `plan.md`

2. **Check status:**
   ```bash
   /status <slug>
   ```

3. **Execute:**
   ```bash
   /implement_this <slug>
   ```
   Orchestrator runs and delegates to sub-agents

4. **Manage:**
   ```bash
   /archive <slug>    # Move to completed
   /cancel <slug>     # Delete job
   ```

## Key Scripts

- **build_agents.py** - Regenerate agent markdown files from YAML + templates
  ```bash
  python3 build_agents.py              # Build all
  python3 build_agents.py orchestrator # Build specific
  ```

## Architecture Overview

```
project-root/
├── docs/                       # Main documentation (YOU ARE HERE)
│   ├── INDEX.md               # This file
│   └── agents/
│       └── BUILD_AGENTS.md    # Agent system docs
│
├── build_agents.py            # Template builder script
│
└── .claude/                   # Claude Code workflow
    ├── agents-src/            # Agent configs (YAML)
    ├── agents/
    │   ├── templates/         # Agent templates (Jinja2)
    │   └── *.md              # Generated agent files
    ├── commands/              # /plan, /implement_this, etc.
    ├── jobs/
    │   ├── scheduled/         # PRD + plan files
    │   └── completed/         # Archived jobs
    └── docs/                  # .claude-specific docs
```

## Related Files

- `build_agents.py` - Python script for regenerating agents
- `.claude/agents-src/*.yaml` - Agent source definitions
- `.claude/agents/templates/*.j2` - Agent Jinja2 templates
- `.claude/commands/` - Claude Code command definitions

## Development

See [BUILD_AGENTS.md](./agents/BUILD_AGENTS.md) for details on:
- Adding new agents
- Template format and variables
- YAML configuration structure
- Running the build system
