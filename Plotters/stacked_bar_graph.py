import pandas as pd
import matplotlib.pyplot as plt
import shared_config as sc
import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8-colorblind")
sns.set_palette("colorblind")


def create_stacked_line_graph():
    average_df = pd.read_csv(sc.average_output)
    if average_df.empty:
        print("Average CSV is empty!")
        exit()
    if "base" in sc.experiment_name: 
        average_df.set_index("Chunks", inplace=True)
        x_label = "Chunks"
    elif  "players" in sc.experiment_name:
        average_df.set_index("players", inplace=True)
        x_label = "Players"
    else:
        raise ValueError("Invalid experiment name")
    
    average_df.sort_index(inplace=True)
    
    final_columns = [
        "TerrainLogicSystem_other",
        "GetUpdates",
        "ReevaluatePropagateMarker",
        "PropagateLogicState",
        "CheckGateState",
    ]

    addition = 1
    legend = "lower right"
    if sc.all_data:
        final_columns = [
            "Main Thread_other",
            "ServerFixedUpdate_other",
            "StatisticsSystem",
            "PlayerTerrainGenCheck",
            "TerrainGeneration",
            "StructureGeneration",
        ] + final_columns
        addition = 2
        legend = "lower left"
        

    final_columns = [col for col in final_columns if col in average_df.columns]
    average_df[final_columns] = average_df[final_columns] / 1e6

    # Plot the stacked bar chart
    ax = average_df[final_columns].plot(kind="barh", stacked=True, figsize=(10, 6))

    plt.ylabel(x_label)
    plt.xlabel("Average Frame Time (ms)")

    plt.ylim(bottom=0)
    plt.legend(title="Columns", loc=legend)

    plt.tight_layout()
    # plt.show()
    plt.savefig(
        f"{sc.plots_directory}{sc.experiment_name}-stacked-bar-{addition}.pdf", format="pdf"
    )


if __name__ == "__main__":
    create_stacked_line_graph()
