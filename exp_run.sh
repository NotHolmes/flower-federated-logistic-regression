#!/bin/bash
set -e
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/

# Check if the loop count is provided as a command-line argument
if [[ $# -eq 0 ]]; then
    echo "Usage: ./exp_run.sh <model> <loop_count>"
    exit 1
fi

# Store the loop count in a variable
loop_count=$1

# Function to run the script
run_script() {
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
    elif [[ "$1" == "--krum" || "$1" == "-k" ]]; then
        echo "Starting Krum server"
        python src/server_krum.py &
        sleep 3  # Sleep for 3s to give the server enough time to start
    elif [[ "$1" == "--avg" || "$1" == "-a" ]]; then
        echo "Starting Krum server"
        python src/server.py &
        sleep 3  # Sleep for 3s to give the server enough time to start
    else
        echo "Starting default (FedAvg) server"
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

    # Run python src/matrices.py after server and client are done
    python src/matrices.py --model "$1" >> "logs/$1_result.txt"
}

# Loop the script based on the provided loop count
for ((count=1; count<=$loop_count; count++)); do
    echo "Loop $count"
    run_script "$@"
done
