# Thoughts Application Project

## Requirements Summary

### Problem Statement
The current per-project thoughts directory workflow is functional but hacky, creating friction that discourages regular use. The system is non-transferable between projects, preventing knowledge reuse and pattern recognition across work. The goal is to create a unified, visually pleasant application that makes the ticket-to-archive workflow easy to use and provides visibility into the development process.

### Requirements

#### Functional Requirements
- Visualize the full development flow (ticket -> research -> plan -> execute -> review -> archive)
- Display tickets clearly and show how they transform into plans and execution logs
- Integrate with OpenCode CLI for reading/writing thoughts data from project contexts
- Support the existing workflow phases while making them more accessible
- Store data in app's own storage while remaining accessible from project contexts
- (Future) Knowledge base for searching past solutions, errors, and patterns across projects

#### Non-Functional Requirements
- Pleasant, simple UI that reduces friction compared to current markdown-file approach
- Self-hosted deployment (possibly via Tailscale for cross-computer access)
- Single-user focused (no multi-tenancy complexity needed)
- Prioritize usability over feature completeness (60% of current features, 100% more pleasant)

### Constraints & Boundaries
- Must work with existing OpenCode subagents (codebase-locator, codebase-analyzer, etc.)
- Subagents run locally in project context, not in the web app
- App provides visualization and organization; heavy lifting stays in CLI/agents
- Cross-computer sync is nice-to-have, not core requirement

### Technical Context
- Current system: Markdown files in `thoughts/` directory per project
- Existing commands: `/ticket`, `/research`, `/plan`, `/execute`, `/review`, `/archive`
- Existing agents: codebase-locator, codebase-analyzer, codebase-pattern-finder, thoughts-locator, thoughts-analyzer
- Potential deployment: Self-hosted web app, possibly behind Tailscale

### Decisions Made
- Start with visualization of the workflow process as the core feature
- Knowledge base / cross-project search is Phase 2, not MVP
- Simpler tool preferred over fully-featured complex system
- Data lives in app storage, accessed via API from OpenCode CLI
- Single user only for initial version

### Out of Scope (MVP)
- Multi-user / team collaboration features
- Complex cross-project knowledge base with semantic search
- Running codebase analysis agents from within the web app
- Mobile app or native desktop app
- Real-time collaboration

---

## Detailed Project Understanding

### The Core Problem

The current thoughts directory system works but has significant friction:

1. **Setup overhead**: Creating the directory structure per-project feels manual and repetitive
2. **Visibility**: Markdown files in a folder don't provide good visibility into the workflow state
3. **Non-transferable**: Knowledge stays siloed in each project with no way to reference past solutions
4. **Feels hacky**: The system works but doesn't feel like a "real" tool, discouraging consistent use

### What Success Looks Like

A web application where you can:
- See all your active tickets across projects at a glance
- Watch a ticket progress through research -> plan -> execution -> archive
- Quickly understand the current state of any development task
- (Eventually) Search "how did I solve X before?" and find relevant past work

### Architecture Vision

```
+------------------+     API calls      +-------------------+
|   OpenCode CLI   | <----------------> |   Thoughts App    |
|  (runs locally)  |                    |  (self-hosted)    |
+------------------+                    +-------------------+
        |                                       |
        v                                       v
+------------------+                    +-------------------+
| Local Codebase   |                    |   App Database    |
| (project files)  |                    | (tickets, plans,  |
+------------------+                    |  logs, etc.)      |
                                        +-------------------+
```

- **OpenCode CLI**: Continues to run locally, has access to codebase for agents
- **Thoughts App**: Web UI for visualization, stores all thoughts data
- **Integration**: CLI commands (`/ticket`, `/plan`, etc.) write to app via API instead of local files

### Workflow Preservation

The existing flow should be preserved but made more visible:

```
ticket -> research -> plan -> execute -> review -> archive
         (optional)          (optional)
```

Each phase creates artifacts that the app displays in a connected, visual way:
- Ticket cards showing status, priority, type
- Research documents linked to their tickets
- Plans showing phases with completion status
- Execution logs with deviation tracking
- Archive view for completed work

### Knowledge Base (Phase 2)

The future knowledge base would:
- Auto-generate summaries from execution logs (what was done, errors encountered, solutions found)
- Create searchable entries with descriptive titles
- Allow semantic or keyword search across all projects
- Surface relevant past work when creating new tickets or plans

This is explicitly deferred to keep MVP simple.

### Technology Considerations

Not yet decided, but considerations:
- Web framework: Something simple (could be as basic as a static site with API, or a full framework)
- Database: SQLite for simplicity, or Postgres if more features needed
- API: REST or simple RPC for CLI integration
- Deployment: Docker container, self-hosted, possibly behind Tailscale

### Open Questions for Future Exploration

1. Should the app have any "active" features (like triggering agent runs), or purely passive visualization?
2. How should project context be handled - explicit project selection, or inferred from API calls?
3. What's the migration path from existing thoughts directories to the new system?
4. Should there be any offline/local-first capabilities, or is always-connected acceptable?
