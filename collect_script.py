import os
import csv
import sys

results_file = "/var/scratch/zmr280/entities_results.csv" #"entities_results.csv" 

def get_last_player_id(csv_file):
    if not os.path.exists(csv_file):
        return 0  # Return 0 if file doesn't exist
    else:
        with open(csv_file, mode="r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            last_player_id = 0
            for row in reader:
                last_player_id = int(row["Player_ID"])
            return last_player_id

def count_player_logs(logs_folder):
    count = 0
    for filename in os.listdir(logs_folder):
        if filename.startswith("player_log") and filename.endswith(".csv"):
            count += 1
    return count

def extract_player_logs(logs_folder, total_players, last_player_id):
    player_logs = []
    player_id = last_player_id + 1
    for filename in os.listdir(logs_folder):
        if filename.startswith("player_log") and filename.endswith(".csv"):
            with open(os.path.join(logs_folder, filename), mode="r") as file:
                reader = csv.DictReader(file, delimiter=";")
                next(reader)  # Skip header
                for row in reader:
                    if int(row["Number of Players (Client)"]) >= total_players and int(row["Frame Number"]) > 1:
                        player_logs.append([player_id, total_players, row["NFE RTT"]])
            player_id += 1
    return player_logs


def save_results(player_logs):
    file_exists = os.path.exists(results_file)
    with open(results_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:  # Write header only if file is empty
            writer.writerow(["Player_ID", "Total_Players", "RoundTripDelay_ms"])
        for log in player_logs:
            writer.writerow(log)

def main(logs_folder):
    total_players = count_player_logs(logs_folder)
    last_player_id = get_last_player_id(results_file)
    player_logs = extract_player_logs(logs_folder, total_players, last_player_id)
    save_results(player_logs)
    print("Script execution completed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <logs_folder>")
        sys.exit(1)
    logs_folder = sys.argv[1]
    main(logs_folder)
