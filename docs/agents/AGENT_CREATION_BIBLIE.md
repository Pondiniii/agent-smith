# The Ultimate Guide to Writing Golden Claude Code Agents

**Complete Guide to Building Production-Grade AI Agents for ~/.claude/**

Version: 1.0  
Last Updated: 2025-10-18  
Author: Based on extensive agent engineering research and production deployments

---

## Table of Contents

1. [Philosophy & Core Principles](#philosophy--core-principles)
2. [Agent Anatomy](#agent-anatomy)
3. [The Bible: Size, Structure, Quality Rules](#the-bible-size-structure-quality-rules)
4. [YAML Frontmatter Specification](#yaml-frontmatter-specification)
5. [Agent Types & Archetypes](#agent-types--archetypes)
6. [Writing System Prompts](#writing-system-prompts)
7. [Context Budget Management](#context-budget-management)
8. [Tool Selection & Usage](#tool-selection--usage)
9. [Agent Communication Patterns](#agent-communication-patterns)
10. [Process Definition](#process-definition)
11. [Quality Checklists](#quality-checklists)
12. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
13. [Testing Agents](#testing-agents)
14. [Example Agents Breakdown](#example-agents-breakdown)
15. [Advanced Patterns](#advanced-patterns)
16. [Troubleshooting](#troubleshooting)
17. [Production Deployment](#production-deployment)

---

## Philosophy & Core Principles

### The Golden Rules

**1. Every Agent Has ONE Job**
- Single Responsibility Principle (SOLID)
- Clear, focused mission
- No feature creep
- If it does too much, split it

**Example:**
```markdown
❌ BAD: "code-writer-reviewer-tester"
✅ GOOD: "swe-agent" (writes), "code-tester" (tests), "code-reviewer" (reviews)
```

**2. Minimalism Over Completeness**
- KISS (Keep It Simple, Stupid)
- Cut everything non-essential
- Shorter = faster = cheaper = better
- Question: "Do I REALLY need this section?"

**3. Agents Are Accountable**
- Bad agent = expensive mistakes downstream
- Every decision has consequences
- Quality > speed
- Think: "Would I trust this in production?"

**4. Communication Is Key**
- Agents work in pipelines
- Clear input/output contracts
- Explicit escalation paths
- Human-like communication

**5. Zero Tolerance for Ambiguity**
- Vague instructions = random behavior
- Every step should be deterministic
- When in doubt, ask (don't guess)
- Examples > explanations

### The "Murphy's Law" Mindset

**Assume everything will break:**
- Users will send malformed input
- Networks will timeout
- Files won't exist
- Dependencies will conflict
- Memory will run out

**Design agents to survive chaos.**

---

## Agent Anatomy

### Basic Structure

```markdown
---
name: agent-name
description: One-sentence purpose. When to use this agent.
tools: [read_file, write_file, edit_file, glob, grep, bash]
model: sonnet
---

# System Prompt

You are **Agent Name** - clear role definition.

## Mission
[2-3 sentences: what you do and why it matters]

## Core Principles
[3-5 key philosophies]

## Process
[Step-by-step workflow]

## Quality Checklist
[Verification steps]

## Anti-Patterns
[What NOT to do]

## Output Format
[Expected deliverables]

## Context Budgets
- Keep <X% context (phase 1)
- Keep <Y% context (phase 2)
```

### Required Sections

**Minimum viable agent:**
1. **YAML frontmatter** - metadata
2. **Mission** - what & why
3. **Process** - how (step-by-step)
4. **Output Format** - deliverables
5. **Context Budgets** - resource limits

**Recommended additions:**
6. **Core Principles** - philosophy
7. **Quality Checklist** - verification
8. **Anti-Patterns** - what to avoid
9. **Examples** - concrete demonstrations (max 1)

---

## The Bible: Size, Structure, Quality Rules

### Size Constraints

**Target Sizes:**
- Minimum: 5KB
- Sweet spot: 8-12KB
- Maximum: 15KB
- Absolute max: 20KB

**Why these limits?**
- Faster loading
- Less token consumption
- Forces clarity
- Easier to maintain

**Measuring size:**
```bash
wc -c ~/.claude/agents/your-agent.md
# Target: 8000-12000 bytes
```

### Compression Techniques

**1. Replace Paragraphs with Bullets**
```markdown
❌ BAD (wordy):
The agent should carefully analyze the input data by first reading 
all relevant files, then processing them through validation logic, 
and finally generating appropriate output based on the analysis.

✅ GOOD (concise):
- Read input files
- Validate data
- Generate output
```

**2. Merge Redundant Sections**
```markdown
❌ BAD (duplicate):
## Quality Standards
[list of standards]

## Verification Steps  
[same standards repeated]

✅ GOOD (merged):
## Quality Checklist
[combined list with checkboxes]
```

**3. Use Examples Sparingly**
- Maximum 1 example per agent
- Keep examples short (<30 lines)
- Focus on pattern, not completeness

**4. Remove Filler Words**
```markdown
❌ "It is important to carefully consider..."
✅ "Consider..."

❌ "You should probably try to..."
✅ "Do..."

❌ "In order to achieve the goal of..."
✅ "To..."
```

**5. Consolidate Headers**
```markdown
❌ BAD (too many):
## Step 1: Preparation
## Step 2: Execution
## Step 3: Validation
## Step 4: Reporting
## Step 5: Cleanup

✅ GOOD (grouped):
## Process
1. Prepare
2. Execute
3. Validate
4. Report
```

### The "One Example" Rule

**Why only one example?**
- Examples are expensive (token-wise)
- Multiple examples create confusion
- One good example > three mediocre ones

**When to include an example:**
- Complex pattern that's hard to explain
- Common mistake you're preventing
- Critical output format

**When to skip examples:**
- Simple, self-explanatory tasks
- Standard programming patterns
- Already shown in other agents

### Context Budget Allocation

**Standard budget breakdown:**
```markdown
## Context Budgets
- Keep <20% context (exploration/understanding)
- Keep <15% context (planning)
- Keep <40% context (implementation/execution)
- Keep <20% context (review/verification)
- Keep <5% context (reporting/finalization)
```

**Adjust based on agent type:**

**For Routers (orchestrator, project-manager):**
```markdown
- Keep <30% context (state detection)
- Keep <20% context (routing decision)
- Keep <25% context (validation)
- Keep <25% context (reporting)
```

**For Builders (swe-agent, solution-architect):**
```markdown
- Keep <15% context (understanding requirements)
- Keep <10% context (planning approach)
- Keep <50% context (building/implementing)
- Keep <15% context (testing)
- Keep <10% context (documentation)
```

**For Reviewers (code-reviewer, code-tester):**
```markdown
- Keep <10% context (setup)
- Keep <60% context (analysis/checking)
- Keep <20% context (report generation)
- Keep <10% context (feedback delivery)
```

---

## YAML Frontmatter Specification

### Required Fields

```yaml
---
name: agent-name
description: |
  Brief description of what agent does.
  When to use this agent.
  Key capabilities.
tools: [read_file, write_file, edit_file, glob, grep, bash]
model: sonnet
---
```

### Field Specifications

**`name:`**
- Lowercase, hyphen-separated
- Descriptive, not generic
- Examples: `swe-agent`, `solution-architect`, `code-tester`
- NOT: `agent1`, `helper`, `utility`

**`description:`**
- 1-3 sentences maximum
- Focus on WHEN to use (trigger conditions)
- Include key capabilities
- Skip obvious information

Good description pattern:
```yaml
description: |
  [Role]. [Primary function]. [Key constraint/philosophy].
  Use when [trigger condition].
```

Example:
```yaml
description: |
  Senior architect with 15+ years experience. Creates detailed 
  technical designs from project-manager's requirements.
  Minimalist, SOLID approach. Use after plan.md is created.
```

**`tools:`**
- List only tools you actually use
- Order by frequency of use
- Common tools:
  - `read_file` - reading files
  - `write_file` - creating new files
  - `edit_file` - modifying existing files
  - `glob` - finding files by pattern
  - `grep` - searching file contents
  - `bash` - running shell commands

Minimal toolset example:
```yaml
tools: [read_file, write_file]  # Document reader/writer
```

Full toolset example:
```yaml
tools: [read_file, write_file, edit_file, glob, grep, bash]  # Builder
```

**`model:`**
- Usually `sonnet` (fast, capable)
- Use `opus` only for complex reasoning
- Never hardcode specific versions

### Optional Fields

```yaml
color: blue  # UI color hint (optional)
```

---

## Agent Types & Archetypes

### 1. Router Agents

**Purpose:** Detect state, make decisions, delegate to other agents

**Characteristics:**
- NO implementation work
- State-driven decision making
- Clear routing logic
- Validation of prerequisites

**Template:**
```markdown
## Mission
Route users to appropriate specialist based on [state/conditions].

## Rules
1. You Are a Router, Not a Worker
   - Detect state
   - Recommend next agent
   - Validate prerequisites
   - DON'T do the work yourself

## Process
1. Check current state
2. Determine next action (decision tree/matrix)
3. Validate prerequisites
4. Route to specialist
5. Report status

## Routing Decision Matrix
| Condition | Route To | Reason |
|-----------|----------|--------|
| X exists  | agent-a  | Because Y |
| X missing | agent-b  | Because Z |
```

**Examples:**
- `i2dr-orchestrator` - Routes I2DR workflow stages
- `project-manager` - Delegates to solution-architect, swe-agent, etc.

### 2. Generator Agents

**Purpose:** Create artifacts from requirements

**Characteristics:**
- Takes input specification
- Produces output artifact
- Quality validation built-in
- Iterative refinement

**Template:**
```markdown
## Mission
Generate [artifact type] from [input type].

## Input Requirements
- Required: [list]
- Optional: [list]

## Process
1. Validate input
2. Generate artifact
3. Self-review
4. Save to [location]

## Output Format
[Exact structure/schema]

## Quality Checklist
- [ ] Meets requirements
- [ ] Follows format
- [ ] No errors
- [ ] Ready for next stage
```

**Examples:**
- `swe-agent` - Generates code from architecture
- `docs-builder` - Generates documentation from features
- `solution-architect` - Generates architecture from requirements

### 3. Reviewer Agents

**Purpose:** Validate quality, provide feedback

**Characteristics:**
- Specific quality criteria
- Binary decisions (approve/reject)
- Actionable feedback
- Fast execution

**Template:**
```markdown
## Mission
Review [artifact type] for [quality aspects].

## Review Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Process
1. Load artifact
2. Check each criterion
3. Generate report
4. Decide: APPROVE or REJECT with fixes

## Output Format
### Status: [APPROVED | REJECTED]

**Issues Found:** [count]
[Specific, actionable feedback]

**Fixes Required:**
1. [Exact change needed]
2. [Exact change needed]
```

**Examples:**
- `code-tester` - Fast smoke tests (compile, test, warnings)
- `code-reviewer` - Deep quality review (SOLID, security, architecture)

### 4. Transformer Agents

**Purpose:** Convert from format A to format B

**Characteristics:**
- Clear input/output formats
- Lossless transformation (when possible)
- Validation on both ends
- Idempotent (same input → same output)

**Template:**
```markdown
## Mission
Transform [format A] to [format B].

## Input Format
[Schema/structure]

## Output Format
[Schema/structure]

## Transformation Rules
1. [Mapping rule]
2. [Mapping rule]
3. [Edge case handling]

## Validation
- Input: [checks]
- Output: [checks]
```

**Examples:**
- `agent-builder` - Transforms brief → agent.md
- (Potential) `spec-to-tests` - Transforms requirements → test cases

### 5. Utility Agents

**Purpose:** Perform specific, narrow tasks

**Characteristics:**
- Single, well-defined function
- Fast execution
- Minimal side effects
- Composable with others

**Template:**
```markdown
## Mission
[One specific task].

## Usage
When [condition], use this agent to [action].

## Process
1. [Simple step]
2. [Simple step]
3. [Simple step]

## Output
[Simple result format]
```

**Examples:**
- (Potential) `file-finder` - Locates files by criteria
- (Potential) `dependency-checker` - Validates dependencies
- (Potential) `format-checker` - Validates formatting

---

## Writing System Prompts

### Opening Statement

**Pattern:**
```markdown
# System Prompt

You are **[Agent Name]** - [one-sentence role with impact statement].
```

**Examples:**

Strong opening:
```markdown
You are **Solution Architect** - a senior technical architect with 15+ 
years of experience. Your decisions have cascading impact: bad design = 
expensive fixes later. Take time to design well.
```

Weak opening:
```markdown
You are an assistant that helps with architecture.
```

### Mission Section

**Purpose:** Answer "What do I do and why does it matter?"

**Pattern:**
```markdown
## Mission

[Primary objective in 1-2 sentences]

Key responsibilities:
- [Responsibility 1 with outcome]
- [Responsibility 2 with outcome]
- [Responsibility 3 with outcome]

[Why this matters / impact statement]
```

**Example:**
```markdown
## Mission

Transform project-manager's high-level plan into detailed, actionable 
technical design for swe-agent.

Key responsibilities:
- Break requirements into components with clear boundaries
- Choose optimal tech stack with justified decisions
- Create step-by-step implementation guide
- Document architecture decisions (ADRs)

Your responsibility is critical: bad architecture = expensive fixes during 
code-review loop. Quality over speed.
```

### Core Principles Section

**Purpose:** Establish philosophical foundation

**Pattern:**
```markdown
## Core Principles

### 1. [Principle Name]
[What it means]
[Why it matters]
[How to apply]

### 2. [Principle Name]
[Same structure]
```

**Good principles:**
- KISS (Keep It Simple, Stupid)
- SOLID (for code agents)
- Murphy's Law (defensive programming)
- DRY (Don't Repeat Yourself)
- Minimalism
- Composition over Inheritance

**Example:**
```markdown
## Core Principles

### 1. Minimalism (KISS)
Simplest solution that works is the best solution.
- No over-engineering
- No premature optimization  
- Question: "Can we solve this simpler?"

### 2. Murphy's Law
If it can fail, it will fail.
- Validate all inputs
- Handle all error cases
- Plan fallback for every operation
- Assume: files missing, network down, disk full
```

### Process Section

**Purpose:** Step-by-step execution guide

**Pattern:**
```markdown
## Process

### Phase 1: [Name] (X% context)

[Brief description of what happens]

**Steps:**
1. [Action verb] [object]
2. [Action verb] [object]
3. [Action verb] [object]

**Output:** [What's produced]

### Phase 2: [Name] (Y% context)

[Repeat pattern]
```

**Best practices:**
- Number phases (1, 2, 3...)
- Use action verbs (Validate, Generate, Check)
- Include context budget per phase
- Show inputs and outputs clearly
- Keep each phase focused

**Example:**
```markdown
## Process

### Phase 1: Understand Requirements (15% context)

Read input documents and extract key information.

**Steps:**
1. Read plan.md from project-manager
2. Extract MUST-have features
3. Identify technical constraints
4. Note success criteria

**Output:** Requirements summary

**If unclear:** Ask project-manager specific questions.

### Phase 2: Design Architecture (40% context)

Create detailed technical design.

**Steps:**
1. Break into components (single responsibility)
2. Choose tech stack with justification
3. Define interfaces between components
4. Document data models
5. Design error handling strategy

**Output:** architecture.md (8-10KB)
```

### Quality Checklist Section

**Purpose:** Verification before completion

**Pattern:**
```markdown
## Quality Checklist

### Before Starting
- [ ] Input validated
- [ ] Requirements clear
- [ ] Dependencies available

### During Work
- [ ] Following process steps
- [ ] Staying within context budgets
- [ ] Making decisions (not guessing)

### Before Completion
- [ ] Output meets format
- [ ] All requirements satisfied
- [ ] No errors or warnings
- [ ] Ready for next agent
```

**Tips:**
- Group by phase
- Make items binary (yes/no)
- Be specific ("All tests pass" not "Tests good")
- Include critical-path items only

### Anti-Patterns Section

**Purpose:** Explicit "don't do this" warnings

**Pattern:**
```markdown
## Anti-Patterns

❌ **Never:**
- [Bad pattern 1] ([why it's bad])
- [Bad pattern 2] ([why it's bad])
- [Bad pattern 3] ([why it's bad])

✅ **Always:**
- [Good pattern 1] ([why it's good])
- [Good pattern 2] ([why it's good])
```

**Example:**
```markdown
## Anti-Patterns

❌ **Never:**
- Skip input validation (leads to cascade failures)
- Use unwrap() in production Rust (can panic)
- Hardcode secrets (security risk)
- Ignore error return values (NASA rule violation)
- Write functions >60 lines (hard to test)

✅ **Always:**
- Validate at boundaries
- Use Result/Option for errors
- Load secrets from environment
- Check all return values
- Keep functions small and focused
```

### Output Format Section

**Purpose:** Define exact deliverable structure

**Pattern:**
```markdown
## Output Format

When complete, deliver:

```markdown
[Exact template or structure]
```

**Required fields:**
- [Field 1]: [specification]
- [Field 2]: [specification]

**Optional fields:**
- [Field 3]: [when to include]
```

**Example:**
```markdown
## Output Format

When complete, deliver:

```markdown
## Implementation Complete: [Module Name]

**Files Created/Modified:**
- path/to/file.ext (X lines) - [purpose]

**Test Results:**
- Tests: X/X passing
- Coverage: X%
- Warnings: 0

**Status:** Ready for code-reviewer
```

**Required fields:**
- Files list with sizes
- Test results summary
- Zero warnings confirmation

**Optional fields:**
- Known issues (if any)
- Deviations from architecture (with reasons)
```

---

## Context Budget Management

### Why Context Budgets Matter

**Problem:** Agents can consume unlimited context → expensive + slow

**Solution:** Explicit budgets per phase

**Benefits:**
- Predictable costs
- Faster execution
- Forces conciseness
- Easier debugging

### Budget Calculation

**Total context = 100%**

**Typical distribution:**
```
Exploration/Understanding:  15-20%
Planning:                   10-15%
Execution/Implementation:   40-50%
Review/Validation:         15-20%
Reporting/Finalization:     5-10%
```

**Adjust based on agent type:**

**Heavy thinkers (architect, reviewer):**
```
Understanding: 20%
Planning:      20%
Execution:     30%
Review:        20%
Finalization:  10%
```

**Heavy builders (swe-agent, generator):**
```
Understanding: 10%
Planning:      5%
Execution:     60%
Review:        15%
Finalization:  10%
```

**Routers (orchestrator):**
```
State Detection: 30%
Decision:        20%
Validation:      25%
Reporting:       25%
```

### Enforcing Budgets

**In agent prompt:**
```markdown
## Context Budgets
- Keep <15% context (understanding phase)
- Keep <40% context (implementation phase)
- Keep <20% context (review phase)

**Warning:** Exceeding budgets increases costs and latency.
```

**Monitor adherence:**
- Check actual token usage in logs
- Compare against budgets
- Refactor if consistently over

---

## Tool Selection & Usage

### Available Tools

**File Operations:**
- `read_file` - Read file contents
- `write_file` - Create new file (overwrites if exists)
- `edit_file` - Modify existing file
- `glob` - Find files matching pattern
- `grep` - Search file contents

**Command Execution:**
- `bash` - Run shell commands

**Internal (if available):**
- `task_tool` - Launch other agents (check if supported)
- `web_search` - Search web (for research agents)
- `web_fetch` - Fetch web content

### Tool Selection Matrix

| Agent Type | Typical Tools | Reason |
|------------|---------------|--------|
| Router | read_file, bash | State detection only |
| Generator | write_file, read_file | Create artifacts |
| Reviewer | read_file, glob, grep | Analyze existing code |
| Builder | All file ops + bash | Full construction |
| Tester | bash, read_file, grep | Run tests, parse results |

### Minimal Toolsets

**Document reader:**
```yaml
tools: [read_file]
```

**Document writer:**
```yaml
tools: [read_file, write_file]
```

**Code builder:**
```yaml
tools: [read_file, write_file, edit_file, glob, grep, bash]
```

**Orchestrator:**
```yaml
tools: [read_file, bash]  # Minimal: just check state
```

### Tool Usage Patterns

**Reading files safely:**
```bash
# Check if file exists first
if [ -f "path/to/file" ]; then
    read_file path/to/file
else
    echo "File not found: path/to/file"
fi
```

**Finding files:**
```bash
# Use glob for patterns
glob 'src/**/*.rs'
glob 'tests/test_*.py'

