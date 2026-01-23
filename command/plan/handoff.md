---
name: handoff
description: Interrupts orchestration and creates a handoff report for continuation by another agent. Updates the plan with current status and saves a comprehensive handoff file.
---

# Orchestration Handoff

This command is used to **interrupt orchestration** and prepare for handoff to another agent session. When invoked, you must:

1. **Update the plan** with current execution status
2. **Create a handoff report** in `thoughts/handoffs/`
3. **Summarize the state** so continuation is seamless

---

## Step 1: Update the Plan

Add or update a **Status Section** at the bottom of the current plan file:

```markdown
---

## Execution Status

**Last Updated:** [timestamp]
**Handoff ID:** [generated-id]

### Phase Status

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 1: [Name] | ✅ Complete | [any notes] |
| Phase 2: [Name] | 🔄 In Progress | Currently on Task 2.3 |
| Phase 3: [Name] | ⏳ Pending | |

### Current Position

**Active Phase:** Phase 2: [Name]
**Active Task:** Task 2.3: [Task Name]
**Task Status:** [In Progress / Blocked / Awaiting Review]

### Completed Tasks This Session

- [x] Task 1.1: [Name] - [brief outcome]
- [x] Task 1.2: [Name] - [brief outcome]
- [x] Task 2.1: [Name] - [brief outcome]
- [x] Task 2.2: [Name] - [brief outcome]
- [ ] Task 2.3: [Name] - **IN PROGRESS**

### Next Actions

1. [What should happen next]
2. [Following action]
```

### Status Markers

Use these markers consistently:

| Marker | Meaning |
|--------|---------|
| `✅` | Complete |
| `🔄` | In Progress |
| `⏳` | Pending (not started) |
| `⚠️` | Blocked |
| `❌` | Failed (needs attention) |
| `📝` | Needs Review |
| `📄` | Needs Documentation |

---

## Step 2: Create Handoff Report

Create a file in `thoughts/handoffs/` with this structure:

**Filename:** `handoff-[YYYY-MM-DD]-[short-description].md`

```markdown
# Orchestration Handoff Report

**Created:** [timestamp]
**Handoff ID:** [same as in plan]
**Plan File:** [path to plan file]

---

## Context

### Original Objective
[What the orchestration was trying to accomplish]

### Plan Overview
[Brief summary of the plan structure - phases and key tasks]

---

## Current State

### Progress Summary
- **Phases Complete:** [N] of [Total]
- **Tasks Complete:** [N] of [Total]
- **Current Phase:** [Phase name]
- **Current Task:** [Task name and status]

### Active Work
[What was being worked on when handoff was initiated]

**Last Subagent Dispatched:** [seeker/worker/executor/reviewer/documenter]
**Subagent Task:** [What they were doing]
**Subagent Status:** [Completed / In Progress / Not Yet Returned]

---

## Completed Work

### Phase 1: [Name] ✅
[Summary of what was accomplished]

**Tasks:**
- Task 1.1: [outcome]
- Task 1.2: [outcome]

**Files Changed:**
- Created: [files]
- Modified: [files]

### Phase 2: [Name] 🔄
[Summary of progress so far]

**Completed Tasks:**
- Task 2.1: [outcome]
- Task 2.2: [outcome]

**In Progress:**
- Task 2.3: [current state]

---

## Divergences from Plan

[Document any deviations from the original plan]

### Intentional Changes
| Original Plan | Actual Implementation | Reason |
|---------------|----------------------|--------|
| [planned approach] | [what was done instead] | [why] |

### Discovered Issues
- [Issue encountered and how it was handled]

### Scope Adjustments
- [Any tasks added, removed, or modified]

---

## Blockers & Open Issues

### Current Blockers
[If the handoff is due to a blocker]
- **Blocker:** [description]
- **Impact:** [what's blocked]
- **Attempted:** [what was tried]
- **Needed:** [what would unblock]

### Known Issues
[Issues that were deferred or noted for later]
- [Issue 1]
- [Issue 2]

---

## Continuation Instructions

### Immediate Next Steps
1. [First thing the pickup agent should do]
2. [Second step]
3. [Third step]

### Context to Gather
[Any information the next agent should seek before continuing]
- [Context item 1]
- [Context item 2]

### Files to Review
[Key files the next agent should read]
- `path/to/file1` - [why]
- `path/to/file2` - [why]

### Subagent Recommendations
[Suggestions for the next agent]
- For Task 2.3: Use [worker/executor] because [reason]
- Consider dispatching seeker first to [gather what context]

---

## Session Summary

### Subagents Dispatched
| Subagent | Task | Outcome |
|----------|------|---------|
| seeker | [task] | [outcome] |
| worker | [task] | [outcome] |
| reviewer | [task] | [outcome] |

### Key Decisions Made
[Decisions that affect future work]
- [Decision 1]: [what was decided and why]
- [Decision 2]: [what was decided and why]

### Lessons Learned
[Useful context for continuation]
- [Observation 1]
- [Observation 2]

---

## Pickup Command

To continue this orchestration:

\`\`\`
/pickup @thoughts/handoffs/[this-filename].md
\`\`\`
```

---

## Step 3: Confirm Handoff

After creating both updates, confirm to the user:

```markdown
## Handoff Complete

**Plan Updated:** [path to plan]
**Handoff Report:** `thoughts/handoffs/[filename].md`

### Current State
- Phase [N] of [Total]: [status]
- Task [N.M]: [status]

### To Continue
Fork the thread after initial context loading and run:
\`\`\`
/pickup @thoughts/handoffs/[filename].md
\`\`\`

### Immediate Next Steps for Pickup Agent
1. [step 1]
2. [step 2]
```

---

## When to Use Handoff

Use `/handoff` when:
- You need to stop orchestration mid-execution
- Context window is getting full
- A long-running task needs to continue in a new session
- You want to checkpoint progress before a risky operation
- The user requests interruption

---

## Important Notes

1. **Don't lose work** - Ensure all completed work is documented
2. **Be specific** - The pickup agent has no memory; be explicit
3. **Note divergences** - Any deviation from plan must be documented
4. **Include file paths** - The pickup agent needs to know what to read
5. **Recommend next actions** - Guide the pickup agent's first steps
