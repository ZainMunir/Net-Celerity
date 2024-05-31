import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from math import ceil

plt.style.use('seaborn-v0_8-colorblind')
sns.set_palette('colorblind')

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
    
    colors = ['red', 'green', 'orange', 'blue', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    for total_players, data in player_data.items():
        plt.figure(figsize=(6, 2))
        bp = plt.boxplot(data, vert=False, patch_artist=True, widths=0.7)  # Horizontal boxplots with different colors

        for box, color in zip(bp['boxes'], colors):
            box.set(facecolor=color)
            box_median = bp['medians'][bp['boxes'].index(box)]
            box_median.set(color='black')

        for outlier in bp['fliers']:
            outlier.set(marker='x', color='black', markersize=5, alpha=0.5)

        plt.xlabel('round trip delay [ms]',fontsize=14)
        plt.title(f'{total_players} total players', fontsize=14)
        plt.yticks(range(1, len(csv_files) + 1), [os.path.splitext(file)[0].replace('_results', '') for file in csv_files], fontsize=14)
        plt.xticks(fontsize=14)
        plt.grid(axis='x')
        plt.tight_layout()
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

        # plt.legend(bbox_to_anchor=(0,1.06,1,0.2), loc="lower left", mode="expand", ncol=3,fontsize=14,frameon=False)
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

    fig, ax = plt.subplots(figsize=(10, 4))
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

    ax.set_ylabel('total players', fontsize=14)
    ax.set_xlabel('mean RSS usage (GB)', fontsize=14)
    ax.set_yticks(np.arange(len(player_numbers)) + bar_height * (len(prototypes) - 1) / 2)
    ax.set_yticklabels(player_numbers)
    plt.legend(fontsize=14, frameon=False)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    ax.grid(axis='x')
    plt.tight_layout()
    plt.savefig(f'plots/rss_ram_usage.pdf')


def create_combined_boxplot_rtt(data_dir):
    # Collect all CSV files
    csv_files = [file for file in os.listdir(data_dir) if file.endswith('_results.csv')]
    all_data = []

    # Read data from each CSV and append to the list
    for csv_file in csv_files:
        experiment_name = os.path.splitext(csv_file)[0].replace('_results', '')
        df = pd.read_csv(os.path.join(data_dir, csv_file))
        df['Experiment'] = experiment_name
        all_data.append(df)
    
    # Concatenate all data into a single DataFrame
    combined_df = pd.concat(all_data)

    # Set up the plot
    plt.figure(figsize=(6, 4))
    sns.boxplot(
        x='Total_Players', 
        y='RoundTripDelay_ms', 
        hue='Experiment', 
        data=combined_df,
        palette=['red', 'green', 'orange'],
        showfliers=False
    )

    plt.xlabel('number of players', fontsize=14)
    plt.ylabel('round trip delay [ms]', fontsize=14)
    plt.xticks(ticks=[0, 1, 2, 3, 4, 5], labels=[5, 10, 20, 40, 60, 80], fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)
    plt.grid(axis='y')

    plt.tight_layout()
    plt.savefig('plots/rtt_combined_comparison.pdf')

def calculate_outliers(data):
    # Ensure the data is a pandas Series and numeric
    data = pd.Series(data)
    data = pd.to_numeric(data, errors='coerce').dropna()

    if len(data) == 0:
        return pd.Series([])  # Return an empty series if data is empty after conversion

    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return data[(data < lower_bound) | (data > upper_bound)]

def calculate_outliers(data):
    # Ensure the data is a pandas Series and numeric
    data = data.apply(lambda x: ceil(x))

    data = pd.Series(data)
    data = pd.to_numeric(data, errors='coerce').dropna()

    if len(data) == 0:
        return pd.Series([])  # Return an empty series if data is empty after conversion

    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return data[(data < lower_bound) | (data > upper_bound)]

def create_outliers_cdf_plot(data_dir):
    csv_files = [file for file in os.listdir(data_dir) if file.endswith('_results.csv')]
    all_outliers = []

    for csv_file in csv_files:
        experiment_name = os.path.splitext(csv_file)[0].replace('_results', '')
        file_path = os.path.join(data_dir, csv_file)
    
        df = pd.read_csv(file_path)
        
        grouped = df.groupby('Total_Players')
        for total_players, group in grouped:
            outliers = calculate_outliers(group['RoundTripDelay_ms'])
            if not outliers.empty:
                outliers_df = pd.DataFrame({'RoundTripDelay_ms': outliers, 'Prototype': experiment_name, 'Total_Players': total_players})
                all_outliers.append(outliers_df)
    
    if not all_outliers:
        print("No outliers found in any of the datasets.")
        return

    combined_outliers_df = pd.concat(all_outliers)

    

    sns.set_palette('colorblind')

    line_styles = ['-', '--', '-.', ':']
    line_width = 2.5

    # Set up the plot for each prototype
    for prototype in combined_outliers_df['Prototype'].unique():
        plt.figure(figsize=(7, 3))
        
        prototype_outliers = combined_outliers_df[combined_outliers_df['Prototype'] == prototype]
        for i, total_players in enumerate(prototype_outliers['Total_Players'].unique()):
            player_outliers = prototype_outliers[prototype_outliers['Total_Players'] == total_players]['RoundTripDelay_ms']
            sns.ecdfplot(player_outliers, label=f'{total_players} players', linestyle=line_styles[i % len(line_styles)], linewidth=line_width)
        
        plt.xlabel('round trip delay [ms]', fontsize=14)
        plt.ylabel('probability density', fontsize=14)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.legend(fontsize=14)
        plt.grid(True)

        plt.tight_layout()
        plt.savefig(f'plots/rtt_outliers_cdf_comparison_{prototype}.pdf')


# rss_ram_usage_plots("system_logs")
# cpu_usage_per_second("./system_logs_workload1")
# create_boxplots_rtt('./workload2_results')
# total_sent("system_logs")
# total_recv("system_logs")
create_outliers_cdf_plot('./workload2_results')
create_combined_boxplot_rtt('./workload2_results')