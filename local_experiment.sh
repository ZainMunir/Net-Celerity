#!/bin/bash

source local_config.cfg
mkdir -p server_logs
mkdir -p client_logs
mkdir -p system_logs

# Config (so I can have formatted strings)
## Folder locations
student_id="zmr280"
build_location="../"
home_folder="../"

## Build locations
build_folder="${build_location}Opencraft/"
raw_executable="Opencraft.exe"
opencraft_executable="${build_folder}${raw_executable}"
opencraft_logs="${build_folder}Opencraft_Data/Opencraft_logs/"

## Net-Celerity locations
net_celerity_folder="${home_folder}Net-Celerity/"
entities_inputs="${net_celerity_folder}DOTS-NFE-inputs/"
server_logs="${net_celerity_folder}server_logs/"
client_logs="${net_celerity_folder}client_logs/"
system_logs="${net_celerity_folder}system_logs/"
### Scripts
system_monitor_script="${net_celerity_folder}system_monitor.py"
client_system_monitor_script="${net_celerity_folder}client_system_monitor.py"
collect_script="${net_celerity_folder}collect_script.py"

shared_command="${opencraft_executable} -batchmode -nographics -logStats True"

server_ip="127.0.0.1"

echo "Starting server on CPU 0..."
server_command="${shared_command} -statsFile ${opencraft_logs}server_log.csv -playType Server -logFile ${home_folder}server.log"
echo $server_command
taskset -c 0 ${server_command} > ${server_logs}server_output.log 2>&1 &

sleep 5

server_pid=$(pgrep -f "$raw_executable.*Server")
if [ -z "$server_pid" ]; then
    echo "Failed to start server."
    exit 1
fi

echo "Server started with PID $server_pid"

echo "Starting system monitoring script for server with PID $server_pid..."
monitor_command="python3 ${system_monitor_script} ${system_logs}server_${num_players}p_${benchmark_duration}s.csv $server_pid"
echo $monitor_command
taskset -c 1 ${monitor_command} &
monitor_pid=$!

# Calculate number of clients per CPU core
clients_per_cpu=$((num_players / client_nodes_number))

echo "Starting clients..."

for cpu_index in $(seq 2 $((1 + client_nodes_number))); do
    start_client=$(( (cpu_index - 2) * clients_per_cpu + 1 ))
    end_client=$(( (cpu_index - 1) * clients_per_cpu ))

    for i in $(seq $start_client $end_client); do
        echo "Starting client $i on CPU $cpu_index..."
        client_command="${shared_command} -serverUrl $server_ip -statsFile ${opencraft_logs}/player_log_$i.csv -userID $i -playType Client -logFile ~/client_log_$i.log"
        echo $client_command
        taskset -c $cpu_index ${client_command} > ${client_logs}client${i}_output.log 2>&1 &
        sleep $client_interval
    done
done

echo "Benchmarking for $benchmark_duration seconds..."
sleep $benchmark_duration

echo "Stopping system monitoring script for server..."
kill $monitor_pid

echo "Stopping server..."
kill $server_pid
sleep 2
kill -0 $server_pid && kill -9 $server_pid

echo "Stopping clients..."
pkill -f "${raw_executable}.*Client"
sleep 2
pkill -0 "${raw_executable}.*Client" && pkill -9 "${raw_executable}.*Client"

echo "Running collection script..."
python3 $collect_script $opencraft_logs
wait

echo "Deleting server and client logs..."
rm -rf ./server_logs/*
rm -rf ./client_logs/*

echo "Deleting ECS logs..."
rm ${opencraft_logs}*

echo "Benchmarking completed."
echo "Script execution complete."
