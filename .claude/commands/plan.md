# /plan

Unified command for planning new implementation project. Creates PRD + plan through interactive session.

## Goal
Single entry point that interviews the human, creates PRD.md and task plan, saves to `jobs/scheduled/`, ready for execution.

## Flow

### Phase 1: Discovery Interview
1. Ask for project/task name and slug (e.g., "user-auth" from "User Authentication")
2. What's the main goal? What problem are we solving?
3. What does success look like? (measurable outcomes)
4. What's in scope vs out of scope?
5. Any constraints, dependencies, or risks?
6. Expected timeline/priority?

### Phase 2: Generate Artifacts
7. Create PRD structure:
   ```markdown
   # PRD — {{ project_name }}

   ## Cel & kontekst
   {{ goal_description }}

   ## Success criteria
   - [ ] {{ criterion_1 }}
   - [ ] {{ criterion_2 }}

   ## Zakres
   **W zakresie:**
   - {{ in_scope_items }}

   **Poza zakresem:**
   - {{ out_of_scope_items }}

   ## Constraints & Dependencies
   - {{ constraints }}

   ## Risks & Mitigations
   - {{ risks_with_mitigations }}
   ```

8. Break into phases and tasks:
   ```markdown
   # Plan — {{ project_name }}

   **Status:** scheduled
   **Created:** {{ timestamp }}
   **Priority:** {{ priority }}

   ## Phases

   ### Phase 1: {{ phase_name }}
   - [ ] {{ task_1 }} (agent: {{ agent_name }})
   - [ ] {{ task_2 }} (agent: {{ agent_name }})
   - [ ] Validate phase 1

   ### Phase 2: {{ phase_name }}
   ...

   ## Validation Checkpoints
   - [ ] Unit tests pass
   - [ ] Integration works
   - [ ] Documentation complete
   ```

### Phase 3: Review & Confirm
9. Show PRD and plan to human
10. Ask: "Czy mogę utworzyć pliki w `jobs/scheduled/{{ slug }}/`?"
11. If human says changes needed:
    - Iterate on PRD/plan
    - Go back to step 9
12. If human confirms:
    - Create `jobs/scheduled/{{ slug }}/`
    - Save `PRD.md`
    - Save `plan.md`
    - Save `status.md` with metadata
    - Confirm to human: "Utworzono w jobs/scheduled/{{ slug }}. Gotowe do /implement_this"

## Directory Structure Created
```
jobs/scheduled/{{ slug }}/
├── PRD.md          # Product requirements
├── plan.md         # Phased task breakdown
├── status.md       # Current status, metadata
└── README.md       # Quick overview
```

## Rules
- Keep interview conversational but focused (max 5-7 questions)
- Don't create files until human confirms
- Use slug format: lowercase-with-hyphens
- Always create status.md with: created timestamp, priority, current phase
- Reference which agents will be used for each task type

## Next Steps
After `/plan` completes, human can:
- `/implement_this {{ slug }}` - run the orchestrator
- `/edit {{ slug }}` - modify PRD/plan before execution
- `/archive {{ slug }}` - move to jobs/completed

## Example Usage
```
Human: /plan
Agent: Co chcesz zaimplementować? (nazwa projektu)
Human: System logowania użytkowników
Agent: Jaki jest główny cel tego systemu?
Human: Bezpieczne uwierzytelnianie z JWT tokens
...
Agent: [Shows PRD and plan]
Agent: Czy mogę utworzyć pliki w jobs/scheduled/user-login/?
Human: tak
Agent: ✓ Utworzono jobs/scheduled/user-login/
       - PRD.md
       - plan.md
       - status.md
       Gotowe do /implement_this user-login
```

## Integration Points
- Uses templates from `.claude/agents/templates/`
- Can delegate to sub-agents during execution phase
- Integrates with `/implement_this` execution workflow
- CODEX validation can be added to plan phases
