---
description: Archive tickets that have been implemented
---

## Task Context

You are responsible for archiving tickets that have been marked as **implemented** and are no longer active.  
All archived materials are stored in the `thoughts/archive` directory.

## Process Overview

### Step 1: Identify implemented tickets

Scan the files in `thoughts/tickets/` to find any tickets where the frontmatter includes a status of `implemented`.

Ticket files begin with a frontmatter block structured as follows:

```markdown
---
type: [bug|feature|debt]
priority: [high|medium|low]
created: [ISO date]
status: open
tags: [relevant-tags]
keywords: [comma-separated keywords]
patterns: [comma-separated patterns] 
---
# [TYPE-XXX]: [Descriptive Title]
```

When reading a ticket file, first read the top portion using:

```bash
head -n 30 path/to/file
```

If the frontmatter does not appear within the first 30 lines, read the remainder of the file to capture it fully.

---

### Step 2: Locate any related plan files

For each implemented ticket, search the `thoughts/plans/` directory for a corresponding plan file.  
Plan filenames generally match the ticket identifier, but if uncertain, open the plan file and confirm that it refers to the same ticket.  
Not every ticket will have an associated plan, which is acceptable.

---

### Step 3: Locate any related log files

For each implemented ticket, search the `thoughts/logs/` directory for a corresponding log file.  
Log filenames generally match the ticket identifier, but if uncertain, open the log file and confirm that it refers to the same ticket.  
Not every ticket will have an associated log, which is acceptable.

---

### Step 4: Confirm with the user

Before making any changes, present the user with a summary of:
- Which tickets have been identified as implemented  
- Which related plan files were found  
- The proposed archive directory structure that will be created

Use this check-in step to confirm which files should be moved before proceeding.

**Note:** Ticket files should include '[TICKET]' in their title, plan files should include '[PLAN]' in their title, and log files should include '[LOG]' in their title.

**Example of resulting file tree after archiving:**

```markdown
thoughts/
├── tickets/
│   ├── FEATURE-1020-improve-login-flow.md
│   ├── BUG-4313-crash-on-launch.md
│   └── DEBT-2201-refactor-database-layer.md
│
├── plans/
│   ├── PLAN-FEATURE-1020-login-enhancement.md
│   └── PLAN-BUG-4313-launch-crash-investigation.md
│
├── logs/
│   ├── LOG-login-flow.md
│   └── LOG-launch-crash-investigation.md
│
└── archive/
    ├── 2025-12-15_redesign-dashboard/
    │   ├── TICKET-FEATURE-0987-redesign-dashboard.md
    │   └── PLAN-FEATURE-0987-dashboard-redesign.md
    │
    ├── 2025-12-10-fix-memory-leak/
    │   ├── TICKET-BUG-3561-fix-memory-leak.md
    │   ├── LOG-fix-memory-leak.md
    │   └── PLAN-BUG-3561-memory-leak-resolution.md
    │
    └── 2025-12-05-remove-legacy-api/
        ├── TICKET-DEBT-1845-remove-legacy-api.md
        └── PLAN-DEBT-1845-cleanup-legacy-interfaces.md
```

---
```
```

### Step 4: Archive the implemented tickets

Once confirmed by the user:
1. Create a new directory in `thoughts/archive/` named in the format  
   `YYYY-MM-DD_<short-ticket-slug>` (e.g., `2025-12-15_redesign-dashboard/`).  
2. Move the implemented ticket file — and its related plan file, if one exists — into this new directory.  
3. Use **non-destructive** commands such as `mv` to perform the move.  
4. Repeat for each implemented ticket.

If a ticket does not have a corresponding plan, only the ticket file should be moved.

---

### Step 5: Update ticket status

After moving, edit each archived ticket file’s frontmatter to update:  
`status: implemented` → `status: archived`

This ensures the record clearly reflects its current state in the system.

---

### Step 6: Notify the user

After archiving is complete, provide the user with a summary listing:
- Which tickets were archived  
- The archive directories that were created  
- The final file tree (if applicable)

---

### General Guidelines

- **Do not delete** any files — use only safe, non-destructive operations (e.g., `mv`).  
- Always **verify** with the user before moving any files.  
- Keep the process transparent by summarizing which files are modified or moved.

---

**End of Process**
