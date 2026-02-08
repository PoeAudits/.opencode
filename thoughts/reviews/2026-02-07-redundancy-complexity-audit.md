# Redundancy + Complexity Audit (Phase 2 + 3)

Date: 2026-02-07
Project root: `/home/thomas/.config/opencode`
Scope reviewed: `plugin/`, `tools/`, `dev/`, `agent/`, `command/`, `skills/`
Focus topics: Redundancy, Complexity

## Notes on Scope

- Executable JS/TS code was found in `plugin/` only.
- `tools/`, `dev/`, `agent/`, `command/`, and `skills/` are mostly markdown/content in this snapshot and produced no JS/TS findings.
- Ignored generated/vendored paths (`node_modules`, `.git`, `dist`, `build`, `vendor`, etc.).

## Phase 2: Consolidated Findings

Impact score rubric (1-10): weighted by lines affected, centrality/hot-path potential, and blast radius.

### Category: Redundancy

#### 1) Pending operation CRUD duplicated by operation type
- File/lines: `plugin/opencode-worktree/src/plugin/worktree/state.ts:265-412`
- Description: Pending spawn and pending delete helpers repeat parse/validate/log/SQL boilerplate with only operation type changing.
- Impact: **8/10**
- Frequency: **2 repeated helper groups** (spawn/delete) with mirrored set/get/clear logic
- Fix effort: ~60-90 lines changed, 1 file, low-medium regression risk (state persistence behavior)
- Estimated simplifiable lines: ~80-120

#### 2) Detached-script spawn sequence duplicated across macOS terminal cases
- File/lines: `plugin/opencode-worktree/src/plugin/worktree/terminal.ts:388-469`
- Description: `kitty`, `alacritty`, and `warp` branches duplicate temp script write/chmod/detached spawn/cleanup pattern.
- Impact: **7/10**
- Frequency: **3 terminal-case repeats**
- Fix effort: ~40-70 lines changed, 1 file, medium risk (platform-specific launch behavior)
- Estimated simplifiable lines: ~50-80

#### 3) Cross-platform detached launch flow reimplemented (Linux/Windows/WSL)
- File/lines: `plugin/opencode-worktree/src/plugin/worktree/terminal.ts:569-949`
- Description: Similar escape/wrap/write/chmod/spawn/unref/cleanup lifecycle appears in multiple platform functions.
- Impact: **9/10**
- Frequency: **3 platform families + several terminal variants**
- Fix effort: ~120-220 lines changed, 1 file, medium-high risk (cross-OS behavior)
- Estimated simplifiable lines: ~140-220

### Category: Complexity

#### 4) Monolithic terminal orchestration module
- File/lines: `plugin/opencode-worktree/src/plugin/worktree/terminal.ts:1-996`
- Description: Nearly 1k-line module mixes tmux logic, platform detection, launch policies, and script generation.
- Impact: **10/10**
- Frequency: **Systemic in module**
- Fix effort: ~250-450 lines moved/edited, 3-6 files touched if split by platform, medium-high risk
- Estimated simplifiable lines: ~150-300 (plus major readability gain)

#### 5) Monolithic worktree plugin module
- File/lines: `plugin/opencode-worktree/src/plugin/worktree.ts:1-962`
- Description: Single file combines schemas, git/file orchestration, config loading, tool definitions, and lifecycle handlers.
- Impact: **10/10**
- Frequency: **Systemic in module**
- Fix effort: ~250-500 lines moved/edited, 4-8 files touched if modularized, medium-high risk
- Estimated simplifiable lines: ~120-260 (plus major maintainability gain)

#### 6) `openLinuxTerminal` has deeply nested branching and fallback state-machine logic
- File/lines: `plugin/opencode-worktree/src/plugin/worktree/terminal.ts:592-707`
- Description: Nested try/closure/switch/loops/returns increase cognitive load and obscure failure-path behavior.
- Impact: **8/10**
- Frequency: **1 large function**
- Fix effort: ~80-150 lines changed, 1-2 files, medium risk
- Estimated simplifiable lines: ~60-110

#### 7) Oversized `WorktreePlugin` entry closure
- File/lines: `plugin/opencode-worktree/src/plugin/worktree.ts:742-959`
- Description: Logging setup, database init, tool declarations, and idle event behavior live in one closure.
- Impact: **8/10**
- Frequency: **1 entrypoint closure with many responsibilities**
- Fix effort: ~90-170 lines changed, 2-4 files, medium risk
- Estimated simplifiable lines: ~60-120

