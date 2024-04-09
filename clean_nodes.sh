#!/bin/bash

# Define server and client nodes
server_node="node001"
client_node="node002"

# Function to check and kill existing processes
check_and_kill_processes() {
    echo "Checking for existing processes on $1..."
    existing_processes=$(ssh $1 "ps aux | grep <process_name_pattern>")
    if [ -n "$existing_processes" ]; then
        echo "Existing processes found on $1. Killing them..."
        ssh $1 "pkill -f <process_name_pattern>"
    else
        echo "No existing processes found on $1."
    fi
}

# Check and kill existing processes on server node
check_and_kill_processes $server_node

# Check and kill existing processes on client node
check_and_kill_processes $client_node

# Continue with the rest of your benchmarking script...
