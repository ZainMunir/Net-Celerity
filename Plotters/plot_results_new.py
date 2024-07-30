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
    if "players" in x
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


        plt.legend(frameon=False, ncol=3)
        plt.title(f'{player_number} total players', fontsize=14)
        plt.grid(axis='y')
        plt.tight_layout()
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.savefig(f'{sc.plots_directory}cpu_usage_players_{player_number}.pdf')
        
        
cpu_usage_per_second(player_experiments)
