#!/bin/bash
module load prun

source config.cfg

mkdir -p server_logs
mkdir -p client_logs

server_ip=$(ssh $server_node "hostname -I | cut -d ' ' -f1")

echo "Starting server on $server_node at $server_ip:7777..."
ssh $server_node "$mirror_kcp_folder/mirror_kcp/mirror_kcp.x86_64 -batchmode -nographics -server > ./unity-net-benchmark/server_logs/server_output.log 2>&1 &" &

sleep 5

server_pid=$(ssh $server_node "pgrep -f '$mirror_kcp_folder/mirror_kcp/mirror_kcp.x86_64 -batchmode -nographics -server'")
echo "Starting system monitoring script on $server_node..."
ssh $server_node "python3 unity-net-benchmark/system_monitor.py ./unity-net-benchmark/system_logs/mirror_kcp/system_log_${num_players}p_${benchmark_duration}s.csv $server_pid &" &

echo "Starting clients on $client_node..."
for i in $(seq 1 $num_players)
do
    echo "Starting client $i..."
    ssh $client_node "$mirror_kcp_folder/mirror_kcp/mirror_kcp.x86_64 -batchmode -nographics -server_ip $server_ip -server_port 7777 -client > ./unity-net-benchmark/client_logs/client${i}_output.log 2>&1 &" &
    sleep $clinet_interval
done

sleep 5

echo "Benchmarking for $benchmark_duration seconds..."
sleep $benchmark_duration

echo "Stopping system monitoring script on $server_node..."
ssh $server_node "pkill -f 'python3 unity-net-benchmark/system_monitor.py'"

echo "Stopping server..."
ssh $server_node "kill $server_pid"
sleep 2
ssh $server_node "kill -0 $server_pid" && ssh $server_node "kill -9 $server_pid"

echo "Stopping clients..."
ssh $client_node "pkill mirror_kcp.x86_64"
sleep 2
ssh $client_node "pkill -0 mirror_kcp.x86_64" && ssh $client_node "pkill -9 mirror_kcp.x86_64"

echo "Running collection script.."
python3 ./mirror_collect_script.py $mirror_kcp_logs
wait 20

echo "Deleting server and client logs..."
rm -rf ./server_logs/*
rm -rf ./client_logs/*

echo "Deleting mirror logs..."
rm ${mirror_kcp_logs}/*

echo "Benchmarking completed."
echo "Script execution complete."
