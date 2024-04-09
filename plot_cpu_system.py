import os
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-colorblind')

def parse_log_file(file_path):
    cpu_usage = []
    with open(file_path, 'r') as file:
        for line in file:
            metrics = line.strip().split('\t')[1:]
            for metric in metrics:
                if metric.startswith('proc.cpu.user='):
                    cpu_usage.append(float(metric.split('=')[1]))
    return cpu_usage

def process_logs(folder_path):
    experiments = {}
    frameworks = ['entities', 'mirror']
    for framework in frameworks:
        experiments[framework] = {}
        for i in range(1, 7):
            log_file = os.path.join(folder_path, framework, f'system_log_{i}.log')
            experiments[framework][f'exp_{i}'] = parse_log_file(log_file)
    return experiments

def plot_mean_cpu_usage(experiments):
    durations = [5, 10, 20, 40, 80, 120]
    entities_means = []
    mirror_means = []

    for duration in durations:
        entities_data = []
        mirror_data = []
        for i in range(1, 7):
            entities_data.extend(experiments['entities'][f'exp_{i}'][:duration])
            mirror_data.extend(experiments['mirror'][f'exp_{i}'][:duration])
        entities_mean = np.mean(entities_data)
        mirror_mean = np.mean(mirror_data)
        entities_means.append(entities_mean)
        mirror_means.append(mirror_mean)

    x = np.arange(len(durations))
    width = 0.35

    fig, ax = plt.subplots()

    bars1 = ax.bar(x - width/2, entities_means, width, label='entities')
    bars2 = ax.bar(x + width/2, mirror_means, width, label='mirror')

    ax.set_xlabel('player count')
    ax.set_ylabel('average CPU usage')
    ax.set_title('system CPU usage prototype vs player count')
    ax.set_xticks(x)
    ax.set_xticklabels(durations)
    ax.legend(framealpha=0)

    plt.savefig('plots/mean_cpu_usage.pdf')
    plt.show()

if __name__ == "__main__":
    folder_path = "system_logs"
    experiments = process_logs(folder_path)
    plot_mean_cpu_usage(experiments)
