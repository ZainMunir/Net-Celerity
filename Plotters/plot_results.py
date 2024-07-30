import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
from math import ceil

plt.style.use('seaborn-v0_8-colorblind')
sns.set_palette('colorblind')

def total_sent(system_logs_folder):
    prototype_data = {}
    my_ticks = []

    for prototype_folder in os.listdir(system_logs_folder):
        prototype_path = os.path.join(system_logs_folder, prototype_folder)

        player_data = {}

        for filename in os.listdir(prototype_path):
            if filename.endswith(".csv") and filename.startswith("system_log_"):
                parts = filename.split("_")
                player_number = int(parts[2][:-1])
                duration_seconds = int(parts[3][:-5])

                if player_number not in my_ticks:
                    my_ticks.append(player_number)

                csv_path = os.path.join(prototype_path, filename)
                df = pd.read_csv(csv_path, delimiter=";")
                df = df.tail(duration_seconds)

                bytes_sent_total = df[[col for col in df.columns if col.startswith('net.bytes_sent')]].sum(axis=1)
                mb_per_sec_sent = np.diff(bytes_sent_total) / (1024 * 1024)  # Calculate MB/s differences

                if player_number in player_data:
                    player_data[player_number].extend(mb_per_sec_sent)
                else:
                    player_data[player_number] = mb_per_sec_sent.tolist()

        prototype_data[prototype_folder] = player_data

    plt.figure(figsize=(7, 5))

    markers = ['o', 's', 'D', 'x', '+', 'v', '^', '<', '>', 'h', 'H', 'd', '|', '_']
    colors = ['red', 'green', 'orange', 'blue', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    line_styles = ['-', '--', '-.', ':']  # Different line styles
    marker_index = 0
    line_style_index = 0

    for prototype, player_data in prototype_data.items():
        player_numbers = sorted(player_data.keys())
        mean_mb_per_sec_sent = [np.mean(player_data[player_number]) for player_number in player_numbers]
        std_mb_per_sec_sent = [np.std(player_data[player_number]) for player_number in player_numbers]

        plt.errorbar(player_numbers, mean_mb_per_sec_sent, yerr=std_mb_per_sec_sent, fmt=markers[marker_index],
                     color=colors[marker_index], label=f"{prototype}", alpha=0.9, linewidth=2,
                     linestyle=line_styles[line_style_index])
        
        marker_index += 1
        line_style_index = (line_style_index + 1) % len(line_styles)

    my_ticks.sort()

    plt.xticks(my_ticks, fontsize=20)
    plt.yticks(fontsize=20)

    plt.xlabel("Number of Players", fontsize=20)
    plt.ylabel("Data Transfer Rate [MB/s]", fontsize=20)
    plt.legend(bbox_to_anchor=(0, 1, 1, 0.6), loc="lower left", mode="expand", ncol=3, fontsize=20, frameon=False)

    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig('plots/total_bytes_sent_vs_players.pdf')

def total_recv(system_logs_folder):
    prototype_data = {}
    my_ticks = []

    for prototype_folder in os.listdir(system_logs_folder):
        prototype_path = os.path.join(system_logs_folder, prototype_folder)

        player_data = {}

        for filename in os.listdir(prototype_path):
            if filename.endswith(".csv") and filename.startswith("system_log_"):
                parts = filename.split("_")
                player_number = int(parts[2][:-1])
                duration_seconds = int(parts[3][:-5])

                if player_number not in my_ticks:
                    my_ticks.append(player_number)

                csv_path = os.path.join(prototype_path, filename)
                df = pd.read_csv(csv_path, delimiter=";")
                df = df.tail(duration_seconds)

                bytes_recv_total = df[[col for col in df.columns if col.startswith('net.bytes_recv')]].sum(axis=1)
                mb_per_sec_recv = np.diff(bytes_recv_total) / (1024 * 1024)  # Calculate MB/s differences

                if player_number in player_data:
                    player_data[player_number].extend(mb_per_sec_recv)
                else:
                    player_data[player_number] = mb_per_sec_recv.tolist()

        prototype_data[prototype_folder] = player_data

    plt.figure(figsize=(7, 5))

    markers = ['o', 's', 'D', 'x', '+', 'v', '^', '<', '>', 'h', 'H', 'd', '|', '_']
    colors = ['red', 'green', 'orange', 'blue', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    line_styles = ['-', '--', '-.', ':']  # Different line styles
    marker_index = 0
    line_style_index = 0

    for prototype, player_data in prototype_data.items():
        player_numbers = sorted(player_data.keys())
        mean_mb_per_sec_recv = [np.mean(player_data[player_number]) for player_number in player_numbers]
        std_mb_per_sec_recv = [np.std(player_data[player_number]) for player_number in player_numbers]

        plt.errorbar(player_numbers, mean_mb_per_sec_recv, yerr=std_mb_per_sec_recv, fmt=markers[marker_index],
                     color=colors[marker_index], label=f"{prototype}", alpha=0.9, linewidth=2,
                     linestyle=line_styles[line_style_index])

        marker_index += 1
        line_style_index = (line_style_index + 1) % len(line_styles)

    my_ticks.sort()

    plt.xticks(my_ticks, fontsize=20)
    plt.yticks(fontsize=20)

    plt.xlabel("Number of Players", fontsize=20)
    plt.ylabel("Data Received Rate [MB/s]", fontsize=20)
    plt.legend(bbox_to_anchor=(0, 1, 1, 0.6), loc="lower left", mode="expand", ncol=3, fontsize=20, frameon=False)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig('plots/total_bytes_recv_vs_players.pdf')

def cpu_usage_per_second(system_logs_folder):
    player_numbers = set() 

    for prototype_folder in os.listdir(system_logs_folder):
        prototype_path = os.path.join(system_logs_folder, prototype_folder)
        
        for filename in os.listdir(prototype_path):
            if filename.endswith(".csv") and filename.startswith("system_log_"):
                parts = filename.split("_")
                player_number = int(parts[2][:-1]) 
                duration_seconds = int(parts[3][:-5]) 
                
                csv_path = os.path.join(prototype_path, filename)
                df = pd.read_csv(csv_path, delimiter=";")
                df = df.tail(duration_seconds)
                player_numbers.add(player_number)

    for player_number in sorted(player_numbers):
        plt.figure(figsize=(5, 3))
        plt.title(f'{player_number} total players', fontsize=14)
        plt.xlabel("time [s]", fontsize=14)
        plt.ylabel("CPU usage [%]", fontsize=14)
        colors = ['red', 'green', 'orange', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
        color_index = 0

        for prototype_folder in os.listdir(system_logs_folder):
            prototype_path = os.path.join(system_logs_folder, prototype_folder)
            
            for filename in os.listdir(prototype_path):
                if filename.endswith(".csv") and filename.startswith("system_log_"):
                    parts = filename.split("_")
                    current_player_number = int(parts[2][:-1]) 
                    
                    if current_player_number == player_number:
                        csv_path = os.path.join(prototype_path, filename)
                        df = pd.read_csv(csv_path, delimiter=";")
                        df = df.tail(duration_seconds)
                        df.reset_index(drop=True, inplace=True) 
                        
                        plt.plot(df.index, df['proc.cpu_percent'], label=f"{prototype_folder}", linewidth=2, color=colors[color_index], alpha=0.8)
                        color_index += 1


        plt.legend(frameon=False, ncol=3)
        plt.title(f'{player_number} total players', fontsize=14)
        plt.grid(axis='y')
        plt.tight_layout()
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.savefig(f'plots/cpu_usage_players_{player_number}.pdf')

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

def cpu_usage_per_player(system_logs_folder):
    player_numbers = set()
    cpu_data = []

    for prototype_folder in os.listdir(system_logs_folder):
        prototype_path = os.path.join(system_logs_folder, prototype_folder)
        
        for filename in os.listdir(prototype_path):
            if filename.endswith(".csv") and filename.startswith("system_log_"):
                parts = filename.split("_")
                player_number = int(parts[2][:-1]) 
                
                csv_path = os.path.join(prototype_path, filename)
                df = pd.read_csv(csv_path, delimiter=";")
                avg_cpu = df['proc.cpu_percent'].mean()
                std_cpu = df['proc.cpu_percent'].std()
                cpu_data.append((player_number, prototype_folder, avg_cpu, std_cpu))

                player_numbers.add(player_number)

    cpu_df = pd.DataFrame(cpu_data, columns=['Player', 'Prototype', 'Average CPU Usage', 'Std Dev CPU'])
    plt.figure(figsize=(7, 4))

    bar_height = 0.3
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
        
    plt.xlabel('number of players', fontsize=17)
    plt.ylabel('number of cores', fontsize=17)
    plt.xticks(positions + bar_height * (len(prototypes_sorted) - 1) / 2, player_numbers_sorted, fontsize = 17)
    
    y_max = (cpu_df['Average CPU Usage'].max() // 100) + 1
    plt.yticks(np.arange(0, 6, 1), fontsize = 17)

    plt.legend(frameon=False, fontsize=17, loc='upper left', ncol=3)
    plt.legend(bbox_to_anchor=(0, 1, 1, 0.6), loc="lower left", mode="expand", ncol=3, fontsize=20, frameon=False)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(f'plots/cpu_usage_per_player_barplot.pdf')

def cpu_usage_per_client(system_logs_folder):
    player_numbers = set()
    cpu_data = []

    for prototype_folder in os.listdir(system_logs_folder):
        prototype_path = os.path.join(system_logs_folder, prototype_folder)
        
        for filename in os.listdir(prototype_path):
            if filename.endswith(".csv") and "client_node" in filename:
                csv_path = os.path.join(prototype_path, filename)
                df = pd.read_csv(csv_path)

                avg_cpu = df['cpu_percent'].mean()
                std_cpu = df['cpu_percent'].std()

                parts = filename.split("_")
                player_number = int(parts[2][:-1])

                cpu_data.append((player_number, prototype_folder, avg_cpu, std_cpu))
                player_numbers.add(player_number)

    cpu_df = pd.DataFrame(cpu_data, columns=['Player', 'Prototype', 'Average CPU Usage', 'Std Dev CPU'])

    cpu_df = cpu_df.sort_values(by='Player')
    plt.figure(figsize=(5, 4))
    bar_height = 0.7
    opacity = 1
    error_config = {'ecolor': '0.1'}
    colors = ['red', 'green', 'orange', 'blue', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

    player_numbers_sorted = sorted(player_numbers)
    prototypes_sorted = sorted(cpu_df['Prototype'].unique())

    positions = range(len(player_numbers_sorted))

    for i, prototype_folder in enumerate(prototypes_sorted):
        prototype_data = cpu_df[cpu_df['Prototype'] == prototype_folder]
        plt.barh(positions, prototype_data['Average CPU Usage'], bar_height,
                 alpha=opacity,
                 color=colors[i % len(colors)],
                 xerr=prototype_data['Std Dev CPU'],
                 error_kw=error_config,
                 label=prototype_folder)
        
    plt.legend(frameon=False, ncol=3)
    plt.ylabel('number of players', fontsize=16)
    plt.xlabel('average CPU usage [%]', fontsize=16)
    plt.yticks(positions, player_numbers_sorted, fontsize=16)
    plt.xticks(fontsize=16)
    plt.grid(axis='x')
    plt.tight_layout()
    plt.savefig('plots/cpu_usage_per_client_barplot.pdf')

def rss_ram_usage_per_client(system_logs_folder, total_ram):
    player_numbers = set()
    prototypes = []
    player_data = {}

    for prototype_folder in os.listdir(system_logs_folder):
        prototypes.append(prototype_folder)
        prototype_path = os.path.join(system_logs_folder, prototype_folder)
        
        for filename in os.listdir(prototype_path):
            if filename.endswith(".csv") and "client_node" in filename:
                parts = filename.split("_")
                player_number = int(parts[2][:-1])
                player_numbers.add(player_number)

    player_numbers = sorted(player_numbers)
    prototypes = sorted(prototypes)

    for prototype_folder in prototypes:
        prototype_path = os.path.join(system_logs_folder, prototype_folder)
        player_data[prototype_folder] = []

        for player_number in player_numbers:
            rss_values = []
            for filename in os.listdir(prototype_path):
                if filename.endswith(".csv") and "client_node" in filename:
                    parts = filename.split("_")
                    current_player_number = int(parts[2][:-1]) 
                    
                    if current_player_number == player_number:
                        csv_path = os.path.join(prototype_path, filename)
                        df = pd.read_csv(csv_path)
                        rss_values.extend(df['rss'])

            mean_rss_bytes = np.mean(rss_values)
            mean_rss_percentage = (mean_rss_bytes / total_ram) * 100  # Convert to percentage of total RAM
            player_data[prototype_folder].append(mean_rss_percentage)

            sem_bytes = np.std(rss_values) / np.sqrt(len(rss_values))
            sem_percentage = (sem_bytes / total_ram) * 100  # Convert to percentage of total RAM
            player_data[prototype_folder].append(sem_percentage)

    fig, ax = plt.subplots(figsize=(5, 4))
    bar_height = 0.7
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

    ax.set_ylabel('number of players', fontsize=16)
    ax.set_xlabel('average memory usage [%]', fontsize=16)
    ax.set_yticks(np.arange(len(player_numbers)) + bar_height * (len(prototypes) - 1) / 2)
    ax.set_yticklabels(player_numbers)
    plt.legend(frameon=False, ncol=3)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    ax.grid(axis='x')
    plt.tight_layout()
    plt.savefig('plots/rss_ram_usage_per_client_percentage.pdf')


log_folder = "system_logs"

cpu_usage_per_player(log_folder)
cpu_usage_per_client(log_folder)
rss_ram_usage_plots(log_folder)
cpu_usage_per_second(log_folder)
total_sent(log_folder)
total_recv(log_folder)
rss_ram_usage_per_client(log_folder, 135017807872)

