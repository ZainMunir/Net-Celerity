import os
import matplotlib.pyplot as plt
from collections import defaultdict

plt.style.use('seaborn-v0_8-colorblind')

def extract_var_csv(folder_path):
    csv_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('M-TP_results_420.csv'):
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

data = [('M-TP', 420, 36.48168895725908),('M-TP', 390, 38.432580244694925), ('M-TP', 360, 19.61400659312184), ('M-TP', 330, 27.385573279756102), ('M-TP', 300, 31.199244309183964), ('M-TP', 270, 8.985656426445209), ('M-TP', 240, 17.447610396295364), ('M-TP', 210, 30.183195278196145), ('M-TP', 180, 15.873806006125658), ('M-TP', 150, 11.419250185575002), ('M-TP', 120, 20.2018314046651), ('M-TP', 90, 26.937288423081238), ('M-TP', 60, 47.66263981263731),('M-TP', 30, 26.347890817833605), ('M-TP', 5, 21.38757258774539), ('M-KCP', 420, 28.16841010949316), ('DOTS-NFE', 420, 2.0514378952505137), ('M-KCP', 390, 27.88917162982882), ('DOTS-NFE', 390, 2.767924758625096), ('DOTS-NFE', 360, 2.3936186621560704), ('M-KCP', 360, 23.529665750464645), ('DOTS-NFE', 330, 2.946337365386775), ('M-KCP', 330, 26.01320123210872), ('DOTS-NFE', 300, 2.1961736552229403), ('M-KCP', 300, 23.498996340916346), ('DOTS-NFE', 270, 2.0857472677203184), ('M-KCP', 270, 25.47688914525538), ('DOTS-NFE', 240, 2.248842759005533), ('M-KCP', 240, 27.155120483658706), ('DOTS-NFE', 210, 2.2380403169105634), ('M-KCP', 210, 26.015050820684355), ('M-KCP', 150, 23.059733797866652), ('M-KCP', 30, 19.41311574689418), ('M-KCP', 5, 25.773749956061987), ('M-KCP', 60, 20.85262234652452), ('M-KCP', 120, 19.54594182451042), ('DOTS-NFE', 60, 1.854112620557412), ('M-KCP', 180, 24.42828712842906), ('DOTS-NFE', 150, 2.2530320338136622), ('DOTS-NFE', 5, 6.144624665252794), ('M-KCP', 90, 26.496122952786468), ('DOTS-NFE', 120, 2.582409636103802), ('DOTS-NFE', 180, 3.121041116714914), ('DOTS-NFE', 30, 4.3650943895019), ('DOTS-NFE', 90, 3.292065501278577)]
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
ax.set_xlabel('time [m]', fontsize=22)  # Updating xlabel
ax.set_ylabel('variance of RTT [ms$^2$]', fontsize=22)  # Updating ylabel with LaTeX
ax.set_xticks(x_ticks)  # Using only integer values for x-axis
ax.tick_params(axis='x', labelsize=22)
ax.tick_params(axis='y', labelsize=22)
plt.legend(bbox_to_anchor=(0,1.02,0.8,0.2), loc="lower left", mode="expand", ncol=3,fontsize=22,frameon=False)

plt.tight_layout()

if not os.path.exists('plots'):
    os.makedirs('plots')
plt.savefig('plots/variance_plot.pdf')
