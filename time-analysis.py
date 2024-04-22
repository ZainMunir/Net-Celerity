import os
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-colorblind')

def extract_var_csv(folder_path):
    csv_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.csv'):
                # extract substring of file name before the first underscore
                # e.g. "time_analysis/mirror_results_30.csv" -> "mirror"
                prototype = file.split('_')[0]
                # now extract the number of seconds from the file
                # e.g. "time_analysis/mirror_results_30.csv" -> 30
                seconds = int(file.split('_')[2].split('.')[0])
                # open the csv file that look like this inside "Player_ID,Total_Players,RoundTripDelay_ms\n1,10,15\n1,10,15\n1,10,15\n..." and calculate variance of the RoundTripDelay_ms column
                with open(os.path.join(root, file), 'r') as csv_file:
                    round_trip_delays = []
                    for line in csv_file:
                        if line.startswith('Player_ID'):
                            continue
                        round_trip_delays.append(float(line.strip().split(',')[2]))
                    variance = sum((x - sum(round_trip_delays) / len(round_trip_delays)) ** 2 for x in round_trip_delays) / len(round_trip_delays)
                    print(prototype, seconds, variance)
                    csv_files.append((prototype, seconds, variance))

    return csv_files

experiments = extract_var_csv("time_analysis")
print(experiments)
