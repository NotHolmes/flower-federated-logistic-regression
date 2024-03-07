#!/bin/bash
set -e
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/

if [[ "$1" != "--client-only" && "$1" != "-cl" ]]; then
    echo "Starting server"
    python src/server.py &
    sleep 3  # Sleep for 3s to give the server enough time to start
fi

for i in $(seq 0 1 2); do
    echo "Starting client $i"
    python src/client.py --client-id "${i}" &
done

# This will allow you to use CTRL+C to stop all background processes
trap 'trap - SIGTERM && kill -- -$$' SIGINT SIGTERM
# Wait for all background processes to complete
wait
