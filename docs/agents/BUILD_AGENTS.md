# build_agents.py

Minimalist template builder for regenerating agent markdown files from YAML configs + Jinja2 templates.

## Overview

```
.claude/agents-src/*.yaml  +  .claude/agents/templates/*.j2  →  .claude/agents/*.md
```

## Usage

```bash
# Build all agents
python3 build_agents.py

# Build specific agent
python3 build_agents.py orchestrator
```

## How It Works

1. **Read YAML config** from `.claude/agents-src/`
   - Example: `orchestrator.yaml`
   - Contains: `source_file`, `meta` (name, description, model, tools, output_name)

2. **Load Jinja2 template** from `.claude/agents/templates/`
   - Example: `orchestrator.md.j2`
   - Referenced in YAML `source_file` field

3. **Render template** with metadata context
   - Simple `{{ key }}` and `{{ meta.key }}` substitution
   - No external template engine (built-in Python)

4. **Write output** to `.claude/agents/`
   - Uses `output_name` from YAML meta
   - Example: `orchestrator.yaml` → `orchestrator.md`

## YAML Format

```yaml
source_file: .claude/agents/templates/orchestrator.md.j2
meta:
  name: orchestrator
  description: Main orchestrator agent
  model: sonnet
  tools:
    - read
    - write
    - task
  output_name: orchestrator
```

## Template Format

Simple Jinja2-style variable substitution:

```markdown
# {{ meta.name }}

{{ meta.description }}

## Model
- Model: {{ meta.model }}
- Tools: {{ meta.tools }}
```

Available context:
- `{{ key }}` - Top-level keys from YAML
- `{{ meta.key }}` - Keys from `meta` section

## Features

- ✅ No external dependencies (uses stdlib only)
- ✅ Simple YAML parser (supports nested structures)
- ✅ Flexible template paths (relative or absolute)
- ✅ Batch or individual agent builds
- ✅ Clear error messages

## Architecture

```
agents-src/
├── orchestrator.yaml      # Config: what to build
├── coding-agent.yaml
└── codex-auditor.yaml

agents/templates/
├── orchestrator.md.j2     # Template: how to render
├── coding_agent.md.j2
└── validator_codex.md.j2

agents/
├── orchestrator.md        # Output: built agent
├── coding-agent.md
└── codex-auditor.md
```

## Adding New Agents

1. Create YAML config in `.claude/agents-src/new-agent.yaml`:
   ```yaml
   source_file: .claude/agents/templates/new_agent.md.j2
   meta:
     name: new-agent
     description: ...
     output_name: new-agent
   ```

2. Create template in `.claude/agents/templates/new_agent.md.j2`:
   ```markdown
   # {{ meta.name }}
   {{ meta.description }}
   ```

3. Build:
   ```bash
   python3 build_agents.py new-agent
   ```

## Development

### Modifying the Parser

Edit `parse_yaml_simple()` for custom YAML features (currently supports basic key:value and nested structures with indentation).

### Adding Template Features

Edit `render_template()` to add support for:
- Conditionals: `{% if ... %}`
- Loops: `{% for ... %}`
- Filters: `{{ key | filter }}`

Currently only `{{ }}` substitution is supported (no Jinja2 engine needed).

## Limitations

- Simple YAML parser (no anchors, aliases, or advanced features)
- Basic template rendering (no full Jinja2 engine)
- Paths must be relative to current working directory

## Future Enhancements

- [ ] Optional Jinja2 engine integration (if pip becomes available)
- [ ] Template inheritance and includes
- [ ] Config validation schema
- [ ] Watch mode for auto-rebuild on changes
- [ ] Parallel agent builds

## Example Run

```bash
$ python3 build_agents.py
Building 3 agent(s)...

✓ codex-auditor.yaml → codex-auditor.md
✓ coding-agent.yaml → coding-agent.md
✓ orchestrator.yaml → orchestrator.md

✓ Complete: 3 agent(s) built
```

## Integration

Use in CI/CD or pre-commit hooks:

```bash
# .git/hooks/pre-commit
python3 build_agents.py
git add .claude/agents/*.md
```

Or as part of build system:

```bash
make build-agents
```

## Troubleshooting

**Q: "template not found"**
A: Check that `source_file` in YAML points to an existing template file in `.claude/agents/templates/`

**Q: Output file has wrong name**
A: Verify `output_name` in YAML meta section

**Q: Variables not being substituted**
A: Ensure YAML is properly formatted with correct indentation (2 spaces per level)

## Code Structure

- `parse_yaml_simple()` - Lightweight YAML parser
- `render_template()` - Simple variable substitution
- `build_agent()` - Single agent build logic
- `main()` - CLI entry point

Total: ~170 lines, no dependencies.
