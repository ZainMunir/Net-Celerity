source config.cfg

total_clients=30
clients_per_node=$(($total_clients / client_nodes_number))

for i in $(seq 1 $num_players2); do
    node_index=$(( ((i-1) % client_nodes_number) + 1 ))
    client_node_var="client_node$node_index"
    client_node=${!client_node_var}
    
    # If this is the first client on the node, start system monitoring
    if (( ((i - 1) / client_nodes_number)  == 0 )); then
        client_monitor_log="${system_logs}client_node${node_index}.csv"
        echo "Starting system monitoring script on $client_node..."
    #     ssh $client_node "python3 ${client_system_monitor_script} ${client_monitor_log} &" &
    fi

    echo "Starting client $i on $client_node..."
    # simulation_type=" -emulationType Simulation "
    # client_command="${shared_command} -serverUrl $server_ip -statsFile ${opencraft_stats}client$i.csv -userID $i -playType Client ${simulation_type} > ${opencraft_logs}client${i}.log 2>&1 &"
    # ssh $client_node "${client_command}" &
    if ((client_nodes_number == node_index)); then
        echo "Sleeping for $client_interval seconds..."
        sleep $client_interval
    fi
done