# Use grep to search content
grep -r "function_name" src/
```

**Running commands safely:**
```bash
# Always check exit codes
cargo build
if [ $? -ne 0 ]; then
    echo "Build failed"
    exit 1
fi

# Or use set -e for auto-exit on error
set -e
cargo build
cargo test
```

**Writing files with backup:**
```bash
# For critical files, backup first
if [ -f "important.md" ]; then
    cp important.md important.md.backup
fi
write_file important.md "new content"
```

### Tool Limitations

**Cannot do:**
- Network requests (except via bash + curl)
- GUI operations
- Persistent state between runs
- File system modifications outside project

**Workarounds:**
- Network: Use `bash` with `curl` or `wget`
- State: Write to files in project
- Large operations: Break into steps

---

## Agent Communication Patterns

### Communication Types

**1. Human ↔ Agent**
- User provides input
- Agent produces output
- Agent asks for clarification

**2. Agent ↔ Agent (via Human)**
- Agent A produces artifact
- Human passes to Agent B
- Agent B uses artifact as input

**3. Agent ↔ Agent (via Files)**
- Agent A writes file (e.g., plan.md)
- Agent B reads same file
- Shared state via filesystem

**4. Agent ↔ Agent (via Task Tool)**
- Agent A calls task_tool to launch Agent B
- Agent B executes
- Result returned to Agent A
- (Check if supported in your environment)

### Designing Clear Contracts

**Input Contract:**
```markdown
## Input Requirements

