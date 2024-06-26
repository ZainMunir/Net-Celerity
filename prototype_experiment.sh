# #!/bin/bash
# module load prun

# source config.cfg

# mkdir -p server_logs
# mkdir -p client_logs

# server_ip=$(ssh $server_node "hostname -I | cut -d ' ' -f1")

# echo "Starting server on $server_node at $server_ip:7777..."
# ssh $server_node "${prototype_server_command} > ./Net-Celerity/server_logs/server_output.log 2>&1 &" &

# sleep 5

# server_pid=$(ssh $server_node "pgrep -f '${prototype_server_command}'")

# echo "Starting system monitoring script on $server_node..."
# ssh $server_node "python3 Net-Celerity/system_monitor.py ./Net-Celerity/system_logs/${prototype_name}/system_log_${num_players}p_${benchmark_duration}s.csv $server_pid &" &


# # echo "--------------------------------------"
# # if [ -f "${mirror_inputs}player_input111.inputtrace" ]; then
# #     echo "File exists!"
# # else
# #     echo "File does not exist."
# # fi
# # echo "--------------------------------------"

# echo "Starting clients on $client_node..."
# for i in $(seq 1 $num_players)
# do
#     # if ssh -n "$client_node" "[ -f "${mirror_inputs}player_input${i}.inputtrace" ]"; then
#     #     echo "${mirror_inputs}player_input${i}.inputtrace exists!"
#     # else
#     #     echo "${mirror_inputs}player_input${i}.inputtrace does not exist."
#     # fi

#     echo "Starting client $i..."
#     ssh $client_node "$prototype_client_command -server_ip $server_ip -server_port 7777 -client -emulationType Playback -emulationFile ${mirror_inputs}player_input${i}.inputtrace > ./Net-Celerity/client_logs/client${i}_output.log 2>&1 &" &
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
# ssh $client_node "pkill ${prototype_name}.x86_64"
# sleep 2
# ssh $client_node "pkill -0 ${prototype_name}.x86_64" && ssh $client_node "pkill -9 ${prototype_name}.x86_64"

# echo "Running collection script.."
# python3 $collection_script $prototype_logs $output_file 
# wait 20

# echo "Deleting server and client logs..."
# rm -rf ./server_logs/*
# rm -rf ./client_logs/*

# echo "Deleting mirror logs..."
# rm ${prototype_logs}/*

# echo "Benchmarking completed."
# echo "Script execution complete."


#!/bin/bash
module load prun

source config.cfg

mkdir -p server_logs
mkdir -p client_logs

server_ip=$(ssh $server_node "hostname -I | cut -d ' ' -f1")

echo "Starting server on $server_node at $server_ip:7777..."
ssh $server_node "${prototype_server_command} > ./Net-Celerity/server_logs/server_output.log 2>&1 &" &

sleep 5

server_pid=$(ssh $server_node "pgrep -f '${prototype_server_command}'")

echo "Starting system monitoring script on $server_node..."
ssh $server_node "python3 Net-Celerity/system_monitor.py ./Net-Celerity/system_logs/${prototype_name}/system_log_${num_players}p_${benchmark_duration}s.csv $server_pid &" &

# Calculate number of clients per node
clients_per_node=$((num_players / client_nodes_number))

echo "Starting clients..."

for node_index in $(seq 1 $client_nodes_number); do
    client_node_var="client_node$node_index"
    client_node=${!client_node_var}

    start_client=$(( (node_index - 1) * clients_per_node + 1 ))
    end_client=$(( node_index * clients_per_node ))

    for i in $(seq $start_client $end_client); do
        echo "Starting client $i on $client_node..."
        # ssh $client_node "$prototype_client_command -server_ip $server_ip -server_port 7777 -client -emulationType Playback -emulationFile ${mirror_inputs}player_input${i}.inputtrace > ./Net-Celerity/client_logs/client${i}_output.log 2>&1 &" &
        ssh $client_node "$prototype_client_command -server_ip $server_ip -server_port 7777 -client > ./Net-Celerity/client_logs/client${i}_output.log 2>&1 &" &
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
    client_node_var="client_node$node_index"
    client_node=${!client_node_var}
    ssh $client_node "pkill ${prototype_name}.x86_64"
    sleep 2
    ssh $client_node "pkill -0 ${prototype_name}.x86_64" && ssh $client_node "pkill -9 ${prototype_name}.x86_64"
done

echo "Running collection script.."
python3 $collection_script $prototype_logs $output_file 
wait

echo "Deleting server and client logs..."
rm -rf ./server_logs/*
rm -rf ./client_logs/*

echo "Deleting prototype logs..."
rm ${prototype_logs}/*

echo "Benchmarking completed."
echo "Script execution complete."
