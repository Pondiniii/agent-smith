# /implement_this

Execute a scheduled job using the orchestrator agent.

## Usage
```
/implement_this <job-slug>
```

## What It Does

1. Validates that `jobs/scheduled/<job-slug>/` exists
2. Spawns the **orchestrator agent** with the job context
3. Orchestrator reads PRD.md and plan.md
4. Executes phases sequentially by delegating to sub-agents
5. Tracks progress in status.md
6. On completion, moves job to `jobs/completed/`

## Prerequisites

- Job must exist in `jobs/scheduled/<job-slug>/`
- Must contain `PRD.md` and `plan.md`
- Use `/plan` to create a job first

## Example

```bash
# After creating a job with /plan
/implement_this user-auth

# Orchestrator will:
# - Read jobs/scheduled/user-auth/PRD.md
# - Read jobs/scheduled/user-auth/plan.md
# - Execute each phase
# - Delegate tasks to coding-agent, validator, etc.
# - Update status.md continuously
# - Move to jobs/completed/user-auth when done
```

## Monitoring Progress

While executing, check:
- `jobs/scheduled/<job-slug>/status.md` - Current status and progress
- `jobs/scheduled/<job-slug>/worklog.md` - Detailed execution log
- Orchestrator will provide concise updates in chat

## Manual Intervention

If orchestrator gets blocked:
- Check status.md for blocker description
- Fix the issue manually if needed
- Re-run `/implement_this <job-slug>` to resume from current phase

## Advanced Options

```
/implement_this <job-slug> --phase <N>      # Start from specific phase
/implement_this <job-slug> --resume         # Resume from last checkpoint
/implement_this <job-slug> --validate-only  # Run validation without execution
```

## Related Commands

- `/plan` - Create new job
- `/status <job-slug>` - Check job status
- `/archive <job-slug>` - Move to completed without executing
- `/cancel <job-slug>` - Cancel and clean up job