**Required files:**
- plan.md - Project requirements from project-manager
- architecture.md - Technical design from solution-architect

**File format:**
- plan.md must have sections: Goals, Features, Success Criteria
- architecture.md must have sections: Components, Tech Stack

**If missing:** Ask [specific agent] to provide [specific file]
```

**Output Contract:**
```markdown
## Output Deliverables

**Files created:**
- src/**/*.rs - Implementation files
- tests/**/*.rs - Test files
- Cargo.toml - Dependency manifest

**Report format:**
```markdown
## Implementation Complete: [Module]
**Files:** [list]
**Tests:** [status]
**Status:** Ready for [next agent]
```
```

### Agent-to-Agent Messages

**Pattern:**
```markdown
## Communication with [Other Agent]

### When You Need Input
Message: "Hey [agent-name], need [specific thing]. 
Can you provide [exact requirement]?"

### When You Deliver Output
Message: "Done! Created [artifacts]. 
[Brief summary]. 
Ready for [next agent]."

### When You Find Issues
Message: "Found issue in [artifact] from [agent]. 
Specifically: [exact problem].
Fix: [specific change needed].
Can you update?"
```

**Example:**
```markdown
## Communication with swe-agent

### When Tests Fail
Message: "Hey swe-agent,

Quick test results: ❌ Code doesn't compile

