import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import shared_config as sc


def sort_list2_by_list1(list1, list2):
    order_dict = {value: index for index, value in enumerate(list1)}

    def extract_key(item):
        key_part = item.split(".")[0]
        return order_dict.get(key_part, float("inf"))

    sorted_list2 = sorted(list2, key=extract_key)

    return sorted_list2

order = [
    "Empty",
    "Empty (Logic Active)",
    "1-Layer (Logic Active)",
    "RollingHills",
    "RollingHills (Logic Active)",
]  

overhead_directory = f"{sc.data_directory}overhead/"

experiments = [d for d in os.listdir(overhead_directory) if os.path.isdir(os.path.join(overhead_directory, d))]

client_column_name = "cpu_percent"
server_column_name = "proc.cpu_percent"
experiment_averages = {}
server_averages = {}

for experiment in experiments:
    experiment_directory = f"{overhead_directory}{experiment}/"
    search = re.search(r"players(.+)", experiment)
    if search:
        val = search.group(1)
        if "-activeLogic" in val:
            val = f"{val.replace('-activeLogic_', '')} (Logic Active)"
        else:
            val = val.replace("_", "")
    else:
        raise ValueError(f"Invalid experiment name: {experiment}")    

    
    combinations = {}
    active_logic = False
    duration = 0
    for run in os.listdir(experiment_directory):
        run_path = f"{experiment_directory}{run}"
        if not active_logic:
            active_logic = "-activeLogic" in run
        if duration == 0 or duration is None:
            duration = re.search(r"_(\d+)s", run).group(1)
        
        player_num = re.search(r"_(\d+)p", run).group(1)
        
        if player_num not in combinations:
            combinations[player_num] = {
                "server": None,
                "clients": [],
            }
        if "server" in run:
            combinations[player_num]["server"] = run_path
        if "client" in run:
            combinations[player_num]["clients"].append(run_path)

    client_averages = {}
    server_averages_per_experiment = {}
    
    sorted_combinations = sorted(combinations.items(), key=lambda x: int(x[0]))
    
    for key, value in sorted_combinations:
        client_csv_files = value["clients"]
        server_csv_file = value["server"]
        
        client_data_frames = [pd.read_csv(csv_file) for csv_file in client_csv_files]
        server_data_frame = pd.read_csv(server_csv_file, sep=";")
        
        client_column_values = pd.concat([df[client_column_name] for df in client_data_frames])
        server_column_values = server_data_frame[server_column_name]
        
        client_averages[int(key)] = client_column_values.mean()
        server_averages_per_experiment[int(key)] = server_column_values.mean()
    
    experiment_averages[val] = client_averages
    server_averages[val] = server_averages_per_experiment

experiments = sort_list2_by_list1(order, list(experiment_averages.keys()))

all_player_nums = sorted({player_num for averages in experiment_averages.values() for player_num in averages.keys()})

output_file = f"{sc.plots_directory}cpu_usage"

# Plotting client CPU usage
bar_width = 1 / (len(experiments) + 1)
index = np.arange(len(all_player_nums))

plt.figure(figsize=(10, 6))

for i, experiment in enumerate(experiments):
    averages = experiment_averages[experiment]
    values = [averages.get(player_num, 0) for player_num in all_player_nums]
    plt.bar(index + i * bar_width, values, bar_width, label=experiment)

plt.xlabel('Number of Players')
plt.ylabel(f'CPU Usage (%) (Client)')
plt.xticks(index + bar_width * (len(experiments) - 1) / 2, all_player_nums)
plt.legend()

# plt.show()
plt.savefig(f"{output_file}_client.pdf", format="pdf")

# Plotting server CPU usage
plt.figure(figsize=(10, 6))

for i, experiment in enumerate(experiments):
    averages = server_averages[experiment]
    values = [averages.get(player_num, 0) for player_num in all_player_nums]
    plt.bar(index + i * bar_width, values, bar_width, label=experiment)

plt.xlabel('Number of Players')
plt.ylabel(f'CPU Usage (%) (Server)')
plt.xticks(index + bar_width * (len(experiments) - 1) / 2, all_player_nums)
plt.legend()

# plt.show()
plt.savefig(f"{output_file}_server.pdf", format="pdf")
