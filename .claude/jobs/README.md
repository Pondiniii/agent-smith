# Jobs Workflow

Job lifecycle in agent-smith system.

---

## Folder Structure

```
jobs/
├── scheduled/   ← Jobs awaiting implementation
├── running/     ← Jobs currently being worked on
└── completed/   ← Jobs finished (ready for final audit)
```

---

## Job Lifecycle

### 1. **SCHEDULED** → Planning Phase
```
jobs/scheduled/[job_slug]/
├── PRD.md              ← Requirements
├── PLAN.md             ← Implementation plan (phases + tasks)
└── STATUS.md           ← Initial state
```

**State:** Job queued, waiting for main agent to pick up

**Main agent:**
- Reads PRD.md and PLAN.md
- Spawns sub-agents (coding-agent, docs-agent, etc)
- Executes phases sequentially

---

### 2. **RUNNING** → Active Implementation
```
jobs/running/[job_slug]/
├── PRD.md              ← Requirements (unchanged)
├── PLAN.md             ← Updated with progress (✓ marks, notes)
├── STATUS.md           ← Live status updates
└── worklog.md          ← Detailed work log
```

**State:** Job actively being worked on by agents

**Updates during work:**
- STATUS.md: current phase, task, blockers
- PLAN.md: checkmarks as tasks complete
- worklog.md: detailed activity log

**When moved here:**
- Main agent starts implementation
- Moves entire folder from `scheduled/` to `running/`

```bash
# When starting job
mv .claude/jobs/scheduled/[slug]/ .claude/jobs/running/[slug]/
```

---

### 3. **COMPLETED** → Ready for Audit
```
jobs/completed/[job_slug]/
├── PRD.md              ← Requirements
├── PLAN.md             ← Final (all ✓)
├── STATUS.md           ← Final status (completion summary)
├── worklog.md          ← Full work history
└── [other artifacts]   ← Generated files, reports
```

**State:** Job finished, ready for project-auditor verification + CODEX final audit

**When moved here:**
- All PLAN.md tasks marked ✓
- STATUS.md shows "completed"
- No active blockers
- Main agent marks job done

```bash
# When job complete
mv .claude/jobs/running/[slug]/ .claude/jobs/completed/[slug]/
```

---

## Key Files in Each Job

### PRD.md (Project Requirements Document)
- **Never changes** during implementation
- Contains requirements, acceptance criteria, success metrics
- Project-auditor verifies against this

### PLAN.md (Implementation Plan)
- Phases and tasks with checkboxes
- Updated as work progresses (✓ marks)
- Tasks format:
  ```markdown
  ## Phase 1: Setup
  - [ ] Task 1.1: Description
  - [ ] Task 1.2: Description

  ## Phase 2: Implementation
  - [ ] Task 2.1: Description
  ```

### STATUS.md (Live Status Tracker)
- Updated frequently during work
- Format:
  ```markdown
  # Status — [job_name]

  **Current Phase:** 2/3 — Implementation
  **Current Task:** Task 2.1: [name]
  **Status:** in_progress
  **Started:** [timestamp]
  **Last Updated:** [timestamp]

  ## Progress
  - [x] Phase 1: Setup ✓
  - [ ] Phase 2: Implementation (current)
    - [x] Task 2.1 ✓
    - [ ] Task 2.2 ← current
    - [ ] Task 2.3

  ## Blockers
  - [blocker if exists]

  ## Metrics
  - Tasks completed: X
  - Time elapsed: X hours
  ```

### worklog.md (Detailed Activity Log)
- Created during work
- Comprehensive record of all actions
- Helps with debugging, learning, hand-offs

---

## Workflow Timeline

```
1. Job Created
   └─> Placed in jobs/scheduled/[slug]/

2. Main Agent Picks Up
   └─> Moves to jobs/running/[slug]/
   └─> Spawns sub-agents
   └─> Updates STATUS.md + PLAN.md + worklog.md

3. Work In Progress
   └─> Main agent updates files frequently
   └─> Sub-agents report progress
   └─> Blockers tracked in STATUS.md
   └─> Tasks marked ✓ in PLAN.md

4. Job Complete (claimed)
   └─> All PLAN.md tasks marked ✓
   └─> STATUS.md shows "completed"
   └─> Moves to jobs/completed/[slug]/

5. Validation by project-auditor
   └─> Spawned by main agent
   └─> Verifies against PRD.md
   └─> Checks git diff for code changes
   └─> Reports: APPROVED or REJECTED

6. If APPROVED
   └─> Moves to final CODEX audit
   └─> Project is ready for deployment

7. If REJECTED
   └─> Moves back to jobs/running/[slug]/
   └─> Main agent continues work
   └─> Fixes issues
   └─> Re-validates with project-auditor
```

---

## Status Values

| Status | Meaning | Location |
|--------|---------|----------|
| **pending** | Job queued, not started | `scheduled/` |
| **in_progress** | Job actively being worked | `running/` |
| **blocked** | Job has blockers, waiting | `running/` |
| **completed** | Job finished, ready for audit | `completed/` |
| **approved** | project-auditor approved | `completed/` (ready for CODEX) |
| **rejected** | project-auditor found issues | → back to `running/` |

---

## Job Folder Naming

Format: `[project-name]-[feature]-[date]` or just `[project-slug]`

Examples:
- `user-auth`
- `database-migration`
- `api-refactor-v2`
- `bug-fix-memory-leak`

---

## Rules

1. **Never skip phases** - Jobs go: scheduled → running → completed
2. **Update STATUS.md frequently** - Live tracking during work
3. **Keep PLAN.md current** - Mark tasks as you complete them
4. **All artifacts stay in job folder** - Don't scatter output files
5. **Use project-auditor before moving to completed** - Verify work done
6. **Blockers must be tracked** - Document what's blocking progress
7. **worklog.md is mandatory** - Record all significant actions

---

## Quick Commands

```bash
# Start a job (move from scheduled to running)
mv .claude/jobs/scheduled/[slug]/ .claude/jobs/running/[slug]/

# Mark job complete (move from running to completed)
mv .claude/jobs/running/[slug]/ .claude/jobs/completed/[slug]/

# List running jobs
ls -1 .claude/jobs/running/

# List completed jobs
ls -1 .claude/jobs/completed/

# Check job status
cat .claude/jobs/running/[slug]/STATUS.md

# View progress
cat .claude/jobs/running/[slug]/PLAN.md
```