#### 8) `forkWithContext` mixes validation, session traversal, FS actions, and cleanup
- File/lines: `plugin/opencode-worktree/src/plugin/worktree.ts:228-335`
- Description: Long multipurpose function with several concern boundaries.
- Impact: **7/10**
- Frequency: **1 multipurpose function**
- Fix effort: ~60-110 lines changed, 1-3 files, medium risk
- Estimated simplifiable lines: ~40-80

#### 9) `loadWorktreeConfig` couples default file creation with parse/validation
- File/lines: `plugin/opencode-worktree/src/plugin/worktree.ts:627-697`
- Description: Bootstrapping and parsing concerns interleaved, increasing branch complexity.
- Impact: **6/10**
- Frequency: **1 function**
- Fix effort: ~35-70 lines changed, 1-2 files, low-medium risk
- Estimated simplifiable lines: ~20-45

#### 10) `copyFiles` nested error/exists handling paths
- File/lines: `plugin/opencode-worktree/src/plugin/worktree.ts:525-553`
- Description: Nested guard/try/catch/exists checks with repeated logging branches.
- Impact: **5/10**
- Frequency: **1 function**
- Fix effort: ~20-45 lines changed, 1 file, low risk
- Estimated simplifiable lines: ~15-30

#### 11) `formatMarkdownTables` nested loop/conditional control flow
- File/lines: `plugin/opencode-md-table-formatter/index.ts:30-47`
- Description: Four-level control stack and repeated push behavior for pass-through vs format path.
- Impact: **4/10**
- Frequency: **1 function**
- Fix effort: ~15-30 lines changed, 1 file, low risk
- Estimated simplifiable lines: ~10-20

#### 12) Long `getProjectId` helper with many fallback branches
- File/lines: `plugin/opencode-worktree/src/plugin/kdco-primitives/get-project-id.ts:59-172`
- Description: Caching, git-dir resolution, command execution, and fallback strategy are tightly coupled.
- Impact: **6/10**
- Frequency: **1 function**
- Fix effort: ~40-90 lines changed, 1-2 files, low-medium risk
- Estimated simplifiable lines: ~25-55

## Summary Table

| Metric | Value |
|---|---:|
| Total issues found | 12 |
| Redundancy issues | 3 |
| Complexity issues | 9 |
| Estimated lines simplifiable/removed (Redundancy) | 270-420 |
| Estimated lines simplifiable/removed (Complexity) | 500-1,020 |
| Total estimated lines simplifiable/removed | 770-1,440 |

## Phase 3: Improvement Plan (Ranked by Impact/Effort)

Ranking uses approximate `impact / effort` with preference for low-risk, high-centrality wins.

### Phase A - Quick wins (high value, low risk)

#### Batch A1: Consolidate pending-operation state helpers
- Files: `plugin/opencode-worktree/src/plugin/worktree/state.ts`
- Approach: Introduce typed generic helpers for pending op CRUD (`setPendingOp/getPendingOp/clearPendingOp`) keyed by op type; retain schema checks.
- Risk/testing: Low-medium. Test spawn/delete pending lifecycle and schema parse failures.
- Expected simplification: 80-120 lines.

#### Batch A2: Simplify table formatter control flow
- Files: `plugin/opencode-md-table-formatter/index.ts`
- Approach: Extract row-collection and validation decisions into small helpers; flatten nested branches.
- Risk/testing: Low. Test mixed markdown blocks and malformed tables.
- Expected simplification: 10-20 lines.

#### Batch A3: Flatten `copyFiles` error handling
- Files: `plugin/opencode-worktree/src/plugin/worktree.ts`
- Approach: Use early-continue/early-return and helper for skip-vs-fail logging to reduce nested blocks.
- Risk/testing: Low. Test missing source, existing target, and hard failure paths.
- Expected simplification: 15-30 lines.

### Phase B - Medium effort (targeted structural cleanup)

#### Batch B1: Extract terminal detached-launch utility
- Files: `plugin/opencode-worktree/src/plugin/worktree/terminal.ts`
- Approach: Create shared helper for temp script lifecycle (render/write/chmod/spawn/cleanup), then call per platform/case.
- Risk/testing: Medium. Validate macOS, Linux, Windows/WSL launch paths and fallback ordering.
- Expected simplification: 190-300 lines.

#### Batch B2: Split `forkWithContext` into concern helpers
- Files: `plugin/opencode-worktree/src/plugin/worktree.ts` (+ optional helper file)
- Approach: Separate client/session resolution, fork FS operations, and cleanup/reconcile steps.
- Risk/testing: Medium. Validate active-session checks and cleanup on partial failures.
- Expected simplification: 40-80 lines.