Found 2 errors in `src/auth/user_auth.rs`:
- Line 78: Missing `Ok()` wrapper
- Line 92: Remove `&` from `&user.email`

These are 1-minute fixes. Want me to show exact code?"

### When Tests Pass
Message: "Hey swe-agent,

Tests passed! ✅
- Compilation: clean
- Tests: 18/18 passing
- Warnings: 0

Code looks good, passing to code-reviewer."
```

### Escalation Paths

**When to ask human:**
- Ambiguous requirements
- Critical decisions (architecture, tech stack)
- Conflicting information
- Budget/timeline concerns
- Security-critical choices

**When to ask other agent:**
- Missing expected artifact
- Unclear format/specification
- Issues in their output
- Need additional context

**Pattern:**
```markdown
## Escalation

### Ask Human When:
- [Condition 1] → "Need decision on [X]"
- [Condition 2] → "Requirement [Y] is ambiguous"

### Ask [Other Agent] When:
- [Condition 1] → "[Agent], need [specific thing]"
- [Condition 2] → "[Agent], [artifact] has [issue]"

### Never:
- Guess at critical decisions
- Proceed with incomplete information
- Ignore errors or warnings
```

---

## Process Definition

### Step-by-Step Pattern

**Template:**
```markdown
## Process

### Step 1: [Action Name]

**Purpose:** [What this step achieves]

**Actions:**
1. [Concrete action]
2. [Concrete action]
3. [Concrete action]

**Validation:**
- [Check 1]
- [Check 2]

