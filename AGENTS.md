When reading json, jsonl, jsonc, yaml, or csv files, only read sections of them as they could be very large.

When adding CLI commands to programs, make sure to update the Makefile with the new command. Makefile commands should use short and descriptive names following existing naming conventions.

When using tmux commands, be careful when closing or ending sessions, as the agent is running in a tmux session, and stopping the tmux server will stop the agent and the execution. Use tmux naming conventions, and interact with tmux sessions by name or session.
