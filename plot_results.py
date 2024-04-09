import os
import csv
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-v0_8-colorblind')

def read_csv_files(folder):
    data = {}
    for filename in os.listdir(folder):
        if filename.endswith("_results.csv"):
            experiment_name = os.path.splitext(filename)[0].replace('_results', '')
            data[experiment_name] = {'Total_Players': [], 'RoundTripDelay_ms': []}
            with open(os.path.join(folder, filename), 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data[experiment_name]['Total_Players'].append(int(row['Total_Players']))
                    data[experiment_name]['RoundTripDelay_ms'].append(float(row['RoundTripDelay_ms']))
    return data

def plot_results(data, output_folder):
    plt.figure(figsize=(8, 6))
    for experiment_name, values in data.items():
        total_players = values['Total_Players']
        round_trip_delay = values['RoundTripDelay_ms']
        unique_players = sorted(set(total_players))
        avg_delay = [sum(round_trip_delay[i] for i, player_count in enumerate(total_players) if player_count == players) / total_players.count(players) for players in unique_players]
        line = plt.plot(unique_players, avg_delay, marker='o', label=experiment_name, markersize=8)[0]  # Change markersize to adjust the size of the shapes

        # Calculate error bars for standard deviation
        error = [np.std([round_trip_delay[i] for i, player_count in enumerate(total_players) if player_count == players]) for players in unique_players]

        # Plot error bars with the same color as the lines
        plt.errorbar(unique_players, avg_delay, yerr=error, fmt='none', ecolor=line.get_color(), capsize=5, elinewidth=2)  # Adjust elinewidth to make the lines thicker

    plt.xlabel('player count')
    plt.ylabel('average round trip delay (ms)')
    plt.title('experiment results')
    plt.legend(loc='upper left')
    plt.grid(True, axis='y') 
    plt.gca().yaxis.grid(True) 

    plt.xticks([0, 5, 10, 20, 40, 80, 120])  # Set the ticks on the x-axis

    os.makedirs(output_folder, exist_ok=True)
    
    # Save the plot as an image in the output folder
    plt.savefig(os.path.join(output_folder, "experiment_results.pdf"))
    


def main():
    folder = "."  # Change this to your folder containing the CSV files
    output_folder = "plots"  # Folder to save the plot image
    data = read_csv_files(folder)
    plot_results(data, output_folder)

if __name__ == "__main__":
    main()