**Output:** [What's produced]

**If problem:** [What to do]

### Step 2: [Next Action]
[Repeat pattern]
```

**Example:**
```markdown
## Process

### Step 1: Validate Input

**Purpose:** Ensure we have everything needed

**Actions:**
1. Check plan.md exists: `test -f plan.md`
2. Verify required sections: Goals, Features, Success Criteria
3. Extract MUST-have features (count >= 3)

**Validation:**
- plan.md is readable
- All sections present
- At least 3 MUST features

**Output:** Requirements summary

**If problem:** Ask project-manager for complete plan.md

### Step 2: Design Components

**Purpose:** Break system into modules

**Actions:**
1. List features from plan.md
2. Group by domain (auth, api, db, etc.)
3. Define one module per group
4. Specify module interface (public functions)

**Validation:**
- Each module has single responsibility
- Interfaces are clear
- Dependencies are minimal

**Output:** Component list with interfaces

**If problem:** If >10 modules, reconsider grouping.
```

### Decision Points

**Pattern:**
```markdown
## Decision Logic

**If [condition]:**
- Then: [action]
- Because: [reason]

**Else if [condition]:**
- Then: [action]
- Because: [reason]

**Else:**
- Then: [default action]
```

**Example:**
```markdown
## Decision Logic

**If tests pass and warnings == 0:**
- Then: APPROVE, send to code-reviewer
- Because: Code meets basic quality

**Else if tests pass but warnings > 0:**
- Then: REJECT, send back to swe-agent
- Because: Zero warnings policy

**Else if tests fail:**
- Then: REJECT with specific fixes
- Because: Broken code blocks pipeline

**Else:**
- Then: ERROR, escalate to human
- Because: Unexpected state
```

### Loops and Iteration

**Pattern:**
```markdown
## Iteration Pattern

**Loop:** While [condition] not met, max [N] iterations

**Each iteration:**
1. [Try action]
2. [Check result]
3. [If success] → exit loop
4. [If failure] → adjust approach

**Exit conditions:**
- Success: [specific state]
- Failure: [max iterations reached]
- Error: [unexpected problem]

**After loop:**
- If success: [next step]
- If failure: [escalation]
```

**Example:**
```markdown
## Retry Pattern

**Loop:** While compilation fails, max 3 attempts

**Each attempt:**
1. Run `cargo build`
2. Parse error messages
3. If compile success → exit loop
4. If compile error → apply common fixes:
   - Add missing imports
   - Fix obvious typos
   - Adjust types

**Exit conditions:**
- Success: `cargo build` returns 0
- Failure: 3 attempts exhausted
- Error: Unrecognizable error format

**After loop:**
- If success: Proceed to tests
- If failure: Report to swe-agent with errors
```

---

## Quality Checklists

### Checklist Structure

**Pattern:**
```markdown
## Quality Checklist

### Category 1: [Name]
- [ ] [Specific, measurable criterion]
- [ ] [Specific, measurable criterion]
- [ ] [Specific, measurable criterion]

### Category 2: [Name]
- [ ] [Specific, measurable criterion]
- [ ] [Specific, measurable criterion]
```

### Categories by Agent Type

**For Generators (swe-agent, docs-builder):**
```markdown
## Quality Checklist

### Completeness
- [ ] All required files created
- [ ] All sections filled (no TODOs)
- [ ] Dependencies documented

### Correctness
- [ ] Compiles/parses without errors
- [ ] Tests pass (if applicable)
- [ ] Follows specification exactly

### Quality
- [ ] Follows style guide
- [ ] No warnings
- [ ] Includes error handling
- [ ] Has docstrings/comments

### Deliverables
- [ ] Output format matches specification
- [ ] Ready for next agent
- [ ] Report generated
```

**For Reviewers (code-tester, code-reviewer):**
```markdown
## Quality Checklist

### Analysis Completeness
- [ ] All files reviewed
- [ ] All criteria checked
- [ ] Edge cases considered

### Decision Clarity
- [ ] APPROVE or REJECT clearly stated
- [ ] Reasons provided for decision
- [ ] Specific fixes listed (if rejected)

### Feedback Quality
- [ ] Actionable (not vague)
- [ ] Specific (file, line, exact change)
- [ ] Prioritized (critical vs nice-to-have)
```

**For Routers (orchestrator, project-manager):**
```markdown
## Quality Checklist

### State Detection
- [ ] Current state accurately identified
- [ ] All required artifacts checked
- [ ] Dependencies satisfied

### Routing Decision
- [ ] Correct next agent selected
- [ ] Prerequisites validated
- [ ] Fallback plan if agent unavailable

### Communication
- [ ] Clear instructions for next agent
- [ ] Context provided
- [ ] Expected output specified
```

### Making Criteria Measurable

**❌ Vague:**
- Code quality is good
- Tests are adequate
- Documentation is sufficient

**✅ Specific:**
- No functions >60 lines
- Test coverage >80%
- All public functions have docstrings

**Pattern:**
- Use numbers where possible
- Use binary (yes/no) criteria
- Reference specific locations/files
- Define "done" explicitly

---

## Anti-Patterns to Avoid

### Agent Design Anti-Patterns

**1. The Swiss Army Knife**
```markdown
❌ Agent that does everything:
- Writes code
- Reviews code
- Tests code
- Deploys code
- Writes documentation
- Manages project

✅ Separate agents:
- swe-agent (writes)
- code-reviewer (reviews)
- code-tester (tests)
- docs-builder (documents)
```

**2. The Oracle**
```markdown
❌ Agent that "knows" information not in prompt:
"As we discussed earlier..." (no prior discussion)
"According to your preferences..." (never specified)

✅ Agent that asks:
"What are your preferences for [X]?"
"Need clarification on [Y]"
```

**3. The Guesser**
```markdown
❌ Agent that assumes when unclear:
"I'll assume you want Python 3.11"
"Probably means PostgreSQL"

✅ Agent that asks:
"Python version not specified. Please specify: 3.9, 3.10, 3.11?"
"Database choice unclear. Options: PostgreSQL, MySQL, SQLite?"
```

**4. The Over-Explainer**
```markdown
❌ Verbose agent (15KB):
- 5 paragraphs of introduction
- Detailed history of the technology
- Philosophy discussions
- Multiple examples for simple concepts

✅ Concise agent (8KB):
- 2 sentences of introduction
- Direct process steps
- One example if needed
- Bullet points over paragraphs
```

**5. The Approval Junkie**
```markdown
❌ Agent that asks permission for everything:
"Should I read the file?"
"OK to create a variable?"
"Can I use a for loop?"

✅ Agent that executes autonomously:
(Reads file, creates code, follows process)
Only asks for: ambiguous requirements, critical decisions
```

### Process Anti-Patterns

**1. The Novelist**
```markdown
❌ Long narrative process:
"First, you should carefully consider reading the input file, 
taking into account the various factors that might affect..."

✅ Bullet point process:
1. Read input file
2. Validate format
3. Extract data
```

**2. The Assumption Maker**
```markdown
❌ Assumes tools/capabilities not listed:
Uses `docker` command (not in tools)
Calls external APIs (not available)

✅ Uses only specified tools:
tools: [read_file, write_file, bash]
(Only uses these three)
```

**3. The Bottleneck**
```markdown
❌ Process with sequential dependencies:
Step 1 → Step 2 → Step 3 → Step 4 → Step 5
(Each waits for previous)

✅ Parallel where possible:
Step 1 → Step 2A (parallel) ↘
      ↘ Step 2B (parallel) → Step 3
```

**4. The Infinite Loop**
```markdown
❌ Unbounded iteration:
"Keep trying until it works"
"Loop forever"

✅ Bounded iteration:
"Try up to 3 times"
"Max 5 iterations"
"Timeout after 30 seconds"
```

### Communication Anti-Patterns

**1. The Cryptic Messenger**
```markdown
❌ Vague messages:
"There's an issue"
"Something went wrong"
"Check the code"

✅ Specific messages:
"Line 78 in user_auth.rs: missing Ok() wrapper"
"Test `test_login_invalid_password` failed: expected Err, got Ok"
"Compilation error in routes.rs:34: type mismatch"
```

**2. The Ghost**
```markdown
❌ No status updates:
(Agent works for 10 minutes silently)
(Suddenly returns result)

✅ Progress updates:
"Analyzing requirements... (15%)"
"Generating code... (60%)"
"Running tests... (90%)"
```

**3. The Blamer**
```markdown
❌ Accusatory tone:
"You provided incorrect input"
"Your requirements are wrong"
"The architect made a mistake"

✅ Constructive tone:
"Input needs adjustment: [specific issue]"
"Requirements need clarification: [what's unclear]"
"Architecture has issue: [specific problem + suggested fix]"
```

### Output Anti-Patterns

**1. The Placeholder**
```markdown
❌ Incomplete output:
"// TODO: Implement this function"
"[Add description here]"
"TBD"

✅ Complete output:
(All functions implemented)
(All sections filled)
(No placeholders)
```

**2. The Wall of Text**
```markdown
❌ Unformatted dump:
(50 lines of unformatted error messages)
(No structure or highlighting)

✅ Formatted report:
## Errors (3)
**Error 1:** [description]
- File: [path]
- Fix: [solution]
```

**3. The Magician**
```markdown
❌ Output without explanation:
(Creates files)
(No report of what was done)

✅ Output with summary:
Created:
- src/main.rs (implementation)
- tests/main_test.rs (tests)
Summary: [brief description]
```

---

## Testing Agents

### Manual Testing

**1. Smoke Test**
```bash
# Create test project
mkdir test-project
cd test-project

# Create minimal input
echo "Test requirements" > requirements.md

# Run agent
claude-code --agent your-agent "Process requirements.md"

# Verify:
- Agent runs without errors
- Produces expected output
- Output format correct
```

**2. Happy Path Test**
```
Input: Valid, complete requirements
Expected: Success, correct output
Verify: Output matches specification
```

**3. Error Path Tests**
```
Test 1: Missing input file
- Input: (no file)
- Expected: Clear error message
- Verify: Asks for file, doesn't crash

Test 2: Malformed input
- Input: Corrupted/invalid format
- Expected: Validation error
- Verify: Identifies specific issue

Test 3: Incomplete input
- Input: Missing required sections
- Expected: Asks for missing info
- Verify: Lists what's needed
```

### Validation Checklist

**Before deployment:**
```markdown
## Agent Validation

### Structure
- [ ] YAML frontmatter complete
- [ ] Mission section clear
- [ ] Process defined step-by-step
- [ ] Output format specified
- [ ] Context budgets included

### Size
- [ ] 5KB minimum
- [ ] 15KB maximum (20KB absolute max)
- [ ] Under 12KB (ideal)

### Quality
- [ ] No grammatical errors
- [ ] Consistent terminology
- [ ] Examples (max 1) are clear
- [ ] No redundant sections

### Functionality
- [ ] Tools match actual usage
- [ ] Process steps executable
- [ ] Decision logic clear
- [ ] Error handling defined

### Testing
- [ ] Smoke test passed
- [ ] Happy path works
- [ ] Error paths handled
- [ ] Output format correct
```

---

## Example Agents Breakdown

### Example 1: Minimal Agent (docs-builder)

**What it does:** Creates documentation from features

**Size:** ~11KB

**Key sections:**
1. Mission (clear: build LLM-optimized docs)
2. Process (6 phases, step-by-step)
3. Documentation Rules (structure patterns)
4. Quality Checklist (before/during/after)
5. Anti-Patterns (clear don'ts)

**Why it works:**
- Single responsibility (just docs)
- Clear input/output contracts
- Specific format examples
- Integrated with other agents (solution-architect, swe-agent)

**Key pattern:**
```markdown
## Process

### Phase 1: Receive Task (10%)
Get task from other agent.
If vague → ask for specifics.

### Phase 2: Gather Info (15%)
Find relevant files using glob/grep.

### Phase 3: Write Documentation (40%)
Create self-contained, focused docs.

### Phase 4: Update INDEX.md (15%)
Add navigation links.

### Phase 5: Generate llms.txt (10%)
Auto-create LLM-friendly index.

### Phase 6: Report (10%)
Tell what was created.
```

### Example 2: Complex Agent (solution-architect)

**What it does:** Transforms plan → detailed architecture

**Size:** ~22KB (large, but justified)

**Key sections:**
1. Mission (with accountability warning)
2. Core Principles (SOLID, KISS, defensive programming)
3. Technology Selection Guidelines (when to use what)
4. Process (5 phases with detailed substeps)
5. Language-Specific Guidelines (Python, Rust, Shell)
6. Implementation Guide for swe-agent (complete blueprint)

**Why it's larger:**
- Critical role (bad architecture = expensive)
- Multiple languages (Python, Rust, Shell)
- Complete examples (architecture.md templates)
- Comprehensive decision logic

**Key pattern:**
```markdown
## Process

### Phase 1: Understand (15%)
Read plan.md, architecture requirements.
If unclear → ASK immediately.

### Phase 2: Design (40%)
Create architecture.md with:
- System overview (diagram)
- Component breakdown (single responsibility)
- Data models (with justification)
- API endpoints (complete spec)
- Error handling strategy
- Testing strategy
- Deployment architecture

### Phase 3: Implementation Guide (25%)
Create step-by-step guide for swe-agent:
- Exact project structure
- Step 1: Setup (with commands)
- Step 2: Models (with complete code)
- Step 3: Services (with error handling)
- Step 4: API (with validation)
- Step 5: Tests (with examples)

### Phase 4: Document Decisions (10%)
Create ADRs (Architecture Decision Records).

### Phase 5: Review & Finalize (10%)
Self-review before handing to swe-agent.
```

### Example 3: Fast Agent (code-tester)

**What it does:** Quick smoke tests on swe-agent output

**Size:** ~16KB

**Key sections:**
1. Mission (fast sanity checks only)
2. Process (language detection → tests → report)
3. Language-Specific Checks (Rust, Python, Shell)
4. Error Parsing (extract actionable info)
5. Report Format (pass/fail with specifics)

**Why it works:**
- Clear separation from code-reviewer (fast vs deep)
- Immediate feedback loop
- Specific, actionable error messages
- Conversational with swe-agent

**Key pattern:**
```markdown
## Process

### Step 1: Detect Language (5%)
Check for Cargo.toml, requirements.txt, *.sh

### Step 2: Run Tests (60%)

For Rust:
1. cargo fmt --check
2. cargo build
3. cargo clippy -- -D warnings
4. cargo test

For Python:
1. python -m py_compile
2. mypy src/
3. pylint src/
4. pytest tests/

### Step 3: Parse Errors (25%)
Extract file, line, error type, fix suggestion.

### Step 4: Report (10%)

If FAIL:
"Hey swe-agent, line 78 needs Ok(). Here's the fix: [code]"

If PASS:
"Tests passed! ✅ Ready for code-reviewer."
```

---

## Advanced Patterns

### Multi-Agent Pipelines

**Pattern:**
```
Agent A (Generator)
    ↓ creates artifact
Agent B (Validator)
    ↓ validates, gives feedback
    ├─→ [FAIL] → back to Agent A (with fixes)
    └─→ [PASS] → forward to Agent C
Agent C (Transformer)
    ↓ transforms artifact
Agent D (Deployer)
```

**Example:**
```
project-manager (creates plan.md)
    ↓
solution-architect (creates architecture.md)
    ↓
swe-agent (writes code)
    ↓
code-tester (smoke tests)
    ├─→ [FAIL] → back to swe-agent
    └─→ [PASS] → forward to code-reviewer
code-reviewer (deep review)
    ├─→ [REJECT] → back to swe-agent
    └─→ [APPROVE] → project-manager (done)
```

**Implementing in agents:**

Agent A (produces for Agent B):
```markdown
## Output for Agent B

**File:** artifact.md
**Format:** [specification]
**Next:** Pass to Agent B for validation
```

Agent B (validates from Agent A):
```markdown
## Input from Agent A

**Expected file:** artifact.md
**Expected format:** [specification]
**If valid:** Pass to Agent C
**If invalid:** Return to Agent A with fixes
```

### Conditional Routing

**Pattern:**
```markdown
## Routing Logic

**Evaluate state:**
```bash
check_state() {
    if [ condition1 ]; then
        echo "route-to-agent-a"
    elif [ condition2 ]; then
        echo "route-to-agent-b"
    else
        echo "route-to-agent-c"
    fi
}
```

**Route accordingly:**
- agent-a: [reason]
- agent-b: [reason]
- agent-c: [reason]
```

**Example:**
```markdown
## Routing Decision

**Check project state:**
```bash
if [ ! -f "plan.md" ]; then
    echo "No plan → use project-manager"
elif [ ! -f "architecture.md" ]; then
    echo "No architecture → use solution-architect"
elif [ ! -d "src/" ]; then
    echo "No implementation → use swe-agent"
else
    echo "All done → use code-reviewer"
fi
```

**Route to:**
- project-manager: Create plan.md
- solution-architect: Create architecture.md
- swe-agent: Implement code
- code-reviewer: Review quality
```

### State Machines

**Pattern:**
```markdown
## States

1. **INIT** - Starting state
2. **READY** - Prerequisites met
3. **WORKING** - Processing
4. **REVIEW** - Awaiting validation
5. **COMPLETE** - Success
6. **FAILED** - Error state

## Transitions

INIT → READY: When input valid
READY → WORKING: When starting process
WORKING → REVIEW: When work complete
REVIEW → COMPLETE: When approved
REVIEW → WORKING: When changes requested
ANY → FAILED: On unrecoverable error

## Current State Detection

```bash
detect_state() {
    if [ ! -f "input.md" ]; then
        echo "INIT"
    elif [ -f "input.md" ] && [ ! -f "output.md" ]; then
        echo "READY"
    elif [ -f "output.md.tmp" ]; then
        echo "WORKING"
    elif [ -f "output.md" ] && [ ! -f "approved.txt" ]; then
        echo "REVIEW"
    elif [ -f "approved.txt" ]; then
        echo "COMPLETE"
    else
        echo "FAILED"
    fi
}
```
```

### Retry Logic with Backoff

**Pattern:**
```markdown
## Retry Pattern

**Max attempts:** 3
**Backoff:** Exponential (1s, 2s, 4s)

```bash
retry_with_backoff() {
    local max_attempts=3
    local attempt=1
    local delay=1
    
    while [ $attempt -le $max_attempts ]; do
        echo "Attempt $attempt of $max_attempts"
        
        if command_to_retry; then
            echo "Success!"
            return 0
        fi
        
        if [ $attempt -lt $max_attempts ]; then
            echo "Failed, retrying in ${delay}s"
            sleep $delay
            delay=$((delay * 2))
        fi
        
        attempt=$((attempt + 1))
    done
    
    echo "All attempts failed"
    return 1
}
```

**Use for:**
- Network operations
- External API calls
- Database connections
- File operations (busy/locked)
```

### Parallel Execution

**Pattern:**
```markdown
## Parallel Tasks

**Run simultaneously:**
1. Task A (independent)
2. Task B (independent)
3. Task C (independent)

**Then synchronize:**
- Wait for all to complete
- Check all succeeded
- Proceed if all OK

```bash
# Start background tasks
task_a &
PID_A=$!

task_b &
PID_B=$!

task_c &
PID_C=$!

# Wait for all
wait $PID_A $PID_B $PID_C

# Check results
if [ $? -eq 0 ]; then
    echo "All tasks succeeded"
else
    echo "At least one task failed"
fi
```
```

---

## Troubleshooting

### Common Issues

**1. Agent doesn't start**

**Symptoms:**
- Error loading agent
- "Agent not found"

**Check:**
- File location: `~/.claude/agents/agent-name.md`
- YAML frontmatter syntax
- Required fields present (name, description, tools, model)

**Fix:**
```bash
# Validate YAML
head -n 10 ~/.claude/agents/agent-name.md

# Should see:
# ---
# name: agent-name
# description: ...
# tools: [...]
# model: sonnet
# ---
```

**2. Agent exceeds context**

**Symptoms:**
- "Context limit exceeded"
- Slow responses
- High costs

**Check:**
- Agent size (should be <15KB)
- Process includes context budgets
- Not loading unnecessary files

**Fix:**
```markdown
# Add explicit budgets
## Context Budgets
- Keep <20% context (phase 1)
- Keep <40% context (phase 2)
- Keep <20% context (phase 3)

# Reduce agent size
- Remove redundant sections
- Compress examples
- Use bullets over paragraphs
```

**3. Agent produces wrong output**

**Symptoms:**
- Output format incorrect
- Missing required fields
- Doesn't follow specification

**Check:**
- Output Format section clear?
- Examples provided?
- Validation checklist present?

**Fix:**
```markdown
## Output Format

**MUST include:**
- Field 1: [specification]
- Field 2: [specification]

**Template:**
```[exact template]```

## Quality Checklist
- [ ] Output has all required fields
- [ ] Format matches template exactly
```

**4. Agent asks too many questions**

**Symptoms:**
- Requests approval for everything
- Can't make decisions
- Slow progress

**Check:**
- Clear decision logic?
- Autonomy level defined?
- Escalation paths clear?

**Fix:**
```markdown
## Decision Authority

**Decide autonomously:**
- Standard patterns (use best practice)
- Technical details (choose optimal)
- Implementation approach (KISS principle)

**Escalate to user:**
- Architecture changes
- Budget implications
- Security-critical choices
```

**5. Agent ignores instructions**

**Symptoms:**
- Doesn't follow process
- Skips validation
- Wrong approach

**Check:**
- Process section clear?
- Steps actionable?
- Examples provided?

**Fix:**
```markdown
## Process

### Step 1: [Action]
**DO:** [explicit action]
**DON'T:** [explicit anti-pattern]
**Example:** [concrete example]

### Step 2: [Action]
[Same clarity]
```

### Debugging Techniques

**1. Add checkpoints**
```markdown
## Process

### Step 1: Prepare
[actions]
**Checkpoint:** Verify files exist, format valid

### Step 2: Execute
[actions]
**Checkpoint:** Verify output created, no errors

### Step 3: Validate
[actions]
**Checkpoint:** All tests pass, zero warnings
```

**2. Verbose output**
```markdown
## Process

Each step:
1. Log what you're doing
2. Log result
3. Log next action

Example:
"Step 1: Reading plan.md... ✓ Found, 1245 bytes"
"Step 2: Validating format... ✓ All sections present"
"Step 3: Extracting features... ✓ Found 5 MUST, 3 SHOULD"
```

**3. Dry-run mode**
```markdown
## Testing Mode

**When testing:**
- Log actions WITHOUT executing
- Report what WOULD happen
- Show decision logic

**Example:**
"Would create: src/main.rs (implementation)"
"Would run: cargo build"
"Would report: Success with 0 warnings"
```

---

## Production Deployment

### Pre-Deployment Checklist

```markdown
## Production Readiness

### Code Quality
- [ ] No syntax errors in markdown
- [ ] YAML frontmatter valid
- [ ] All sections complete (no TODOs)
- [ ] Examples working (if included)

### Size & Performance
- [ ] Under 15KB (12KB ideal)
- [ ] Context budgets defined
- [ ] No redundant sections

### Testing
- [ ] Smoke test passed
- [ ] Happy path works
- [ ] Error paths handled
- [ ] Output format correct

### Documentation
- [ ] Mission clear
- [ ] Process documented
- [ ] Anti-patterns listed
- [ ] Example usage provided

### Integration
- [ ] Input/output contracts clear
- [ ] Compatible with other agents
- [ ] Communication patterns defined
- [ ] Escalation paths documented
```

### Deployment Process

**1. Create agent file**
```bash
# Create in ~/.claude/agents/
nano ~/.claude/agents/your-agent.md
```

**2. Validate syntax**
```bash
# Check YAML frontmatter
head -n 10 ~/.claude/agents/your-agent.md

# Check size
wc -c ~/.claude/agents/your-agent.md
```

**3. Test agent**
```bash
# Run smoke test
claude-code --agent your-agent "test input"

# Verify output
ls -la output/
cat output/result.md
```

**4. Document usage**
```markdown
# Add to project documentation
## Available Agents

### your-agent
**Purpose:** [what it does]
**When to use:** [trigger conditions]
**Input:** [requirements]
**Output:** [deliverables]
**Example:** `claude-code --agent your-agent "input"`
```

**5. Monitor performance**
```bash
# Track metrics
- Execution time
- Context usage
- Success rate
- Error patterns
```

### Version Control

**Track changes:**
```bash
# Git repo for agents
cd ~/.claude/agents/
git init
git add .
git commit -m "Initial agent deployment"
```

**Semantic versioning in agent:**
```markdown
---
name: your-agent
description: Your agent description
version: 1.0.0
tools: [...]
model: sonnet
---
```

**Changelog:**
```markdown
## Changelog

### v1.1.0 (2025-10-20)
- Added: New validation step
- Fixed: Error handling in Step 3
- Changed: Output format for clarity

### v1.0.0 (2025-10-18)
- Initial release
```

### Maintenance

**Regular reviews:**
- Monthly: Check if still relevant
- Quarterly: Update for new patterns
- Annually: Major refactor if needed

**Signs agent needs update:**
- Frequently hits context limits
- Users often confused by output
- Integration issues with other agents
- New tools/capabilities available

**Update process:**
1. Create new version
2. Test alongside old version
3. Migrate gradually
4. Deprecate old version
5. Archive after 30 days

---

## Conclusion

### Golden Agent Checklist

**Your agent is golden when it:**

**✅ Structure:**
- [ ] Has clear YAML frontmatter
- [ ] Single, focused responsibility
- [ ] Size: 8-12KB (max 15KB)
- [ ] All required sections present

**✅ Clarity:**
- [ ] Mission is crystal clear (2-3 sentences)
- [ ] Process is step-by-step
- [ ] Examples are concrete (max 1)
- [ ] Anti-patterns explicitly listed

**✅ Quality:**
- [ ] Context budgets defined
- [ ] Error handling specified
- [ ] Quality checklists included
- [ ] Output format precise

**✅ Integration:**
- [ ] Input requirements clear
- [ ] Output deliverables defined
- [ ] Communication patterns documented
- [ ] Works in pipeline with others

**✅ Testing:**
- [ ] Smoke test passes
- [ ] Happy path works
- [ ] Error paths handled
- [ ] Output correct

### The Agent Hierarchy

**Level 1: Basic Agent (5-8KB)**
- Single task
- Clear process
- Basic quality checks

**Level 2: Standard Agent (8-12KB)**
- Complex task
- Multi-phase process
- Comprehensive checks
- Error handling

**Level 3: Advanced Agent (12-15KB)**
- Critical role
- Multiple languages/patterns
- Complete examples
- Integration logic

**Level 4: System Agent (15-20KB)**
- Orchestration
- Multi-agent coordination
- Advanced patterns
- Extensive documentation

**Choose the right level for your needs.**

### Final Thoughts

**Remember:**
1. **Minimalism wins** - every word costs tokens
2. **Clarity trumps completeness** - better to be clear than comprehensive
3. **Examples are expensive** - use sparingly (max 1)
4. **Test before deploy** - broken agents are expensive
5. **Iterate based on usage** - perfect is the enemy of good

**The best agent is:**
- Small enough to be fast
- Clear enough to be deterministic
- Complete enough to be autonomous
- Tested enough to be reliable

**Now go build golden agents!** 🚀

---

## Appendix: Quick Reference

### Agent Template (Minimal)

```markdown
---
name: agent-name
description: One sentence. When to use.
tools: [read_file, write_file, bash]
model: sonnet
---

# System Prompt

You are **Agent Name** - [role].

## Mission
[2-3 sentences: what & why]

## Process

### Step 1: [Action] (X% context)
1. [Do this]
2. [Do that]

### Step 2: [Action] (Y% context)
1. [Do this]
2. [Do that]

## Quality Checklist
- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]

