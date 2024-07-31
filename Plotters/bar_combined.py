import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import shared_config as sc
import seaborn as sns
import numpy as np
import os
import sys
import re
from PIL import Image
import matplotlib.patches as mpatches


def overlay_images(base_image_path, overlay_images_paths, shift_constant):
    base_image = Image.open(base_image_path).convert("RGBA")
    print(base_image_path)

    for i, overlay_image_path in enumerate(overlay_images_paths):
        print(overlay_image_path)
        overlay_image = Image.open(overlay_image_path).convert("RGBA")

        horizontal_shift = i * shift_constant

        new_image_width = base_image.width + horizontal_shift
        new_image_height = max(base_image.height, overlay_image.height)
        new_image = Image.new("RGBA", (new_image_width, new_image_height), (0, 0, 0, 0))

        new_image.paste(base_image, (0, 0), base_image)

        new_image.paste(overlay_image, (horizontal_shift, 0), overlay_image)

        base_image = new_image

    return base_image


def sort_list2_by_list1(list1, list2):
    order_dict = {value: index for index, value in enumerate(list1)}

    def extract_key(item):
        key_part = item.split(".")[0] 
        return order_dict.get(
            key_part, float("inf")
        )  

    sorted_list2 = sorted(list2, key=extract_key)

    return sorted_list2


def create_bar_graph(all_data=False):
    player_experiments = [
        f"{sc.data_directory}{x}/"
        for x in os.listdir(sc.data_directory)
        if "players" in x and not "TerrainCircuitry" in x
    ]
    average_csvs = [exp + "averaged_output.csv" for exp in player_experiments]

    order = [
        "Dummy",
        "Empty",
        "Empty (Logic Active)",
        "1-Layer (Logic Active)",
        "RollingHills",
        "RollingHills (Logic Active)",
    ]  # , "TerrainCircuitry (Logic Active)"]
    patterns = ["", "/", "-", "x", "o", ".", "*"]

    output_files = []
    for average_csvs in average_csvs:
        if not os.path.exists(average_csvs):
            print(f"{average_csvs} does not exist")
            continue

        average_df = pd.read_csv(average_csvs)
        average_df.set_index("players", inplace=True)

        search = re.search(r"players(.+)\/", average_csvs)
        if search:
            val = search.group(1)
            if "-activeLogic" in val:
                val = f"{val.replace('-activeLogic_', '')} (Logic Active)"
            else:
                val = val.replace("_", "")
        else:
            raise ValueError("Invalid experiment name")

        columns = [
            "StatisticsSystem",
            "PlayerTerrainGenCheck",
            "TerrainGeneration",
            "StructureGeneration",
            "TerrainLogicSystem",
        ]

        if all_data:
            columns = [
                "Main Thread_other",
                "ServerFixedUpdate_other",
            ] + columns

        x = average_df.index
        y = average_df[columns] / 1e6

        total_width = 0.9
        bar_width = total_width / len(order)
        hatching_index = order.index(val)

        ax = y.plot(
            kind="bar", stacked=True, figsize=(10, 6), width=bar_width, legend=False
        )

        ax.set_xlabel("Players")
        ax.set_ylabel("Time (ms)")
        if all_data:
            ax.set_ybound(0, 9)
        else:
            ax.set_ybound(0, 0.8)
        addition = "png"
        transparent = True
        if val == "Dummy":
            first_legend = ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
            ax.add_artist(first_legend)
            ax.figure.set_figwidth(13.5)
            transparent = False
            ax.set_xlim(-0.5, len(x) - 0.5)
            
            box = ax.get_position()
            ax.set_position([box.x0*.8, box.y0, box.width * 0.77, box.height])

            legend_marker = []
            for order_val in order[1:]:
                circ = mpatches.Patch(
                    facecolor="white",
                    edgecolor="black",
                    hatch=patterns[order.index(order_val)],
                    label=order_val,
                )
                legend_marker.append(circ)
            ax.legend(handles=legend_marker, loc="center", bbox_to_anchor=(1.22, 0.2))
            # addition = "pdf"
        else:
            ax.set_axis_off()
            bars = ax.patches
            pattern = patterns[
                hatching_index
            ]  # set hatch patterns in the correct order
            hatches = []  # list for hatches in the order of the bars
            for i in range(int(len(bars))):
                hatches.append(pattern)
            for bar, hatch in zip(
                bars, hatches
            ):  # loop over bars and hatches to set hatches in correct order
                bar.set_hatch(hatch)

        ax.set_xticklabels(x, rotation=0)
        ax.tick_params(bottom=False)

        output_filename = f"{val}.{addition}"
        output_files.append(output_filename)
        ax.figure.savefig(output_filename, transparent=transparent, format=addition)
        # plt.close(fig)

    output_files = sort_list2_by_list1(order, output_files)

    overlayed_image = overlay_images(output_files[0], output_files[1:], 13)
    addition = 2 if all_data else 1
    overlayed_image.save(f"{sc.plots_directory}players-bar-combined-{addition}.png",
    )
    
    for output_file in output_files:
        os.remove(output_file)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "all":
            create_bar_graph(True)
        else:
            print("Invalid argument. Usage: python3 bar_combined.py [all]")
    else:
        create_bar_graph()
