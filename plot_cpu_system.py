import os
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-colorblind')
def extract_subfolders(folder_path):
    subfolders = [folder for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]
    return subfolders

def extract_log_files(folder_path):
    log_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.log'):
                log_files.append(os.path.join(root, file))
    return log_files

def parse_log_file(file_path):
    values = []
    with open(file_path, 'r') as file:
        for line in file:
            metrics = line.strip().split('\t')[1:]
            for metric in metrics:
                if metric.startswith('proc.cpu.user='):
                    # Convert bytes to megabytes
                    values.append(float(metric.split('=')[1]))
    return sum(values)/len(values)/10

prototypes = extract_subfolders("system_logs")

log_files_dict = {}

for prototype in prototypes:
    log_files = extract_log_files(f"system_logs/{prototype}")
    for log_file in log_files:
        log_files_dict[log_file] = parse_log_file(log_file)

logs = {}

for key, value in log_files_dict.items():
    parts = key.split('/')
    prototype = parts[1]
    log_num = int(parts[2].split('.')[0].split('_')[-1])
    if log_num not in logs:
        logs[log_num] = {}
    logs[log_num][prototype] = value

log_numbers = sorted(logs.keys())
prototype_values = {prototype: [logs[num][prototype] for num in log_numbers] for prototype in prototypes}

plt.figure(figsize=(10, 8))
bar_width = 0.8 / len(prototypes)
index = range(len(log_numbers))

colors = {'mirror': 'green', 'entities': 'blue'}

for i, prototype in enumerate(prototypes):
    plt.bar([idx + i * bar_width for idx in index], prototype_values[prototype], bar_width, label=prototype, color=colors.get(prototype, 'black'))

plt.xlabel('player count')
plt.ylabel('CPU usage (%)')
plt.title('comparison of CPU usage for each prototype vs. player count')
my_xticks = [5,10,20,40,80,120]
plt.xticks([idx + len(log_files_dict)/len(my_xticks)/10 for idx in index], my_xticks)
plt.legend()

plt.savefig('plots/cpu_comparison.pdf')