#### Batch B3: Separate config bootstrapping from parsing
- Files: `plugin/opencode-worktree/src/plugin/worktree.ts`
- Approach: Extract `ensureConfigFileExists` and `parseConfig` helpers; keep logging and defaults deterministic.
- Risk/testing: Low-medium. Test first-run config generation and invalid file recovery.
- Expected simplification: 20-45 lines.

#### Batch B4: Decompose `getProjectId` fallback chain
- Files: `plugin/opencode-worktree/src/plugin/kdco-primitives/get-project-id.ts`
- Approach: Isolate cache lookup, git-dir derivation, and fallback normalization into composable helpers.
- Risk/testing: Low-medium. Test worktree/main repo edge cases and cache reuse.
- Expected simplification: 25-55 lines.

### Phase C - Deep refactors (largest payoff, higher coordination)

#### Batch C1: Modularize terminal by platform
- Files: `plugin/opencode-worktree/src/plugin/worktree/terminal.ts` into platform files (e.g., `terminal.macos.ts`, `terminal.linux.ts`, `terminal.windows.ts`, shared launcher helpers)
- Approach: Keep public `openTerminal` contract stable; delegate to per-platform modules and shared primitives.
- Risk/testing: Medium-high. Requires regression checks on every supported terminal path and tmux behavior.
- Expected simplification: 150-300 lines (plus large readability improvement).

#### Batch C2: Break `worktree.ts` into domain modules
- Files: `plugin/opencode-worktree/src/plugin/worktree.ts` split into modules (config, sync/copy/link, session lifecycle, tool handlers)
- Approach: Keep plugin entry minimal and wire together focused services/functions.
- Risk/testing: Medium-high. Must preserve tool behavior and lifecycle hooks.
- Expected simplification: 120-260 lines (plus strong maintainability gain).

#### Batch C3: Slim `WorktreePlugin` entrypoint
- Files: `plugin/opencode-worktree/src/plugin/worktree.ts` (+ extracted handler files)
- Approach: Move tool definitions and idle-event handlers to dedicated factories; entrypoint should compose only.
- Risk/testing: Medium. Validate tool registration, database initialization, and event-triggered cleanup.
- Expected simplification: 60-120 lines.

## Highest-Impact Findings

1. `plugin/opencode-worktree/src/plugin/worktree/terminal.ts` monolithic + duplicated launch flow (impact 9-10).
2. `plugin/opencode-worktree/src/plugin/worktree.ts` monolithic plugin orchestration (impact 10).
3. Pending-operation CRUD duplication in `state.ts` (impact 8, easy to medium effort).

## Execution Update

### Phase A status: completed
- Consolidated pending operation CRUD helpers in `state.ts`.
- Flattened markdown table formatting control flow.
- Simplified nested copy-file error handling.

### Phase B status: completed
- Extracted shared detached-launch behavior.
- Decomposed `forkWithContext` into focused helpers.
- Split config bootstrapping/parsing flow.
- Decomposed `getProjectId` cache/fallback chain.

### Phase C status: completed
- Terminal orchestration split into platform modules:
  - `plugin/opencode-worktree/src/plugin/worktree/terminal_macos.ts`
  - `plugin/opencode-worktree/src/plugin/worktree/terminal_linux.ts`
  - `plugin/opencode-worktree/src/plugin/worktree/terminal_windows.ts`
  - Shared primitives in `plugin/opencode-worktree/src/plugin/worktree/terminal_shared.ts`
  - Slim dispatcher in `plugin/opencode-worktree/src/plugin/worktree/terminal.ts`
- Worktree logger extracted to `plugin/opencode-worktree/src/plugin/worktree/worktree_logger.ts` and wired into plugin entry.
- Tool/event orchestration extracted into `plugin/opencode-worktree/src/plugin/worktree/worktree_handlers.ts`.
- Plugin entry in `plugin/opencode-worktree/src/plugin/worktree.ts` now composes handler dependencies and delegates create/delete/event logic.
- Runtime operations extracted to `plugin/opencode-worktree/src/plugin/worktree/worktree_runtime.ts` (git ops, sync ops, config load, attach/spawn command helpers).
- DB lifecycle extracted to `plugin/opencode-worktree/src/plugin/worktree/worktree_db.ts` (retry init, singleton access, cleanup handlers).
- Session fork lifecycle extracted to `plugin/opencode-worktree/src/plugin/worktree/worktree_fork.ts` (session fork, context artifact copy, failure cleanup).
- `plugin/opencode-worktree/src/plugin/worktree.ts` now focuses on branch validation and dependency composition for plugin wiring.

### Validation notes
- Bun module import check passed for refactored terminal, handler, logger, project-id, `worktree_db`, and `worktree_fork` modules.
- Runtime + full plugin import remain blocked in this environment due missing `jsonc-parser` package resolution in local runtime.
