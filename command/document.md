---
description: Updates documentation based on implementation logs in thoughts/logs. Proposes minimal, user-approved edits derived from log summaries.
---

# Update Documentation

You are responsible for keeping the agent documentation (e.g., `AGENTS.md`) in sync with the actual behavior of the system by using implementation logs in `thoughts/logs` as your primary source of truth for recent changes.

## Task Context

The project workflow is:

1. A ticket is created in `thoughts/tickets/`.
2. A plan is created in `thoughts/plans/` for that ticket.
3. The plan is implemented, and an implementation log is written to `thoughts/logs/` summarizing:
   - Files changed
   - New/changed/removed commands, flags, or behaviors
   - Unexpected issues and resolutions

Your job is to:

- Read one or more logs.
- Identify documentation-relevant changes.
- Propose minimal, targeted edits to `AGENTS.md`.
- Ask the user for confirmation before applying any changes.
- Apply only the approved edits using the Edit tool.

## Directory & File Conventions

- Tickets: `thoughts/tickets/*.md`
- Plans: `thoughts/plans/*.md`
- Logs: `thoughts/logs/YYYY-MM-DD_<ticket-id>.md`
- Archive: `thoughts/archive/*`
- Agent documentation: `AGENTS.md` (typically in the repo root, should have already been read)

## Process Steps

### Step 1: Context Gathering

1. Read all log files provided as arguments:
   - Use the Read tool WITHOUT limit/offset to read each log fully.
   - Focus on:
     - High-level summary of changes
     - Sections explicitly mentioning commands, flags, configuration, or agent behavior
2. When helpful, identify the related ticket/plan from the log and briefly skim them for additional context (ticket purpose, scope of changes).

Before proceeding, summarize to the user:

- Which logs you read
- Which high-level changes appear documentation-relevant

### Step 2: Extract Documentation-Relevant Changes

From the logs, extract only information that should be reflected in `AGENTS.md`, for example:

- New commands or agent capabilities
- New flags/options/env vars for existing commands
- Changes to existing flags (renamed, behavior changed, default changed)
- Removed/deprecated commands or flags
- Updated workflows (e.g., new required step, changed file paths)
- Important behavioral constraints or limitations that users must know

Organize these as a structured list, for example:

- [Type: new flag] `command_name --new-flag`
  - Behavior: ...
  - Source: `thoughts/logs/2025-01-20_eng_1234.md`
- [Type: behavior change] `implement-plan` now skips logs when `--skip-logs` is set
  - Source: `thoughts/logs/2025-01-21_eng_5678.md`

If anything is ambiguous or underspecified in the logs, ask the user for clarification before designing documentation changes.

### Step 3: Read Existing Documentation

1. Read `AGENTS.md` fully (no limit/offset) if not already read.
2. The AGENTS.md file may include other locations for documentation which should be read as well.
2. Identify:
   - Sections describing commands, flags, workflows, or behaviors related to the extracted changes
   - Any text that appears outdated or conflicting with the logs
   - Natural insertion points for new information (e.g., existing command subsections or flag tables)

Do not modify anything yet.

### Step 4: Design Minimal Proposed Changes

For each documentation-relevant change:

1. Decide whether it requires:
   - Adding a new bullet/row/paragraph
   - Updating an existing line (e.g., flag name, default value, behavior)
   - Marking a feature as deprecated or removed
   - Removing a now-invalid instruction

2. Keep changes as small and local as possible:
   - Prefer editing a single bullet or sentence over rewriting a whole section.
   - Preserve existing formatting, headings, and style.
   - Avoid duplicating information already clearly documented elsewhere.

3. Draft the exact markdown edits you intend to make, grouped by location, for example:

   - Section: `## Implement Plan Command`
     - Current line: `- Supports the \`--dry-run\` flag to simulate changes.`
     - Proposed replacement: `- Supports the \`--dry-run\` and \`--skip-logs\` flags to simulate changes or skip log creation.`

   - Section: `### Logs Directory`
     - Proposed addition (new bullet): `- Each implementation run writes a summary log to \`thoughts/logs/YYYY-MM-DD_<ticket-id>.md\` describing files changed and notable behavior changes.`

