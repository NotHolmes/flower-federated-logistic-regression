#!/bin/bash
set -e
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/

if [[ "$1" == "--client-only" || "$1" == "-cl" ]]; then
    :  # Do nothing if client-only mode is specified
elif [[ "$1" == "--trim" || "$1" == "-t" ]]; then
    echo "Starting FedTrimmedAvg server"
    python src/server_fedtrimmedavg.py &
    sleep 3  # Sleep for 3s to give the server enough time to start
elif [[ "$1" == "--med" || "$1" == "-m" ]]; then
    echo "Starting FedMedian server"
    python src/server_fedmedian.py &
    sleep 3  # Sleep for 3s to give the server enough time to start
elif [[ "$1" == "--avg" || "$1" == "-a" ]]; then
    echo "Starting FedAvg server"
    python src/server.py &
    sleep 3  # Sleep for 3s to give the server enough time to start
elif [[ "$1" == "--krum" || "$1" == "-k" ]]; then
    echo "Starting Krum server"
    python src/server_krum.py &
    sleep 3  # Sleep for 3s to give the server enough time to start
else
    echo "Starting default (FedAvg) server"
    python src/server.py &
    sleep 3  # Sleep for 3s to give the server enough time to start
fi

for i in $(seq 0 $(( $2 - 1 ))); do
    echo "Starting client $i"
    python src/client.py --client-id "${i}" --random_state "${i}" &
done

# This will allow you to use CTRL+C to stop all background processes
trap 'trap - SIGTERM && kill -- -$$' SIGINT SIGTERM
# Wait for all background processes to complete
wait
