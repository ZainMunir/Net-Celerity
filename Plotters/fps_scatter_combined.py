import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import shared_config as sc
import seaborn as sns
import numpy as np
import os
import re

def create_fps_scatter():
    player_experiments = [
        f"{sc.data_directory}{x}/"
        for x in os.listdir(sc.data_directory)
        if "players" in x
    ]
    average_dfes = [exp + "averaged_output.csv" for exp in player_experiments]

    fig, ax = plt.subplots(
        1, 1, sharex=True, height_ratios=[10], figsize=(10, 6)
    )

    handles = []
    labels = []
    min_ys = []
    max_ys = []
    for average_df_file in average_dfes:
        if not os.path.exists(average_df_file):
            print(f"{average_df_file} does not exist")
            continue
        average_df = pd.read_csv(average_df_file)
        average_df.set_index("players", inplace=True)
        x_label = "Players"
        fps = 1 / (average_df["Main Thread"] / 1e9)
        average_df["FPS"] = fps

        x = average_df.index
        y = average_df["FPS"]

        max_ys.append(y.max())
        min_ys.append(y.min())

        a, b = np.polyfit(x, y, 1)

        scatter = ax.scatter(x, y, alpha=0.6)
        (line,) = ax.plot(x, a * x + b)

        handles.append((scatter, line))
        search = re.search(r"players(.+)\/", average_df_file)
        if search:
            val = search.group(1)
            if "-activeLogic" in val:
                labels.append(f"{val.replace('-activeLogic_', '')} (Logic Active)")
            else: 
                labels.append(val.replace("_", ""))
        else:
            raise ValueError("Invalid experiment name")

    legend_handles = [h[0] for h in handles] + [h[1] for h in handles]
    fig.legend(legend_handles, labels, bbox_to_anchor=[0.1, 0.1], loc='lower left')


    fig.text(0.5, 0, x_label, ha="center")
    fig.text(0, 0.5, "Server FPS", va="center", rotation="vertical")

    plt.ylim(bottom=0)

    plt.tight_layout()
    # plt.show()
    plt.savefig(f"{sc.plots_directory}players-fps-2.pdf", format="pdf")
    print(f"Saved plot to {sc.plots_directory}players-fps.pdf")


if __name__ == "__main__":
    create_fps_scatter()
