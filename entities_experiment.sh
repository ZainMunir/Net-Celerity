#!/bin/bash
module load prun

source config.cfg

mkdir -p server_logs
mkdir -p client_logs

server_ip=$(ssh $server_node "hostname -I | cut -d ' ' -f1")

echo "Starting server on $server_node at $server_ip:7777..."
ssh $server_node "${entities_folder}entities/entities.x86_64 -batchmode -nographics -logStats True -statsFile ${entities_logs}/server_log.csv -playType Server > ./Net-Celerity/server_logs/server_output.log 2>&1 &"
sleep 5

server_pid=$(ssh $server_node "pgrep entities.x86_64")
echo "Starting system monitoring script on $server_node..."
ssh $server_node "python3 Net-Celerity/system_monitor.py ./Net-Celerity/system_logs/entities/system_log_${num_players}p_${benchmark_duration}s.csv $server_pid &" &

# Calculate number of clients per node
clients_per_node=$((num_players / client_nodes_number))

echo "Starting clients..."

for node_index in $(seq 1 $client_nodes_number); do
    client_node_var="client_node$node_index"
    client_node=${!client_node_var}

    # Start system monitoring on client node
    # client_monitor_log="./Net-Celerity/client_system_logs/entities/system_log_${num_players}p_${benchmark_duration}s_client_node${node_index}.csv"
    # ssh $client_node "python3 Net-Celerity/client_system_monitor.py ${client_monitor_log} &" &

    start_client=$(( (node_index - 1) * clients_per_node + 1 ))
    end_client=$(( node_index * clients_per_node ))

    for i in $(seq $start_client $end_client); do
        echo "Starting client $i on $client_node..."
        # ssh $client_node "${entities_folder}entities/entities.x86_64 -batchmode -nographics -serverUrl $server_ip -logStats True -statsFile ${entities_logs}/player_log_$i.csv -userID $i -playType Client -emulationType Playback -emulationFile ${entities_inputs}player_input${i}.inputtrace > ./Net-Celerity/client_logs/client${i}_output.log 2>&1 &" &
        ssh $client_node "${entities_folder}entities/entities.x86_64 -batchmode -nographics -serverUrl $server_ip -logStats True -statsFile ${entities_logs}/player_log_$i.csv -userID $i -playType Client > ./Net-Celerity/client_logs/client${i}_output.log 2>&1 &" &
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
    ssh $client_node "pkill entities.x86_64"
    sleep 2
    ssh $client_node "pkill -0 entities.x86_64" && ssh $client_node "pkill -9 entities.x86_64"
done

echo "Running collection script..."
python3 ./entities_collect_script.py $entities_logs
wait

echo "Deleting server and client logs..."
rm -rf ./server_logs/*
rm -rf ./client_logs/*

echo "Deleting ECS logs..."
rm ${entities_logs}/*

echo "Benchmarking completed."
echo "Script execution complete."
