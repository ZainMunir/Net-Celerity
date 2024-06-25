# #!/bin/bash
# module load prun

# source config.cfg

# mkdir -p server_logs
# mkdir -p client_logs

# server_ip=$(ssh $server_node "hostname -I | cut -d ' ' -f1")

# echo "Starting server on $server_node at $server_ip:7777..."
# ssh $server_node "$mirror_kcp_folder/mirror_kcp/mirror_kcp.x86_64 -batchmode -nographics -server > ./Net-Celerity/server_logs/server_output.log 2>&1 &" &

# sleep 5

# server_pid=$(ssh $server_node "pgrep -f '$mirror_kcp_folder/mirror_kcp/mirror_kcp.x86_64 -batchmode -nographics -server'")
# echo "Starting system monitoring script on $server_node..."
# ssh $server_node "python3 Net-Celerity/system_monitor.py ./Net-Celerity/system_logs/mirror_kcp/system_log_${num_players}p_${benchmark_duration}s.csv $server_pid &" &

# echo "Starting clients on $client_node..."
# for i in $(seq 1 $num_players)
# do
#     echo "Starting client $i..."
#     ssh $client_node "$mirror_kcp_folder/mirror_kcp/mirror_kcp.x86_64 -batchmode -nographics -server_ip $server_ip -server_port 7777 -emulationType Playback -emulationFile ${mirror_inputs}player_input${i}.inputtrace -client > ./Net-Celerity/client_logs/client${i}_output.log 2>&1 &" &
#     sleep $clinet_interval
# done

# sleep 5

# echo "Benchmarking for $benchmark_duration seconds..."
# sleep $benchmark_duration

# echo "Stopping system monitoring script on $server_node..."
# ssh $server_node "pkill -f 'python3 Net-Celerity/system_monitor.py'"

# echo "Stopping server..."
# ssh $server_node "kill $server_pid"
# sleep 2
# ssh $server_node "kill -0 $server_pid" && ssh $server_node "kill -9 $server_pid"

# echo "Stopping clients..."
# ssh $client_node "pkill mirror_kcp.x86_64"
# sleep 2
# ssh $client_node "pkill -0 mirror_kcp.x86_64" && ssh $client_node "pkill -9 mirror_kcp.x86_64"

# echo "Running collection script.."
# python3 ./mirror_collect_script.py $mirror_kcp_logs
# wait 20

# echo "Deleting server and client logs..."
# rm -rf ./server_logs/*
# rm -rf ./client_logs/*

# echo "Deleting mirror logs..."
# rm ${mirror_kcp_logs}/*

# echo "Benchmarking completed."
# echo "Script execution complete."

#!/bin/bash
module load prun

source config.cfg

mkdir -p server_logs
mkdir -p client_logs

server_ip=$(ssh $server_node "hostname -I | cut -d ' ' -f1")

echo "Starting server on $server_node at $server_ip:7777..."
ssh $server_node "$mirror_kcp_folder/mirror_kcp/mirror_kcp.x86_64 -batchmode -nographics -server > ./Net-Celerity/server_logs/server_output.log 2>&1 &" &

sleep 5

server_pid=$(ssh $server_node "pgrep -f '$mirror_kcp_folder/mirror_kcp/mirror_kcp.x86_64 -batchmode -nographics -server'")
echo "Starting system monitoring script on $server_node..."
ssh $server_node "python3 Net-Celerity/system_monitor.py ./Net-Celerity/system_logs/mirror_kcp/system_log_${num_players}p_${benchmark_duration}s.csv $server_pid &" &

# Calculate number of clients per node
clients_per_node=$((num_players / client_nodes_number))

echo "Starting clients..."

for node_index in $(seq 1 $client_nodes_number); do
    client_node_var="client_node$node_index"
    client_node=${!client_node_var}

    # Start system monitoring on client node
    # client_monitor_log="./Net-Celerity/client_system_logs/mirror_KCP/system_log_${num_players}p_${benchmark_duration}s_client_node${node_index}.csv"
    # ssh $client_node "python3 Net-Celerity/client_system_monitor.py ${client_monitor_log} &" &


    start_client=$(( (node_index - 1) * clients_per_node + 1 ))
    end_client=$(( node_index * clients_per_node ))

    for i in $(seq $start_client $end_client); do
        echo "Starting client $i on $client_node..."
        ssh $client_node "$mirror_kcp_folder/mirror_kcp/mirror_kcp.x86_64 -batchmode -nographics -server_ip $server_ip -server_port 7777 -emulationType Playback -emulationFile ${mirror_inputs}player_input${i}.inputtrace -client > ./Net-Celerity/client_logs/client${i}_output.log 2>&1 &" &
        # ssh $client_node "$mirror_kcp_folder/mirror_kcp/mirror_kcp.x86_64 -batchmode -nographics -server_ip $server_ip -server_port 7777 -client > ./Net-Celerity/client_logs/client${i}_output.log 2>&1 &" &
        sleep $clinet_interval
    done
done

sleep 5

echo "Benchmarking for $benchmark_duration seconds..."
sleep $benchmark_duration

echo "Stopping system monitoring script on $server_node..."
ssh $server_node "pkill -f 'python3 Net-Celerity/system_monitor.py'"

echo "Stopping server..."
ssh $server_node "kill $server_pid"
sleep 2
ssh $server_node "kill -0 $server_pid" && ssh $server_node "kill -9 $server_pid"

echo "Stopping clients..."
for node_index in $(seq 1 $client_nodes_number); do
    # Stop system monitoring on client node
    # ssh $client_node "pkill -f 'python3 Net-Celerity/client_system_monitor.py'"

    client_node_var="client_node$node_index"
    client_node=${!client_node_var}
    ssh $client_node "pkill mirror_kcp.x86_64"
    sleep 2
    ssh $client_node "pkill -0 mirror_kcp.x86_64" && ssh $client_node "pkill -9 mirror_kcp.x86_64"
done

echo "Running collection script.."
python3 ./mirror_collect_script.py $mirror_kcp_logs
wait

echo "Deleting server and client logs..."
rm -rf ./server_logs/*
rm -rf ./client_logs/*

echo "Deleting mirror logs..."
rm ${mirror_kcp_logs}/*

echo "Benchmarking completed."
echo "Script execution complete."

