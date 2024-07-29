import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import shared_config as sc
import seaborn as sns
import numpy as np
import os
import re

matplotlib.rcParams.update({"font.size": 15})
plt.style.use("seaborn-v0_8-colorblind")
sns.set_palette("colorblind")


def create_stacked_line_graph():
    player_experiments = [
        f"{sc.data_directory}{x}/"
        for x in os.listdir(sc.data_directory)
        if "players" in x
    ]
    average_dfes = [exp + "averaged_output.csv" for exp in player_experiments]

    fig, (ax1, ax2) = plt.subplots(
        2, 1, sharex=True, height_ratios=[10, 1], figsize=(10, 6)
    )

    handles = []
    labels = []
    min_ys = []
    max_ys = []
    for average_df_file in average_dfes:
        if not os.path.exists(average_df_file):
            print(f"{average_df_file} does not exist")
            exit()
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

        scatter = ax1.scatter(x, y, alpha=0.6)
        (line,) = ax1.plot(x, a * x + b)

        handles.append((scatter, line))
        search = re.search(r"players(.+)\/", average_df_file)
        if search:
            val = search.group(1)
            if "-activeLogic" in val:
                labels.append(f"{val.replace('-activeLogic_', '')} (Logic Active)")
            else: 
                labels.append(search.group(1).replace("_", ""))
        else:
            raise ValueError("Invalid experiment name")

        ax1.spines.bottom.set_visible(False)
        ax2.spines.top.set_visible(False)
        ax1.xaxis.tick_top()
        ax1.tick_params(labeltop=False, top=False)
        ax2.xaxis.tick_bottom()

        d = 0.5
        kwargs = dict(
            marker=[(-1, -d), (1, d)],
            markersize=12,
            linestyle="none",
            color="k",
            mec="k",
            mew=1,
            clip_on=False,
        )
        ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
        ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)

    ax1.set_ylim(min(min_ys) - 10, max(max_ys) + 10)
    ax2.set_ylim(0, 10)

    legend_handles = [h[0] for h in handles] + [h[1] for h in handles]
    fig.legend(legend_handles, labels, bbox_to_anchor=[0.1, 0.1], loc='lower left')


    fig.text(0.5, 0, x_label, ha="center")
    fig.text(0, 0.5, "Server FPS", va="center", rotation="vertical")

    plt.ylim(bottom=0)

    plt.tight_layout()
    # plt.show()
    plt.savefig(f"{sc.plots_directory}players-fps.pdf", format="pdf")
    print(f"Saved plot to {sc.plots_directory}players-fps.pdf")


if __name__ == "__main__":
    create_stacked_line_graph()
