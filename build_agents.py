#!/usr/bin/env python3
"""
Build agent markdown files from unified .j2 definition files.

Structure:
    .claude/agents/
    ├── orchestrator-agent.j2      ← Agent definition (YAML config + template)
    ├── coding-agent.j2
    └── components/
        ├── prework.md.j2
        ├── work.md.j2
        └── ...

Each .j2 file has:
  [Lines 1-N: YAML config]
  ---
  [Lines N+2+: Markdown template]

Usage:
    python build_agents.py              # Build all agents
    python build_agents.py orchestrator # Build specific agent
"""

import sys
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


AGENTS_DIR = Path(".claude/agents")


def parse_yaml_simple(content: str) -> dict:
    """Simple YAML parser for basic key: value and nested structures."""
    result = {}
    stack = [(0, result)]  # (indent_level, parent)
    last_key_at_indent = {}  # Track last key at each indent for list conversion

    for line in content.split("\n"):
        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith("#"):
            continue

        # Calculate indentation
        indent = len(line) - len(line.lstrip())

        # Handle list items (lines starting with -)
        if line.lstrip().startswith("- "):
            # Find the parent dict by popping to the right indent level
            while len(stack) > 1 and indent <= stack[-1][0]:
                stack.pop()

            parent_dict = stack[-1][1]

            # Find which key at this indent level owns this list
            list_key_indent = indent - 2
            list_key = last_key_at_indent.get(list_key_indent)

            if list_key:
                item = line.lstrip()[2:].strip()  # Remove "- "
                # Convert dict to list if needed, or add to existing list
                if isinstance(parent_dict.get(list_key), dict):
                    parent_dict[list_key] = []
                if isinstance(parent_dict.get(list_key), list):
                    parent_dict[list_key].append(item)
            continue

        # Pop stack if indentation decreased
        while len(stack) > 1 and indent < stack[-1][0]:
            stack.pop()

        # Parse key: value
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Track this key at this indent level (for list conversion)
            last_key_at_indent[indent] = key

            # Handle comments
            if "#" in value:
                value = value.split("#")[0].strip()

            # Get current dict
            current_dict = stack[-1][1]

            # Convert list values
            if value.startswith("[") and value.endswith("]"):
                value = [v.strip() for v in value[1:-1].split(",")]
            # Convert empty values to dict (for nested structures)
            elif not value:
                # Create dict for nested key-value structures
                value = {}
                # Push with indent + 2 to indicate children will be at that level
                stack.append((indent + 2, value))
                current_dict[key] = value
                continue

            current_dict[key] = value

    return result


def render_template(template_content: str, context: dict, env: Environment) -> str:
    """Render template using Jinja2 with proper whitespace control."""
    # Create a temporary template from string
    template = env.from_string(template_content)
    return template.render(**context)


def build_agent(j2_file: Path, env: Environment) -> None:
    """Build a single agent from .j2 definition file."""

    # Read .j2 file
    with open(j2_file, "r") as f:
        content = f.read()

    # Split into YAML config and template at "---" separator
    parts = content.split("---\n", 1)
    if len(parts) != 2:
        print(f"⚠ Skip {j2_file.name}: missing '---' separator between config and template")
        return

    yaml_content, template_content = parts

    # Parse YAML config
    config = parse_yaml_simple(yaml_content)
    meta = config.get("meta", {})

    if not meta:
        print(f"⚠ Skip {j2_file.name}: no meta section in YAML")
        return

    # Extract frontmatter fields
    name = meta.get("name", "agent")
    description = meta.get("description", "")
    model = meta.get("model", "sonnet")

    # Format tools (must be list of strings)
    tools_list = meta.get("tools", [])
    if isinstance(tools_list, list):
        tools_filtered = [t for t in tools_list if isinstance(t, str)]
        tools_str = ", ".join(tools_filtered)
    else:
        tools_str = str(tools_list)

    # Create YAML frontmatter
    frontmatter = f"""---
name: {name}
description: {description}
tools: {tools_str}
model: {model}
---

"""

    # Render template
    context = {"meta": meta}
    rendered = render_template(template_content, context, env)

    # Write output with frontmatter
    output_name = meta.get("output_name", name)
    output_file = AGENTS_DIR / f"{output_name}.md"

    with open(output_file, "w") as f:
        f.write(frontmatter)
        f.write(rendered)

    print(f"✓ {j2_file.name} → {output_file.name}")


def main() -> None:
    """Build all or specific agents."""

    if not AGENTS_DIR.exists():
        print(f"Error: {AGENTS_DIR} not found")
        sys.exit(1)

    # Create Jinja2 environment with proper whitespace control
    # Using default whitespace behavior to preserve structure
    env = Environment(
        loader=FileSystemLoader(str(AGENTS_DIR)),
        keep_trailing_newline=False,  # Don't preserve trailing newline from templates
    )

    # Determine which agents to build
    if len(sys.argv) > 1:
        # Build specific agent
        agent_name = sys.argv[1]
        j2_file = AGENTS_DIR / f"{agent_name}.j2"

        if not j2_file.exists():
            print(f"Error: {j2_file} not found")
            sys.exit(1)

        build_agent(j2_file, env)
    else:
        # Build all agents
        j2_files = sorted(AGENTS_DIR.glob("*.j2"))

        if not j2_files:
            print(f"No .j2 files found in {AGENTS_DIR}")
            sys.exit(1)

        print(f"Building {len(j2_files)} agent(s)...\n")

        for j2_file in j2_files:
            build_agent(j2_file, env)

        print(f"\n✓ Complete: {len(j2_files)} agent(s) built")


if __name__ == "__main__":
    main()
