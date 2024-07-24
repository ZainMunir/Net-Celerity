    #!/bin/bash
    
    source config.cfg
    mkdir -p server_logs
    mkdir -p client_logs
    mkdir -p system_logs

    # Config (so I can have formatted strings)
    ## Folder locations
    student_id="zmr280"
    build_location="/var/scratch/${student_id}/"
    home_folder="/home/${student_id}/"

    ##Build locations
    build_folder="${build_location}opencraft/"
    raw_executable="opencraft.x86_64"
    opencraft_executable="${build_folder}${raw_executable}"
    opencraft_logs="${build_folder}opencraft_Data/Opencraft_logs/"

    ## Net-Celerity locations
    net_celerity_folder="${home_folder}Net-Celerity/"
    entities_inputs="${net_celerity_folder}DOTS-NFE-inputs/"
    server_logs="${net_celerity_folder}server_logs/"
    client_logs="${net_celerity_folder}client_logs/"
    system_logs="${net_celerity_folder}system_logs/${terrain_type}/"
    mkdir -p ${system_logs}
    ### Scripts
    system_monitor_script="${net_celerity_folder}system_monitor.py"
    client_system_monitor_script="${net_celerity_folder}client_system_monitor.py"
    collect_script="${net_celerity_folder}collect_script.py"

    shared_command="${opencraft_executable} -batchmode -nographics -logStats True"

    server_ip=$(ssh $server_node "hostname -I | cut -d ' ' -f1")
    server_stats="${opencraft_logs}server_log_${terrain_type}_${num_players}p_${benchmark_duration}s.csv"
    echo "Starting server on $server_node at $server_ip:7777 with $terrain_type terrain..."
    server_command="${shared_command} -terrainType ${terrain_type} -statsFile ${server_stats}  -playType Server > ${server_logs}server_output.log 2>&1 &" # -logFile ${home_folder}server.log
    # echo "$server_command"
    ssh $server_node "${server_command}" &
    sleep 10

    server_pid=$(ssh $server_node "pgrep -f '$raw_executable'")
    echo "Starting system monitoring script on $server_node with PID $server_pid..."
    monitor_command="python3 ${system_monitor_script} ${system_logs}system_log_${num_players}p_${benchmark_duration}s.csv $server_pid"
    # echo "$monitor_command"
    ssh $server_node "${monitor_command}" &

    # Calculate number of clients per node
    clients_per_node=$((num_players / client_nodes_number))

    echo "Starting clients..."

    for node_index in $(seq 1 $client_nodes_number); do
        client_node_var="client_node$node_index"
        client_node=${!client_node_var}

        # Start system monitoring on client node
        client_monitor_log="${system_logs}client_node_${num_players}p_${benchmark_duration}s_node${node_index}.csv"
        ssh $client_node "python3 ${client_system_monitor_script} ${client_monitor_log} &" &

        start_client=$(( (node_index - 1) * clients_per_node + 1 ))
        end_client=$(( node_index * clients_per_node ))

        for i in $(seq $start_client $end_client); do
            echo "Starting client $i on $client_node..."
            # client_command="${shared_command} -serverUrl $server_ip -statsFile ${opencraft_logs}player_log_$i.csv -userID $i -playType Client > ${client_logs}client${i}_output.log 2>&1 &" # -logFile ${home_folder}client.log >
            client_command="${shared_command} -serverUrl $server_ip -statsFile ${opencraft_logs}player_log_$i.csv -userID $i -playType Client -emulationType Simulation > ${client_logs}client${i}_output.log 2>&1 &"
            # echo "$client_command"
            ssh $client_node "${client_command}" &
            sleep $client_interval
        done
    done

    sleep 5

    echo "Benchmarking for $benchmark_duration seconds..."
    sleep $benchmark_duration

    echo "Stopping system monitoring script on $server_node..."
    ssh $server_node "pkill -f 'python3 ${system_monitor_script}'"

    echo "Stopping server.. on $server_node."
    ssh $server_node "kill $server_pid"
    sleep 2
    ssh $server_node "kill -0 $server_pid" && ssh $server_node "kill -9 $server_pid"

    echo "Stopping clients..."
    for node_index in $(seq 1 $client_nodes_number); do
        # Stop system monitoring on client node
        ssh $client_node "pkill -f 'python3 ${client_system_monitor_script}'"

        client_node_var="client_node$node_index"
        client_node=${!client_node_var}
        ssh $client_node "pkill ${opencraft_executable}"
        sleep 2
        ssh $client_node "pkill -0 ${opencraft_executable}" && ssh $client_node "pkill -9 ${opencraft_executable}"
        echo "Stopped clients on $client_node."
    done

    ls ${opencraft_logs}
    echo "Running collection script..."
    python3 $collect_script $opencraft_logs ${terrain_type}_${num_players}p_${benchmark_duration}s
    wait

    mv ${server_logs}server_output.log ${home_folder}server_output_${terrain_type}_${num_players}p_${benchmark_duration}s.log
    echo "Deleting server and client logs..."
    # rm -rf ./server_logs/*
    # rm -rf ./client_logs/*

    mv $server_stats $build_location
    echo "Deleting ECS logs..."
    # rm ${opencraft_logs}*

    echo "Benchmarking completed."
    echo "Script execution complete."
