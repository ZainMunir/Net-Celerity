#!/bin/bash

module load prun

source config.cfg

mkdir -p server_logs
mkdir -p client_logs

server_ip=$(ssh $server_node "hostname -I | cut -d ' ' -f1")
echo "Starting server on $server_node at $server_ip:7979..."
ssh $server_node "$entities_folder/entities/entities.x86_64 -batchmode -nographics -logStats true -statsFile $entities_folder/server_log.csv -playType Server > ./benchmark/server_logs/server_output.log 2>&1 &"

server_pid=$(ssh $server_node "pgrep -f entities.x86_64")

sleep 5

# echo "Starting system monitoring script on $server_node..."
# ssh $server_node "export PATH=\"/home/esu530/miniconda3/bin:$PATH\" && conda activate && python3 ./benchmark/system_monitor.py $server_pid &" &

server_pid=$(ssh $server_node "pgrep -f '$entities_folder/entities/entities.x86_64 -batchmode -nographics'")
echo "Starting system monitoring script on $server_node..."
ssh $server_node "python3 benchmark/system_monitor.py ./benchmark/system_logs/entities/system_log.log $server_pid &" &

echo "Starting clients on $client_node..."
for i in $(seq 1 $num_players)
do
    echo "Starting client $i..."
    ssh $client_node "$entities_folder/entities/entities.x86_64 -batchmode -nographics -serverUrl $server_ip -logStats true -statsFile $entities_logs/player_log_$i.csv -userID $i -playType Client > ./benchmark/client_logs/client${i}_output.log 2>&1 &" &
    sleep 3
done

sleep 5

echo "Benchmarking for $benchmark_duration seconds..."
sleep $benchmark_duration

echo "Stopping system monitoring script on $server_node..."
ssh $server_node "pkill -f 'python3 benchmark/system_monitor.py'"

echo "Stopping server..."
ssh $server_node "kill $server_pid"
sleep 2
# Check if server process is still running and force terminate if necessary
ssh $server_node "pgrep -f entities.x86_64" && ssh $server_node "pkill -9 -f entities.x86_64"

echo "Stopping clients..."
ssh $client_node "pkill -f entities.x86_64"
sleep 2
ssh $client_node "pgrep -f entities.x86_64" && ssh $client_node "pkill -9 -f entities.x86_64"

echo "Running collection script.."
python3 ./entities_collect_script.py $entities_logs
wait 10

# Delete server and client logs
echo "Deleting server and client logs..."
rm -rf ./server_logs/*
rm -rf ./client_logs/*

Delete mirror logs folder
echo "Deleting mirror logs folder..."
rm -rf $entities_logs 

echo "Benchmarking completed."

echo "Script execution complete."
