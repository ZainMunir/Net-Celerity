import os
import csv
import sys

def get_last_player_id(csv_file):
    if not os.path.exists(csv_file):
        return 0  # Return 0 if file doesn't exist
    else:
        with open(csv_file, mode="r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            last_row = None
            for row in reader:
                last_row = row
            if last_row is None:
                return 0  # Return 0 if file is empty
            return int(last_row["Player_ID"])

def create_csv(logs_folder):
    log_files = [f for f in os.listdir(logs_folder) if os.path.isfile(os.path.join(logs_folder, f))]
    
    log_files.sort()
    total_players = len(log_files) - 1
    
    csv_file = "mirror_results.csv"
    last_player_id = get_last_player_id(csv_file)
    
    with open(csv_file, mode="a", newline="") as csvfile:  # Open file in append mode
        fieldnames = ["Player_ID", "Total_Players", "RoundTripDelay_ms"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if os.stat(csv_file).st_size == 0:  # Check if file is empty
            writer.writeheader()  # Write header if file is empty
        
        for log_file in log_files:
            if log_file.startswith("player_log"):
                with open(os.path.join(logs_folder, log_file), mode="r") as file:
                    next(file)
                    
                    player_id = last_player_id + 1  # Start new player ID from the next number
                    
                    for line in file:
                        data = line.strip().split(",")
                        
                        writer.writerow({
                            "Player_ID": player_id,
                            "Total_Players": total_players,
                            "RoundTripDelay_ms": data[-1] 
                        })
            
                last_player_id = player_id  # Update last player ID for the next player

def main(logs_folder):
    create_csv(logs_folder)
    print("Script execution completed.")  # Print message indicating script completion

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <logs_folder>")
        sys.exit(1)
    logs_folder = sys.argv[1]
    main(logs_folder)
