#!/usr/bin/env bash

set -euo pipefail

AGENT_DIR="/home/thomas/.config/opencode/agent"
PRIMARY_DIR="$AGENT_DIR/primary"
if [ "$1" = "to-pickle" ] || [ "$1" = "tp" ]; then
    FROM="anthropic/claude-haiku-4-5"
    TO="opencode/big-pickle"
    echo "Changing model from $FROM to $TO"
elif [ "$1" = "to-haiku" ] || [ "$1" = "th" ]; then
    FROM="opencode/big-pickle"
    TO="anthropic/claude-haiku-4-5"
    echo "Changing model from $FROM to $TO"
elif [ "$1" = "to-grok" ] || [ "$1" = "tg" ]; then
    FROM="anthropic/claude-haiku-4-5"
    TO="opencode/grok-code"
    echo "Changing model from $FROM to $TO"
else
    echo "Usage: $0 [to-pickle|tp|to-haiku|th|to-grok|tg]"
    echo "  to-pickle, tp: Change from claude-haiku-4-5 to big-pickle"
    echo "  to-haiku, th: Change from big-pickle to claude-haiku-4-5"
    echo "  to-grok, tg: Change from claude-haiku-4-5 to grok-code"
    exit 1
fi

count=0

find "$AGENT_DIR" -name "*.md" -not -path "$PRIMARY_DIR/*" | while read -r file; do
    if grep -q "model: $FROM" "$file"; then
        sed -i "s|model: $FROM|model: $TO|g" "$file"
        echo "Updated: $file"
        count=$((count + 1))
    fi
done

echo "Updated $count agent files"