#!/usr/bin/env bash

set -euo pipefail

AGENT_DIR="/home/thomas/.config/opencode/agent"
PRIMARY_DIR="$AGENT_DIR/primary"
if [ "$1" = "to-pickle" ] || [ "$1" = "tp" ]; then
    TO="opencode/big-pickle"
    EXCLUDE_MODEL="opencode/big-pickle"
    echo "Changing model to $TO"
elif [ "$1" = "to-haiku" ] || [ "$1" = "th" ]; then
    TO="anthropic/claude-haiku-4-5"
    EXCLUDE_MODEL="anthropic/claude-haiku-4-5"
    echo "Changing model to $TO"
elif [ "$1" = "to-grok" ] || [ "$1" = "tg" ]; then
    TO="opencode/grok-code"
    EXCLUDE_MODEL="opencode/grok-code"
    echo "Changing model to $TO"
elif [ "$1" = "to-sonnet" ] || [ "$1" = "ts" ]; then
    TO="anthropic/claude-sonnet-4-5"
    EXCLUDE_MODEL="anthropic/claude-sonnet-4-5"
    echo "Changing model to $TO"
else
    echo "Usage: $0 [to-pickle|tp|to-haiku|th|to-grok|tg]"
    echo "  to-pickle, tp: Change to opencode/big-pickle"
    echo "  to-haiku, th: Change to anthropic/claude-haiku-4-5"
    echo "  to-grok, tg: Change to opencode/grok-code"
    echo "  to-sonnet, tg: Change to anthropic/claude-sonnet-4-5"
    exit 1
fi

count=0

while IFS= read -r file; do
    # Find any model line that doesn't match the target model
    if grep -q "^model: " "$file" && ! grep -q "^model: $TO" "$file"; then
        # Replace any model line with the target model
        sed -i "s|^model: .*|model: $TO|g" "$file"
        echo "Updated: $file"
        count=$((count + 1))
    fi
done < <(find "$AGENT_DIR" -name "*.md" -not -path "$PRIMARY_DIR/*")

echo "Updated $count agent files"
