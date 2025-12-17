---
description: Execute a specific implementation plan. Provide a plan file as the argument to this command. It's very important this command runs in a new session.
---

# Implement Plan

You are tasked with implementing an approved technical plan from `thoughts/plans/`. These plans contain phases with specific changes and success criteria.

## Implementation Philosophy

Plans are carefully designed, but reality can be messy. Your job is to:
- Follow the plan's intent while adapting to what you find
- Implement each phase fully before moving to the next
- Verify your work makes sense in the broader codebase context
- Update checkboxes in the plan as you complete sections

When things don't match the plan exactly, think about why and communicate clearly. The plan is your guide, but your judgment matters too.

If you encounter a mismatch:
- STOP and think deeply about why the plan can't be followed
- Present the issue clearly:
  ```
  Issue in Phase [N]:
  Expected: [what the plan says]
  Found: [actual situation]
  Why this matters: [explanation]

  How should I proceed?
  ```
- **Document deviations in the plan**: If proceeding with a change, update the plan file with a clear record of the deviation using the Edit tool. Add or update a section at the end of the plan:

  ```markdown
  ## Deviations from Plan

  ### Phase [N]: [Phase Name]
  - **Original Plan**: [brief summary of what the plan specified]
  - **Actual Implementation**: [what was actually done]
  - **Reason for Deviation**: [why the change was necessary]
  - **Impact Assessment**: [effects on other phases, success criteria, or overall project]
  - **Date/Time**: [when the deviation was made]
  ```

## Verification Approach

After implementing a phase:
- Run the success criteria checks (usually `bun run check` covers everything)
- Fix any issues before proceeding
- Update your progress in both the plan and your todos
- Check off completed items in the plan file itself using Edit

Don't let verification interrupt your flow - batch it at natural stopping points.

## If You Get Stuck

When something isn't working as expected:
- First, make sure you've read and understood all the relevant code
- Consider if the codebase has evolved since the plan was written
- Present the mismatch clearly and ask for guidance

Use sub-tasks sparingly - mainly for targeted debugging or exploring unfamiliar territory.

## Resuming Work

If the plan has existing checkmarks:
- Trust that completed work is done
- Pick up from the first unchecked item
- Verify previous work only if something seems off

Remember: You're implementing a solution, not just checking boxes. Keep the end goal in mind and maintain forward momentum.

## Steps

1. **Read the plan completely** and check for any existing checkmarks (- [x]). Only read the plan file provided as an argument.

2. **Read the original ticket and all files mentioned in the plan**. Read files fully - never use limit/offset parameters, you need complete context. If you have trouble understanding the plan, refer to the research and ticket information.

3. **Consider the steps involved in the plan**. Think deeply about how the pieces fit together and derive a detailed todo list from the plan's phases and requirements.

4. **Implement each phase sequentially**, adapting to what you find while following the plan's intent.

5. **Verify each phase** using the success criteria checks (usually `bun run check` covers everything). Fix any issues before proceeding.

6. **Update the plan file** with checkmarks for completed items using the Edit tool.

7. **Handle any mismatches or issues** by presenting them clearly and asking for guidance if needed.

8. **Update ticket status** to 'implemented' by editing the ticket file's frontmatter.

9. **Create implementation log** create a log file in thoughts/logs with a name that matches the ticket prefixed with the date and time in the format `YYYY-MM-DD` with a summary of the changes made including files changed, unexpected issues encountered if any, and resolutions to said issues if any.

For the log file use this template for the frontmatter:

Use this template structure for the log file:

```markdown
---
type: log
# Ticket this log belongs to (file path or ID)
ticket: thoughts/tickets/[type_subject].md
# Related implementation plan (if any)
plan: thoughts/plans/[descriptive_name].md
# When this implementation run happened
executed_at: [ISO date-time e.g. 2025-01-15T10:30:00Z]
# success | partial | failed
status: success
# Optional: tech, area, command names, etc.
tags: [agents, docs, implement-plan]
# Optional: short, searchable keywords
keywords: [implement-plan, AGENTS.md, flags]
---

# LOG-[ticket-subject]: [Short Summary of Changes]

## Overview

[2–4 sentences summarizing what was implemented in this run.  
Focus on the “what changed” rather than the “why”, since the ticket/plan
already holds the why.]

Example:
- Implemented `update-docs` command to sync `agents.md` from logs.
- Added `--skip-logs` flag to `implement-plan` to optionally skip log creation.

---

## Related Work

- **Ticket**: `[type_subject]` – [short ticket title or description]
- **Plan**: `[descriptive_name]` – [short plan summary]
- **Previous Logs (if any)**:
  - [YYYY-MM-DD_ticket-subject.md] – [very short note]
  - [...]

[Use this section to link this log to its ticket/plan and any earlier runs.]

---

## Changes Overview

[High-level bullet list of what changed in this run.]

- Added/updated commands:
  - `[command-name]` – [very short description]
- Added/changed flags:
  - `[command-name --flag-name]` – [new/changed/removed; behavior summary]
- Behavior changes:
  - [Existing behavior X now does Y instead of Z]
- Structural/code changes:
  - [Refactored agents pipeline; split file X into Y/Z]

---

### Inconsistencies with Current Docs (If Known)

[Optional but very helpful: note any place where you noticed
`AGENTS.md` is now wrong or incomplete.]

- [agents.md – section “Implement Plan” still says logs are optional, but
  they are now always created unless `--skip-logs` is used.]

---

## Documentation Impact (For agents.md and related docs)

[This section is specifically designed to help future tooling/agents
update `agents.md` with minimal but accurate changes.]

---

## Issues, Edge Cases & Resolutions

[Capture anything unexpected that occured during the execution]

- **Issue**: [short title]
  - Description: [what happened]
  - Impact: [how serious; where it shows up]
  - Resolution/Workaround: [what was done]

- **Known Limitations / Edge Cases**
  - [e.g. “`update-docs` currently only looks at the most recent log file.”]

# [TYPE-XXX]: [Descriptive Title]
---
```
```


Use the todowrite tool to create a structured task list for the 8 steps above, marking each as pending initially. Note that Step 3 may expand into multiple implementation subtasks derived from the plan.

**plan**

$ARGUMENTS
