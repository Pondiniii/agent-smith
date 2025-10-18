#!/usr/bin/env python3
"""
Regenerate agent markdown files from YAML config + template files.

Structure:
    .claude/agents/
    ├── orchestrator.yaml          ← Config
    ├── orchestrator.md            ← Generated output
    └── templates/
        └── orchestrator.md.j2     ← Template

Minimalist version with no external dependencies.

Usage:
    python build_agents.py              # Build all agents
    python build_agents.py orchestrator # Build specific agent
"""

import sys
import re
from pathlib import Path


AGENTS_DIR = Path(".claude/agents")
AGENTS_TEMPLATES_DIR = AGENTS_DIR / "templates"
AGENTS_SRC_DIR = AGENTS_DIR  # YAML files live in .claude/agents/
AGENTS_OUT_DIR = AGENTS_DIR  # Output MD files also go here


def parse_yaml_simple(content: str) -> dict:
    """Simple YAML parser for basic key: value and nested structures."""
    result = {}
    stack = [(0, result)]  # (indent_level, dict)

    for line in content.split("\n"):
        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith("#"):
            continue

        # Calculate indentation
        indent = len(line) - len(line.lstrip())

        # Pop stack if indentation decreased
        while len(stack) > 1 and indent < stack[-1][0]:
            stack.pop()

        # Parse key: value
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

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
                value = {}
                stack.append((indent, value))

            current_dict[key] = value

    return result


def render_template(template_content: str, context: dict, templates_dir: Path = None) -> str:
    """Simple template renderer using {{ }} substitution and {% include %} directives."""
    if templates_dir is None:
        templates_dir = AGENTS_TEMPLATES_DIR

    output = template_content

    # Process {% include "path" %} directives
    import re as regex
    include_pattern = r'{%\s*include\s+"([^"]+)"\s*%}'
    for match in regex.finditer(include_pattern, output):
        include_path = match.group(1)
        full_path = templates_dir / include_path

        if full_path.exists():
            with open(full_path, "r") as f:
                included_content = f.read()
            # Recursively render included content
            included_content = render_template(included_content, context, templates_dir)
            output = output.replace(match.group(0), included_content)
        else:
            print(f"⚠ Warning: include file not found: {include_path}")

    # Replace {{ key }} with values from context
    for key, value in context.items():
        placeholder = f"{{{{ {key} }}}}"
        if isinstance(value, (list, dict)):
            replacement = str(value)
        else:
            replacement = str(value)
        output = output.replace(placeholder, replacement)

    # Replace {{ meta.key }} patterns
    for key, value in context.get("meta", {}).items():
        placeholder = f"{{{{ meta.{key} }}}}"
        if isinstance(value, (list, dict)):
            replacement = str(value)
        else:
            replacement = str(value)
        output = output.replace(placeholder, replacement)

    return output


def build_agent(yaml_file: Path) -> None:
    """Build a single agent from YAML + template."""

    # Load YAML config
    with open(yaml_file, "r") as f:
        config = parse_yaml_simple(f.read())

    source_file = config.get("source_file")
    meta = config.get("meta", {})

    if not source_file:
        print(f"⚠ Skip {yaml_file.name}: no source_file specified")
        return

    # Load template
    # Handle both relative and absolute paths
    if "/" in source_file:
        template_path = Path(source_file)
    else:
        template_path = AGENTS_TEMPLATES_DIR / source_file

    if not template_path.exists():
        print(f"⚠ Skip {yaml_file.name}: template not found at {template_path}")
        return

    # Read template
    with open(template_path, "r") as f:
        template_content = f.read()

    # Render template
    context = {"meta": meta, **meta}
    rendered = render_template(template_content, context)

    # Write output
    output_name = meta.get("output_name", meta.get("name", "agent"))
    output_file = AGENTS_OUT_DIR / f"{output_name}.md"

    with open(output_file, "w") as f:
        f.write(rendered)

    print(f"✓ {yaml_file.name} → {output_file.name}")


def main() -> None:
    """Build all or specific agents."""

    if not AGENTS_SRC_DIR.exists():
        print(f"Error: {AGENTS_SRC_DIR} not found")
        sys.exit(1)

    if not AGENTS_TEMPLATES_DIR.exists():
        print(f"Error: {AGENTS_TEMPLATES_DIR} not found")
        sys.exit(1)

    # Determine which agents to build
    if len(sys.argv) > 1:
        # Build specific agent
        agent_name = sys.argv[1]
        yaml_file = AGENTS_SRC_DIR / f"{agent_name}.yaml"

        if not yaml_file.exists():
            print(f"Error: {yaml_file} not found")
            sys.exit(1)

        build_agent(yaml_file)
    else:
        # Build all agents
        yaml_files = sorted(AGENTS_SRC_DIR.glob("*.yaml"))

        if not yaml_files:
            print(f"No YAML files found in {AGENTS_SRC_DIR}")
            sys.exit(1)

        print(f"Building {len(yaml_files)} agent(s)...\n")

        for yaml_file in yaml_files:
            build_agent(yaml_file)

        print(f"\n✓ Complete: {len(yaml_files)} agent(s) built")


if __name__ == "__main__":
    main()
