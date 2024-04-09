#!/bin/bash
module load prun

# Define server and client nodes
server_node="node001"
client_node="node002"

# Create directories for logs if they don't exist
mkdir -p server_logs
mkdir -p client_logs

# Find out the IP address of the server node
server_ip=$(ssh $server_node "hostname -I | cut -d ' ' -f1")

# Start the server on the server node and redirect output to a file
echo "Starting server on $server_node at $server_ip:7979..."
ssh $server_node "./entities/entities.x86_64 -batchmode -nographics -logStats true -statsFile ./entities/entities_Data/entities_logs/server_log.csv -playType Server > ./benchmark/server_logs/server_output.log 2>&1 &"
# Capture the server process ID
server_pid=$(ssh $server_node "pgrep -f entities.x86_64")

# Introduce a delay to ensure the server process has started
sleep 5

# Start the system monitoring script on the server node with the server PID
echo "Starting system monitoring script on $server_node..."
ssh $server_node "export PATH=\"/home/esu530/miniconda3/bin:$PATH\" && conda activate && python3 ./benchmark/system_monitor.py $server_pid &" &

# Start clients on the client node and redirect output to separate files
echo "Starting clients on $client_node..."
for i in {1..120}
do
    echo "Starting client $i..."
    ssh $client_node "./entities/entities.x86_64 -batchmode -nographics -serverUrl $server_ip -logStats true -statsFile ./entities/entities_Data/entities_logs/player_log_$i.csv -userID $i -playType Client > ./benchmark/client_logs/client${i}_output.log 2>&1 &" &
    sleep 3
done

sleep 5

echo "Benchmarking for 1 minute..."
sleep 60

echo "Stopping system monitoring script on $server_node..."
ssh $server_node "pkill -2 -f 'python3 ./benchmark/system_monitor.py $server_pid'"

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
python3 ./entities_collect_script.py
wait 40

# Delete server and client logs
echo "Deleting server and client logs..."
rm -rf ./server_logs/*
rm -rf ./client_logs/*

# Delete mirror logs folder
echo "Deleting mirror logs folder..."
rm -rf ../entities/entities_Data/entities_logs/*

echo "Benchmarking completed."

echo "Script execution complete."
