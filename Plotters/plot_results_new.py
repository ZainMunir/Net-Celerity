import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import ceil
import shared_config as sc
import re

player_experiments = [
    f"{sc.data_directory}{x}/"
    for x in os.listdir(sc.data_directory)
    if "players" in x # and not "RollingHills" in x and not "TerrainCircuitry" in x
]

def cpu_usage_per_second(experiment_directories):
    player_numbers = set() 
    
    for experiment_directory in experiment_directories:
        experiment_name= os.path.basename(os.path.abspath(experiment_directory))
        for run in os.listdir(experiment_directory):
            run_directory = os.path.join(experiment_directory, run)
            if experiment_name in run and os.path.isdir(run_directory):  
                system_logs_folder = os.path.join(run_directory, "system_logs")
                
                player_number_search = re.search(r"_(\d+)p", run_directory)
                duration_seconds_search = re.search(r"_(\d+)s", run_directory)
                
                if player_number_search and duration_seconds_search:
                    player_number = int(player_number_search.group(1))
                    duration_seconds = int(duration_seconds_search.group(1))
                else:
                    print(f"Invalid experiment directory: {run_directory}")
                    return
                for file in os.listdir(system_logs_folder):
                    if file.endswith(".csv"):
                        csv_path = os.path.join(system_logs_folder, "server.csv")
                        df = pd.read_csv(csv_path, delimiter=";")
                        df = df.tail(duration_seconds)
                        player_numbers.add(player_number)
                
    for player_number in sorted(player_numbers):
        plt.figure(figsize=(10, 6))
        plt.title(f'{player_number} total players', fontsize=14)
        plt.xlabel("time [s]")
        plt.ylabel("CPU usage [%]")
        colors = ['red', 'green', 'orange', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
        color_index = 0
                
        for experiment_directory in experiment_directories:
                experiment_name= os.path.basename(os.path.abspath(experiment_directory))
                for run in os.listdir(experiment_directory):
                    run_directory = os.path.join(experiment_directory, run)
                    if experiment_name in run and os.path.isdir(run_directory):
                        system_logs_folder = os.path.join(run_directory, "system_logs")
                        player_number_search = re.search(r"_(\d+)p", run_directory)
                        current_player_number = int(player_number_search.group(1))
                        if current_player_number == player_number:
                            csv_path = os.path.join(system_logs_folder, "server.csv")
                            df = pd.read_csv(csv_path, delimiter=";")
                            df = df.tail(duration_seconds)
                            df.reset_index(drop=True, inplace=True) 
                            
                            search = re.search(r"players(.+)\/", run_directory)
                            if search:
                                val = search.group(1)
                                if "-activeLogic" in val:
                                    val = f"{val.replace('-activeLogic_', '')} (Logic Active)"
                                else: 
                                    val = search.group(1).replace("_", "")                
                            
                            
                            plt.plot(df.index, df['proc.cpu_percent'], label=f"{val}", linewidth=2, color=colors[color_index], alpha=0.8)
                            color_index += 1


        plt.legend(frameon=False, ncol=2)
        plt.title(f'{player_number} total players')
        plt.savefig(f'{sc.plots_directory}cpu_usage_players_{player_number}.pdf')
        

def cpu_usage_per_player(experiment_directories):
    player_numbers = set()
    cpu_data = []
    
    for experiment_directory in experiment_directories:
        experiment_name= os.path.basename(os.path.abspath(experiment_directory))
        for run in os.listdir(experiment_directory):
            run_directory = os.path.join(experiment_directory, run)
            if experiment_name in run and os.path.isdir(run_directory):  
                system_logs_folder = os.path.join(run_directory, "system_logs")
                player_number_search = re.search(r"_(\d+)p", run_directory)
                csv_path = os.path.join(system_logs_folder, "server.csv")
                
                if player_number_search:
                    player_number = int(player_number_search.group(1))
                else:
                    print(f"Invalid experiment directory: {run_directory}")
                    return
                
                df = pd.read_csv(csv_path, delimiter=";")
                avg_cpu = df['proc.cpu_percent'].mean()
                std_cpu = df['proc.cpu_percent'].std()
                
                search = re.search(r"players(.+)\/", run_directory)
                if search:
                    val = search.group(1)
                    if "-activeLogic" in val:
                        val = f"{val.replace('-activeLogic_', '')} (Logic Active)"
                    else: 
                        val = search.group(1).replace("_", "")     
                
                cpu_data.append((player_number, val, avg_cpu, std_cpu))
                
                player_numbers.add(player_number)

    cpu_df = pd.DataFrame(cpu_data, columns=['Player', 'Prototype', 'Average CPU Usage', 'Std Dev CPU'])
    plt.figure(figsize=(10, 6))

    bar_height = 0.1
    opacity = 1
    error_config = {'ecolor': '0.1'}
    colors = ['red', 'green', 'orange', 'blue', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    player_numbers_sorted = sorted(player_numbers)
    prototypes_sorted = sorted(cpu_df['Prototype'].unique())

    positions = np.arange(len(player_numbers_sorted))

    for i, prototype_folder in enumerate(prototypes_sorted):
        prototype_data = cpu_df[cpu_df['Prototype'] == prototype_folder]
        plt.bar(positions + bar_height * i, prototype_data['Average CPU Usage'] / 100, bar_height,
                alpha=opacity,
                color=colors[i],
                yerr=prototype_data['Std Dev CPU'] / 100,
                error_kw=error_config,
                label=prototype_folder)
        
    plt.xlabel('number of players')
    plt.ylabel('number of cores')
    plt.xticks(positions + bar_height * (len(prototypes_sorted) - 1) / 2, player_numbers_sorted)
    
    y_max = (cpu_df['Average CPU Usage'].max() // 100) + 1
    plt.yticks(np.arange(0, y_max, 1))

    plt.legend(frameon=False, loc='upper left', ncol=3)
    plt.legend(bbox_to_anchor=(0, 1, 1, 0.6), loc="lower left", mode="expand", ncol=3, frameon=False)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(f'{sc.plots_directory}/cpu_usage_per_player_barplot.pdf')


# def cpu_usage_per_client(experiment_directories):
#     player_numbers = set()
#     cpu_data = []

#     for experiment_directory in experiment_directories:
#         experiment_name= os.path.basename(os.path.abspath(experiment_directory))
#         for run in os.listdir(experiment_directory):
#             run_directory = os.path.join(experiment_directory, run)
#             if experiment_name in run and os.path.isdir(run_directory):  
#                 system_logs_folder = os.path.join(run_directory, "system_logs")
#                 player_number_search = re.search(r"_(\d+)p", run_directory)
#                 if player_number_search:
#                     player_number = int(player_number_search.group(1))
#                 else:
#                     print(f"Invalid experiment directory: {run_directory}")
#                     return
#                 search = re.search(r"players(.+)\/", run_directory)
#                 if search:
#                     val = search.group(1)
#                     if "-activeLogic" in val:
#                         val = f"{val.replace('-activeLogic_', '')} (Logic Active)"
#                     else: 
#                         val = search.group(1).replace("_", "")   
#                 for file in os.listdir(system_logs_folder):
#                     if file.endswith(".csv") and "client_node" in file:
#                         csv_path = os.path.join(system_logs_folder, file)
                        
#                         df = pd.read_csv(csv_path)

#                         avg_cpu = df['cpu_percent'].mean()
#                         std_cpu = df['cpu_percent'].std()

#                         cpu_data.append((player_number, val, avg_cpu, std_cpu))
#                         player_numbers.add(player_number)

#     cpu_df = pd.DataFrame(cpu_data, columns=['Player', 'Prototype', 'Average CPU Usage', 'Std Dev CPU'])

#     cpu_df.to_csv("temp.csv")
#     cpu_df = cpu_df.sort_values(by=['Player', 'Prototype'])
#     plt.figure(figsize=(10, 6))
#     bar_height = 0.7
#     opacity = 1
#     error_config = {'ecolor': '0.1'}
#     colors = ['red', 'green', 'orange', 'blue', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

#     player_numbers_sorted = sorted(player_numbers)
#     prototypes_sorted = sorted(cpu_df['Prototype'].unique())

#     positions = range(len(player_numbers_sorted))
    

#     for i, prototype_folder in enumerate(prototypes_sorted):
#         prototype_data = cpu_df[cpu_df['Prototype'] == prototype_folder]
#         plt.barh(positions, prototype_data['Average CPU Usage'], bar_height,
#                  alpha=opacity,
#                  color=colors[i % len(colors)],
#                  xerr=prototype_data['Std Dev CPU'],
#                  error_kw=error_config,
#                  label=prototype_folder)
        
#     plt.legend(frameon=False, ncol=3)
#     plt.ylabel('number of players')
#     plt.xlabel('average CPU usage [%]')
#     plt.yticks(positions, player_numbers_sorted)
#     plt.grid(axis='x')
#     plt.tight_layout()
#     plt.savefig(f'{sc.plots_directory}/cpu_usage_per_client_barplot.pdf')


def rss_ram_usage_plots(system_logs_folder):
    player_numbers = set()
    prototypes = []
    player_data = {}

    for prototype_folder in os.listdir(system_logs_folder):
        prototypes.append(prototype_folder)
        prototype_path = os.path.join(system_logs_folder, prototype_folder)
        
        for filename in os.listdir(prototype_path):
            if filename.endswith(".csv") and filename.startswith("system_log_"):
                parts = filename.split("_")
                player_number = int(parts[2][:-1])
                duration_seconds = int(parts[3][:-5])
                player_numbers.add(player_number)

    player_numbers = sorted(player_numbers)
    prototypes = sorted(prototypes)

    for prototype_folder in prototypes:
        prototype_path = os.path.join(system_logs_folder, prototype_folder)
        player_data[prototype_folder] = []

        for player_number in player_numbers:
            rss_values = []
            for filename in os.listdir(prototype_path):
                if filename.endswith(".csv") and filename.startswith("system_log_"):
                    parts = filename.split("_")
                    current_player_number = int(parts[2][:-1]) 
                    
                    if current_player_number == player_number:
                        csv_path = os.path.join(prototype_path, filename)
                        df = pd.read_csv(csv_path, delimiter=";")
                        df = df.tail(duration_seconds)
                        df.reset_index(drop=True, inplace=True) 
                        rss_values.extend(df['proc.memory_info.rss'])

            mean_rss_bytes = np.mean(rss_values)
            mean_rss_gb = mean_rss_bytes / (1024 ** 3)  # Convert bytes to gigabytes
            player_data[prototype_folder].append(mean_rss_gb)

            sem_bytes = np.std(rss_values) / np.sqrt(len(rss_values))
            sem_gb = sem_bytes / (1024 ** 3)  # Convert bytes to gigabytes
            player_data[prototype_folder].append(sem_gb)

    fig, ax = plt.subplots(figsize=(10, 7))
    bar_height = 0.3
    opacity = 1

    error_config = {'ecolor': '0.1'}

    colors = ['red', 'green', 'orange', 'blue', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

    for i, prototype_folder in enumerate(prototypes):
        positions = np.arange(len(player_numbers)) + bar_height * i
        ax.barh(positions, player_data[prototype_folder][::2], bar_height,
               alpha=opacity,
               color=colors[i],
               xerr=player_data[prototype_folder][1::2],
               error_kw=error_config,
               label=prototype_folder)

    ax.set_ylabel('number of players', fontsize=26)
    ax.set_xlabel('average memory usage [GB]', fontsize=26)
    ax.set_yticks(np.arange(len(player_numbers)) + bar_height * (len(prototypes) - 1) / 2)
    ax.set_yticklabels(player_numbers)
    plt.legend(bbox_to_anchor=(0, 1, 1, 0.6), loc="lower left", mode="expand", ncol=3, fontsize=20, frameon=False)
    plt.xticks(fontsize=26)
    plt.yticks(fontsize=26)
    ax.grid(axis='x')
    plt.tight_layout()
    plt.savefig(f'plots/rss_ram_usage.pdf')


cpu_usage_per_second(player_experiments)
# cpu_usage_per_player(player_experiments)
# cpu_usage_per_client(player_experiments)
# rss_ram_usage_plots(player_experiments)
