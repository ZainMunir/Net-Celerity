import os
import matplotlib.pyplot as plt
from collections import defaultdict

plt.style.use('seaborn-v0_8-colorblind')

def extract_var_csv(folder_path):
    csv_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('entities_results_210.csv'):
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

print(extract_var_csv('time_analysis'))

# ('mirror', 210, 26.015050820684355)
data = [('mirror', 150, 23.059733797866652), ('mirror', 30, 19.41311574689418), ('mirror', 5, 25.773749956061987), ('mirror', 60, 20.85262234652452), ('mirror', 120, 19.54594182451042), ('entities', 60, 1.854112620557412), ('mirror', 180, 24.42828712842906), ('entities', 150, 2.2530320338136622), ('entities', 5, 6.144624665252794), ('mirror', 90, 26.496122952786468), ('entities', 120, 2.582409636103802), ('entities', 180, 3.121041116714914), ('entities', 30, 4.3650943895019), ('entities', 90, 3.292065501278577)]
sorted_data = sorted(data, key=lambda x: x[1])

category_data = defaultdict(list)

for entry in sorted_data:
    category_data[entry[0]].append((entry[1], entry[2]))

plt.figure(figsize=(7, 5))

markers = ['o', 's', 'D', '^', 'v', 'p', 'P', '*', 'X', 'd', 'H', 'h', '<', '>', '8']
colors = ['g', 'b', 'r', 'c', 'm', 'y', 'k']
current_index = 0
for category, data_points in category_data.items():
    x_values = [x for x, _ in data_points]
    y_values = [y for _, y in data_points]    
    plt.plot(x_values, y_values, label=category, marker=markers[current_index], color=colors[current_index])
    current_index += 1

# set y-axis grid
plt.grid(axis='y')
plt.xlabel('Seconds')
plt.ylabel('Variance of RTT')
plt.title('Variance of RTT over Time')
plt.legend()

plt.xticks([0, 5, 30, 60, 90, 120, 150, 180])

if not os.path.exists('plots'):
    os.makedirs('plots')

plt.savefig('plots/variance_plot.pdf')
