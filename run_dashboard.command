#!/bin/bash
export PATH="/opt/homebrew/Cellar/openjdk/26.0.2/bin:$PATH"
DIR="$(dirname "$0")"

# Check if Flask dashboard is running
if ! lsof -i :5050 > /dev/null; then
    echo "Starting Hack Computer Web Dashboard..."
    python3 "$DIR/dashboard/app.py" &
    sleep 2
fi

open http://localhost:5050
echo "Hack Computer Dashboard opened at http://localhost:5050"