### Step 5: Interactive Review & Approval (CRITICAL)

Before using the Edit tool:

1. Present a clear, grouped proposal to the user, for example:

   ```markdown
   Based on log `thoughts/logs/2025-01-20_eng_1234.md`, I propose:

   1. In "## Create Ticket Command":
      - Add a bullet documenting the new `--priority` flag.

   2. In "## Implement Plan Command":
      - Update the description of `--dry-run` to match the new behavior.
      - Remove the reference to the deprecated `--legacy-mode` flag.
   3. For each proposed change, show:
      - The relevant excerpt from AGENTS.md (before)
      - The exact markdown you propose (after)
   ```

2. Ask the user to:
   - Approve all changes
   - Approve only specific items
   - Request edits to the wording
   - Mark some items as "out of scope" or "do not document"

Do not make any file edits until the user gives explicit approval on what will be added/changed.

If the user indicates that a proposed change is out of scope or too large, either:

- Drop that change, or
- Suggest creating a separate ticket and plan for a broader documentation update.

### Step 6: Apply Approved Changes

For each user-approved change set:

1. Use the Edit tool to update AGENTS.md or other documentation file:
   - Modify only the lines necessary.
   - Preserve surrounding formatting and spacing.
   - Avoid reflowing or reformatting unrelated content.

2. If a requested change would require a large rewrite:
   - Pause and confirm with the user before proceeding.
   - Clearly explain the impact and scope.

After editing, re-read the updated sections to confirm they match both:

- The behavior described in the logs
- The wording agreed upon during review

### Step 7: Summarize Results

Report back to the user:

- Which log(s) were processed
- Exactly which sections of AGENTS.md were updated
- A brief bullet list of the final documentation changes, for example:
  - Documented new --priority flag for Create Ticket command.
  - Updated Implement Plan to describe --skip-logs.
  - Removed obsolete reference to --legacy-mode.

If you discovered additional potential documentation improvements that were not applied (to keep the change minimal), list them as suggestions and recommend creating separate tickets if desired.

### Step 8: Task Tracking

Use the todowrite tool to create a structured todo list for this command, for example:

1. Read provided logs
2. Extract documentation-relevant changes
3. Read AGENTS.md
4. Design minimal proposed edits
5. Present proposals for user review
6. Apply approved edits
7. Summarize final documentation updates

Mark each as pending initially and update as you progress.

## Important Guidelines

1. **Be Minimal:**
   - Favor the smallest possible change that makes the documentation accurate.
   - Do not expand sections with speculative or nice-to-have details.
   - Do not copy large log excerpts into AGENTS.md.

2. **Be Log-Driven:**
   - Only document behavior that is supported by logs, tickets, plans, or clear user confirmation.
   - If the log is unclear or contradicts existing docs, ask the user before changing anything.

3. **Be Consistent:**
   - Match the formatting, tone, and structure of existing AGENTS.md sections.
   - Use the same heading hierarchy, bullet styles, and code formatting conventions.

4. **Be Interactive:**
   - Never silently update documentation.
   - Always show proposed changes and get explicit approval before editing files.
   - Encourage the user to mark items as out of scope when appropriate.

5. **Avoid Scope Creep:**
   - This command is for reflecting concrete changes from recent logs.
   - Large refactors or structural documentation changes should go through a separate ticket/plan/implementation cycle.

6. **No Open Questions in Final Docs:**
   - Do not leave TODOs, "TBD", or speculative statements in AGENTS.md.
   - If a question cannot be resolved, leave the existing docs unchanged and flag the issue to the user.

## Success Criteria

- AGENTS.md accurately reflects all documentation-relevant changes described in the processed logs.
- No unrelated sections are modified.
- All edits were explicitly approved by the user before being applied.
- The user confirms that the final changes match their expectations.

---

Use the todowrite tool to create a structured task list for the 8 steps above, marking each as pending initially.

Further information from the user if any is below:

$ARGUMENTS
