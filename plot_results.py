import os
import csv
import matplotlib.pyplot as plt

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
        plt.plot(unique_players, avg_delay, marker='o', label=experiment_name)

        # Create box plots for each Total_Players value
        for players in unique_players:
            delays = [round_trip_delay[i] for i, player_count in enumerate(total_players) if player_count == players]
            # Plot box plot with red color and half transparency
            plt.boxplot(delays, positions=[players], widths=1, showfliers=False, patch_artist=False, boxprops=dict(color='red', alpha=0.5))
            # Plot line connecting means
            plt.plot(players, sum(delays) / len(delays), marker='_', markersize=10, color='blue')

    plt.xlabel('Total Players')
    plt.ylabel('Average Round Trip Delay (ms)')
    plt.title('Experiment Results')
    plt.legend(loc='upper left')
    plt.grid(True, axis='y')  # Only horizontal grid
    plt.gca().yaxis.grid(True)  # Force horizontal grid

    # Set x-axis limits with padding
    plt.xlim(-5, max(unique_players) + 5)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Save the plot as an image in the output folder
    plt.savefig(os.path.join(output_folder, "experiment_results.png"))


def main():
    folder = "."  # Change this to your folder containing the CSV files
    output_folder = "plots"  # Folder to save the plot image
    data = read_csv_files(folder)
    plot_results(data, output_folder)

if __name__ == "__main__":
    main()
