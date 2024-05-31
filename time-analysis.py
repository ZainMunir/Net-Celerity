import os
import matplotlib.pyplot as plt
from collections import defaultdict

plt.style.use('seaborn-v0_8-colorblind')

def extract_var_csv(folder_path):
    csv_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('mirrorTelepathy_results_420.csv'):
                prototype = file.split('_')[0]
                seconds = int(file.split('_')[2].split('.')[0])

                with open(os.path.join(root, file), 'r') as csv_file:
                    round_trip_delays = []
                    for line in csv_file:
                        if line.startswith('Player_ID'):
                            continue
                        round_trip_delays.append(float(line.strip().split(',')[2]))
                    variance = sum((x - sum(round_trip_delays) / len(round_trip_delays)) ** 2 for x in round_trip_delays) / len(round_trip_delays)
                    csv_files.append((prototype, seconds, variance))

    return csv_files

data = [('mirrorTelepathy', 420, 36.48168895725908),('mirrorTelepathy', 390, 38.432580244694925), ('mirrorTelepathy', 360, 19.61400659312184), ('mirrorTelepathy', 330, 27.385573279756102), ('mirrorTelepathy', 300, 31.199244309183964), ('mirrorTelepathy', 270, 8.985656426445209), ('mirrorTelepathy', 240, 17.447610396295364), ('mirrorTelepathy', 210, 30.183195278196145), ('mirrorTelepathy', 180, 15.873806006125658), ('mirrorTelepathy', 150, 11.419250185575002), ('mirrorTelepathy', 120, 20.2018314046651), ('mirrorTelepathy', 90, 26.937288423081238), ('mirrorTelepathy', 60, 47.66263981263731),('mirrorTelepathy', 30, 26.347890817833605), ('mirrorTelepathy', 5, 21.38757258774539), ('mirrorKCP', 420, 28.16841010949316), ('entities', 420, 2.0514378952505137), ('mirrorKCP', 390, 27.88917162982882), ('entities', 390, 2.767924758625096), ('entities', 360, 2.3936186621560704), ('mirrorKCP', 360, 23.529665750464645), ('entities', 330, 2.946337365386775), ('mirrorKCP', 330, 26.01320123210872), ('entities', 300, 2.1961736552229403), ('mirrorKCP', 300, 23.498996340916346), ('entities', 270, 2.0857472677203184), ('mirrorKCP', 270, 25.47688914525538), ('entities', 240, 2.248842759005533), ('mirrorKCP', 240, 27.155120483658706), ('entities', 210, 2.2380403169105634), ('mirrorKCP', 210, 26.015050820684355), ('mirrorKCP', 150, 23.059733797866652), ('mirrorKCP', 30, 19.41311574689418), ('mirrorKCP', 5, 25.773749956061987), ('mirrorKCP', 60, 20.85262234652452), ('mirrorKCP', 120, 19.54594182451042), ('entities', 60, 1.854112620557412), ('mirrorKCP', 180, 24.42828712842906), ('entities', 150, 2.2530320338136622), ('entities', 5, 6.144624665252794), ('mirrorKCP', 90, 26.496122952786468), ('entities', 120, 2.582409636103802), ('entities', 180, 3.121041116714914), ('entities', 30, 4.3650943895019), ('entities', 90, 3.292065501278577)]
sorted_data = sorted(data, key=lambda x: x[1])

x_ticks = []
for x in sorted_data:
    if x[1] % 60 == 0:  # Check if the value is a multiple of 60 (representing minutes)
        x_ticks.append(x[1] // 60)  # Append the value in minutes

category_data = defaultdict(list)

for entry in sorted_data:
    category_data[entry[0]].append((entry[1], entry[2]))

fig, ax = plt.subplots(figsize=(14, 4))

markers = ['D', 's', 'o', '^', 'v', 'p', 'P', '*', 'X', 'd', 'H', 'h', '<', '>', '8']
colors = ['orange', 'g', 'r', 'c', 'm', 'y', 'k']
current_index = 0

for category, data_points in category_data.items():
    x_values = [x/60 for x, _ in data_points]  # Converting seconds to minutes
    y_values = [y for _, y in data_points]    
    ax.plot(x_values, y_values, label=category, marker=markers[current_index], color=colors[current_index])
    current_index += 1

ax.grid(axis='both')
ax.set_xlabel('time [minutes]', fontsize=14)  # Updating xlabel
ax.set_ylabel('variance of RTT [ms$^2$]', fontsize=14)  # Updating ylabel with LaTeX
ax.set_xticks(x_ticks)  # Using only integer values for x-axis
ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=14)
plt.legend(bbox_to_anchor=(0,1.02,0.6,0.2), loc="lower left", mode="expand", ncol=3,fontsize=14,frameon=False)

plt.tight_layout()

if not os.path.exists('plots'):
    os.makedirs('plots')
plt.savefig('plots/variance_plot.pdf')
