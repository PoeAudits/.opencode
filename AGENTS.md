When reading json, jsonl, jsonc, yaml, or csv files, only read sections of them as they could be very large.

When adding CLI commands to programs, make sure to update the Makefile with the new command. Makefile commands should use short and descriptive names following existing naming conventions.

When using tmux commands, be careful when closing or ending sessions, as the agent is running in a tmux session, and stopping the tmux server will stop the agent and the execution. Use tmux naming conventions, and interact with tmux sessions by name or session.

I often use speech-to-text, so if the prompt contains unfamiliar words or terms, try to infer the meaning from the context or similar sounding terms.

When using grep or glob tools make sure to include the proper flags to exclude hidden files and dependency folders like node_modules.

Opencode agents, skills, and commands are located in ~/.config/opencode folder and the source of truth.

Use the opencode-worktree workflow for all worktree lifecycle actions.  
- Create isolated work using worktree_create(branch, baseBranch?) instead of manual git worktree commands.  
- Delete worktrees using worktree_delete(reason) so hooks, snapshot commit, and cleanup run correctly.  
- Prefer server attach flow (opencode attach) in spawned worktree terminals.

There is no ~/.config/Claude directory, the config lives in ~/.config/opencode
