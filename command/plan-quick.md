---
description: Quick implementation plan for simple tickets. Minimal iteration for straightforward changes. Best for small bugs, simple features, or targeted refactors.
---

# Quick Plan

You are tasked with creating focused implementation plans for straightforward tickets without extensive back-and-forth.

## Process Steps

### Step 1: Gather Context

1. **Read all provided files FULLY**:
   - Ticket file
   - Any research documents mentioned
   - Related code files if specified

2. **Run targeted research** (single round):
   - Use **codebase-locator** to find directly relevant files
   - Use **codebase-analyzer** if implementation patterns are unclear
   - Focus only on the immediate area of change

3. **Summarize understanding** (no questions unless blocking):
   ```
   Based on the ticket and codebase research:
   
   **What needs to change:**
   - [Change 1 with file reference]
   - [Change 2 with file reference]
   
   **Approach:**
   [1-2 sentence strategy]
   
   **Any concerns:** [List or "None - proceeding with plan"]
   ```

   Only ask questions if there's a genuine blocker. For simple tickets, proceed directly to planning.

### Step 2: Write the Plan

Create plan at: `thoughts/plans/{descriptive_name}.md`

**Template for Quick Plans:**

```markdown
# [Task Name] Implementation Plan

## Overview
[2-3 sentences: what we're doing and why]

## Current State
[Brief description of what exists now]
- Key file: `path/to/file.ext` (lines X-Y)

## Changes Required

### 1. [First Change Area]
**File**: `path/to/file.ext`

**What to change:**
[Description of the change]

```[language]
// Code snippet if helpful for clarity
```

**Why:**
[Brief rationale]

### 2. [Second Change Area]
**File**: `path/to/another/file.ext`

**What to change:**
[Description]

---

## Out of Scope
- [Thing we're explicitly not doing]

## Success Criteria

### Automated Verification
- [ ] Tests pass: `[test command]`
- [ ] Type check passes: `[check command]`
- [ ] Lint passes: `[lint command]`

### Manual Verification
- [ ] [Specific manual test]
- [ ] [Another manual check if needed]

## References
- Ticket: `thoughts/tickets/[ticket_file].md`
```

### Step 3: Quick Review
Present the plan location and key points:

```
Created implementation plan: `thoughts/plans/[filename].md`

**Summary:**
- [Number] files to modify
- Main changes: [brief list]
- Estimated complexity: [low/medium]

Let me know if any adjustments are needed, otherwise this is ready for implementation.
```

### Step 4: Update Ticket Status
Update the ticket's frontmatter status to 'planned'.

## Guidelines

### When to Use Quick Plan
- Single file or small number of files affected
- Clear, well-defined ticket
- Follows existing patterns in codebase
- No architectural decisions needed
- Bug fixes with obvious solutions
- Small feature additions

### When to Use Full Plan Instead
- Multiple systems or services affected
- New patterns need to be established
- Database migrations required
- API contract changes
- Significant refactoring
- Unclear implementation path

### Quality Standards (Still Required)
- Specific file paths and line references
- Clear success criteria (automated + manual)
- Explicit out-of-scope items
- Actionable without further clarification

### Plan Sizing
Quick plans should typically have:
- 1-3 change areas
- 1-5 files modified
- Single phase (no phasing needed)
- Can be implemented in one session

## Example Quick Plan

```markdown
# Fix Mobile Contact Form Submit - Implementation Plan

## Overview
The contact form submit button doesn't respond on mobile due to missing touch event handling. We'll add proper touch support while maintaining desktop functionality.

## Current State
Form component at `src/components/ContactForm.tsx` uses only onClick handler (line 45).

## Changes Required

### 1. Add Touch Event Support
**File**: `src/components/ContactForm.tsx`

**What to change:**
Add onTouchEnd handler alongside onClick, with preventDefault to avoid double-firing.

```tsx
<button
  onClick={handleSubmit}
  onTouchEnd={(e) => {
    e.preventDefault();
    handleSubmit();
  }}
  type="submit"
>
```

**Why:**
Mobile Safari requires explicit touch handlers for reliable button interaction.

### 2. Add Mobile Test
**File**: `src/components/__tests__/ContactForm.test.tsx`

**What to change:**
Add test case for touch event submission.

```tsx
it('submits on touch end', () => {
  fireEvent.touchEnd(submitButton);
  expect(mockSubmit).toHaveBeenCalled();
});
```

---

## Out of Scope
- Form validation changes
- Form styling updates
- Other forms in the application

## Success Criteria

### Automated Verification
- [ ] Tests pass: `npm test ContactForm`
- [ ] Type check: `npm run typecheck`

### Manual Verification
- [ ] Form submits on iOS Safari
- [ ] Form submits on Android Chrome
- [ ] Desktop click still works
- [ ] No double submissions occur

## References
- Ticket: `thoughts/tickets/bug_contact_form_mobile.md`
```

## Common Quick Plan Patterns

### Bug Fix Pattern
1. Identify root cause location
2. Describe the fix
3. Add regression test
4. List verification steps

### Small Feature Pattern
1. Where to add the feature
2. Implementation details
3. How it integrates with existing code
4. Test coverage needed

### Targeted Refactor Pattern
1. Current code location
2. What's changing and why
3. Ensure behavior preservation
4. Update related tests



**files**

$ARGUMENTS
