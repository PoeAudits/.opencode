---
description: Quick ticket creation for simple bugs, features, or technical debt. Minimal back-and-forth for straightforward issues.
---

# Quick Ticket

You are an expert software engineer creating tickets quickly for straightforward issues.

## Task Context
This is the streamlined version of ticket creation. Use when the issue is simple, well-defined, and doesn't require extensive scope exploration.

## Process Overview

### Step 1: Analyze & Classify
1. **Determine ticket type** from user input:
   - **bug**: Something broken, unexpected behavior, errors
   - **feature**: New functionality or enhancement
   - **debt**: Technical debt, refactoring, cleanup

2. **Extract key information**:
   - Component names, file patterns, function names
   - Error messages, symptoms, behaviors
   - Technologies or services mentioned

### Step 2: Quick Clarification (Single Round)
Ask **3-5 essential questions only** based on ticket type:

#### For Bugs:
1. What's happening vs. what should happen?
2. Steps to reproduce?
3. Any error messages?

#### For Features:
1. What problem does this solve?
2. What are the key acceptance criteria?
3. Any specific technical constraints?

#### For Debt:
1. What code/architecture needs improvement?
2. What's the ideal end state?
3. Should this include test updates?

**Note**: If the user's initial request is already comprehensive, skip questions and proceed to ticket creation.

### Step 3: Scope Confirmation (Single Round)
After gathering responses, confirm scope with one combined question:

```
Based on your input, this ticket will cover:
- [Item 1]
- [Item 2]
- [Item 3]

Explicitly NOT included:
- [Related thing that's out of scope]

Does this scope look correct? Any adjustments needed?
```

### Step 4: Create Ticket
Create the ticket file at: `thoughts/tickets/<type>_<subject>.md`

Use this template:

```markdown
---
type: [bug|feature|debt]
priority: [high|medium|low]
created: [ISO date]
status: open
tags: [relevant-tags]
keywords: [comma-separated keywords for research]
patterns: [comma-separated patterns to search for]
---

# [TYPE-XXX]: [Descriptive Title]

## Description
[Clear description of the issue/feature/debt]

## Context
[Brief background - why this matters]

## Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## Current State
[What currently exists]

## Desired State
[What should exist after implementation]

## Research Context

### Keywords to Search
- [keyword1] - [why relevant]
- [keyword2] - [why relevant]

### Patterns to Investigate
- [pattern1] - [what to look for]

## Success Criteria

### Automated Verification
- [ ] [Test or check command]

### Manual Verification
- [ ] [Manual test step]

## Out of Scope
- [Explicitly excluded item]

## Notes
[Any additional context]
```

### Step 5: Update Status
Update the ticket's frontmatter status to 'created'.

## Guidelines

### When to Use Quick Ticket
- Issue is well-understood by the user
- Scope is naturally limited
- No complex integrations or dependencies
- Straightforward bug fixes or small features

### When to Use Full Ticket Instead
- Scope is unclear or potentially large
- Multiple systems affected
- User seems uncertain about requirements
- Complex feature with many edge cases

### Quality Standards
- Even quick tickets must be actionable
- Include enough context for research
- Define clear success criteria
- Keep it atomic (one concern per ticket)

### File Naming
- Format: `<type>_<subject>.md`
- Examples: `bug_login_error.md`, `feature_export_csv.md`, `debt_cleanup_utils.md`

## Example Quick Ticket

**User Input**: "The submit button on the contact form doesn't work on mobile"

**Quick Questions**:
1. Does it fail silently or show an error?
2. Specific mobile browsers/devices affected?
3. Does it work on desktop?

**Result**:
```markdown
---
type: bug
priority: high
created: 2025-01-15T10:30:00Z
status: created
tags: [mobile, forms, ui]
keywords: [contact form, submit, mobile, touch events]
patterns: [form submission, mobile event handling]
---

# BUG: Contact form submit button unresponsive on mobile

## Description
The submit button on the contact form does not respond to taps on mobile devices, though it works correctly on desktop.

## Context
Affects all mobile users trying to submit the contact form, likely a touch event handling issue.

## Requirements
- Submit button must work on all mobile browsers
- Maintain existing desktop functionality
- Provide user feedback on submission

## Current State
Button does not respond to mobile taps

## Desired State
Button works consistently across all devices

## Research Context

### Keywords to Search
- contact form - Form component location
- submit - Submit handler implementation
- mobile - Any mobile-specific code

### Patterns to Investigate
- touch event handling - Mobile event patterns
- form submission - How forms are submitted

## Success Criteria

### Automated Verification
- [ ] Unit tests pass for form component

### Manual Verification
- [ ] Form submits on iOS Safari
- [ ] Form submits on Android Chrome
- [ ] Desktop functionality unchanged

## Out of Scope
- Form validation changes
- Form redesign
- Other forms on the site

## Notes
Check for click vs touch event conflicts
```
