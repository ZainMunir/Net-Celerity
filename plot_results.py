import os
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('seaborn-v0_8-colorblind')

# Printing box plots
def create_boxplots_rtt(data_dir):
    csv_files = [file for file in os.listdir(data_dir) if file.endswith('_results.csv')]
    player_data = {}


    for csv_file in csv_files:
        experiment_name = os.path.splitext(csv_file)[0].replace('_results', '')
        df = pd.read_csv(os.path.join(data_dir, csv_file))

        grouped = df.groupby('Total_Players')

        for total_players, group in grouped:
            if total_players not in player_data:
                player_data[total_players] = []

            player_data[total_players].append(group['RoundTripDelay_ms'].values)

    colors = ['red', 'green', 'orange', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    for total_players, data in player_data.items():
        plt.figure(figsize=(6, 2))
        bp = plt.boxplot(data, vert=False, patch_artist=True, widths=0.7)  # Horizontal boxplots with different colors

        for box, color in zip(bp['boxes'], colors):
            box.set(facecolor=color)
            box_median = bp['medians'][bp['boxes'].index(box)]
            box_median.set(color='black')

        for outlier in bp['fliers']:
            outlier.set(marker='x', color='black', markersize=5, alpha=0.5)

        plt.xlabel('round trip delay (ms)',fontsize=14)
        plt.title(f'{total_players} total players', fontsize=14)
        plt.yticks(range(1, len(csv_files) + 1), [os.path.splitext(file)[0].replace('_results', '') for file in csv_files], fontsize=14)
        plt.xticks(fontsize=14)
        plt.grid(axis='x')
        plt.tight_layout()
        plt.show()
        plt.savefig(f'plots/rtt_comparison_{total_players}.pdf')

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
                total_mb_sent = (bytes_sent_total.iloc[-1] - bytes_sent_total.iloc[0]) / (1024 * 1024)
                player_data[player_number] = total_mb_sent

        
        prototype_data[prototype_folder] = player_data

    plt.figure(figsize=(6, 5))

    markers = ['o', 's', 'D', 'x', '+', 'v', '^', '<', '>', 'h', 'H', 'd', '|', '_']
    colors = ['red', 'green', 'orange', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    marker_index = 0
    for prototype, player_data in prototype_data.items():
        player_numbers = sorted(player_data.keys())
        total_bytes_sent = [player_data[player_number] for player_number in player_numbers]
        
        plt.plot(player_numbers, total_bytes_sent, marker=markers[marker_index], color=colors[marker_index] , label=f"{prototype}", alpha=0.9, linewidth = 2)
        marker_index += 1

    my_ticks.sort()

    plt.xticks(my_ticks, fontsize=14)
    plt.yticks(fontsize=14)

    plt.xlabel("total players",fontsize=14)
    plt.ylabel("total sent (MB)",fontsize=14)
    plt.legend(fontsize=14, frameon=False)
    plt.grid(axis='y')
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
                total_mb_recv = (bytes_recv_total.iloc[-1] - bytes_recv_total.iloc[0]) / (1024 * 1024)
                player_data[player_number] = total_mb_recv

        
        prototype_data[prototype_folder] = player_data

    plt.figure(figsize=(6, 5))

    markers = ['o', 's', 'D', 'x', '+', 'v', '^', '<', '>', 'h', 'H', 'd', '|', '_']
    colors = ['red', 'green', 'orange', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

    marker_index = 0
    for prototype, player_data in prototype_data.items():
        player_numbers = sorted(player_data.keys())
        total_bytes_sent = [player_data[player_number] for player_number in player_numbers]
        
        plt.plot(player_numbers, total_bytes_sent, marker=markers[marker_index], color=colors[marker_index], label=f"{prototype}", alpha=0.9, linewidth = 2)
        marker_index += 1

    my_ticks.sort()

    plt.xticks(my_ticks, fontsize=14)
    plt.yticks(fontsize=14)

    plt.xlabel("total players",fontsize=14)
    plt.ylabel("total recieved (MB)",fontsize=14)
    plt.legend(fontsize=14, frameon=False)
    plt.grid(axis='y')
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
        plt.figure(figsize=(7, 4))
        plt.title(f'{player_number} total players', fontsize=14)
        plt.xlabel("time (s)", fontsize=14)
        plt.ylabel("CPU usage (%)", fontsize=14)
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

        plt.legend(bbox_to_anchor=(0,1.06,1,0.2), loc="lower left", mode="expand", ncol=3,fontsize=14,frameon=False)
        plt.grid(axis='y')
        plt.tight_layout()
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.savefig(f'plots/cpu_usage_players_{player_number}.pdf')




# cpu_usage_per_second("system_logs")
# create_boxplots_rtt('.')
# total_sent("system_logs")
# total_recv("system_logs")
