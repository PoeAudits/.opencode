# Task: {{TASK_NAME}}

## Branch
`{{BRANCH_NAME}}`

## Assigned Approach
{{APPROACH_DESCRIPTION}}

## Goal
{{GOAL_DESCRIPTION}}

## Success Criteria
{{SUCCESS_CRITERIA}}

---

## Codebase Context

{{CODEBASE_CONTEXT}}

---

## Known Issues from Previous Attempts

{{KNOWN_ISSUES}}

---

## Constraints

{{CONSTRAINTS}}

---

## Log File Formats

You MUST create and maintain these files in this worktree:

### WORKLOG.md

```markdown
# Worklog: {{BRANCH_NAME}}

Started: <timestamp>
Task: {{TASK_NAME}}
Approach: {{APPROACH_NAME}}

---

## Entry N: <timestamp>
### Plan
<What you're about to do>

### Action  
<What you did>

### Result
- Status: SUCCESS | FAILURE | PARTIAL
- Output: <relevant output>
- Notes: <observations>

---
```

### REFLECTION.md

```markdown
# Reflection: {{BRANCH_NAME}}

## Outcome
- **Status**: SUCCESS | PARTIAL | FAILED
- **Completion**: <what was achieved>

## Approach Taken
<summary>

## What Worked
- <item>

## What Failed
- **<problem>**: <description>
  - Attempted: <what you tried>
  - Suggestion: <for future attempts>

## Errors Encountered

### Error 1: <name>
- **Message**: `<message>`
- **Cause**: <why>
- **Solution**: <how fixed or UNRESOLVED>
- **Prevention**: <how to avoid>

## Files Modified
| File | Change | Description |
|------|--------|-------------|
| | | |

## Recommendations for Next Attempt
1. <suggestion>
```

---

## Begin

1. Initialize WORKLOG.md with Entry 1 documenting your start
2. Proceed with your assigned approach
3. Log every significant action
4. Write REFLECTION.md when complete
