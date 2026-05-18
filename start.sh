#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "$TMUX" ]; then
  echo "Error: must be run inside a tmux session."
  exit 1
fi

# Create new window and capture its unique id (e.g. @4) — immune to name conflicts
WID=$(tmux new-window -n 'milliways' -P -F '#{window_id}')

# Split into left (backend) and right (frontend) — right pane becomes active
tmux split-window -h -t "$WID"

# Right pane is active — start frontend
tmux send-keys -t "$WID" "cd '$SCRIPT_DIR/frontend' && npm run dev -- --host" Enter

# Move left and start backend
tmux select-pane -t "$WID" -L
tmux send-keys -t "$WID" "cd '$SCRIPT_DIR' && PYTHONPATH=backend uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload" Enter