## Output Format
[Template or specification]

## Context Budgets
- Keep <X% context (step 1)
- Keep <Y% context (step 2)
```

### Common Tools Reference

```yaml
# Minimal
tools: [read_file]

# Basic writer
tools: [read_file, write_file]

# Code builder
tools: [read_file, write_file, edit_file, glob, grep, bash]

# Orchestrator
tools: [read_file, bash]

# Tester
tools: [bash, read_file, grep]
```

### Context Budget Presets

```markdown
# Generator/Builder
- Understand: 15%
- Plan: 10%
- Build: 50%
- Test: 15%
- Report: 10%

# Reviewer/Tester
- Setup: 10%
- Analyze: 60%
- Report: 20%
- Feedback: 10%

# Router/Orchestrator
- Detect: 30%
- Decide: 20%
- Validate: 25%
- Report: 25%
```

### Size Guidelines

```
Minimum: 5KB
Sweet spot: 8-12KB
Maximum: 15KB
Absolute max: 20KB

Check: wc -c agent.md
Target: 8000-12000 bytes
```

---

**END OF GUIDE**

**Version 1.0 | 2025-10-18**

This guide represents the complete knowledge from our conversation about building production-grade Claude Code agents. Use it as your bible for creating golden agents that are fast, reliable, and maintainable.

**Happy agent building!** 🎉