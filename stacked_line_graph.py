import pandas as pd
import matplotlib.pyplot as plt

data_directory = "Data/"
experiment_name = "base"
experiment_directory = f"{data_directory}{experiment_name}/"
summed_df = pd.read_csv(f"{experiment_directory}summed_output.csv")
summed_df.sort_values("NumInputTypeBlocks", inplace=True)

columns_to_average = [
    "Main Thread",
    "ServerFixedUpdate",
    "TerrainGeneration",
    "PlayerTerrainGenCheck",
    "StructureGeneration",
    "TerrainLogicSystem",
    "GetUpdates",
    "ReevaluatePropagateMarker",
    "PropagateLogicState",
    "CheckGateState",
    "StatisticsSystem",
]

average_df = summed_df[columns_to_average].div(summed_df["original_row_count"], axis=0)

average_df["filename"] = [x.split("_")[1] + (" (Logic Active)" if "-activeLogic" in x else "") for x in summed_df["filename"]]
average_df.set_index("filename", inplace=True)

subsets = {
    "Main Thread": [
        "ServerFixedUpdate",
    ],
    "ServerFixedUpdate": [
        "TerrainGeneration",
        "PlayerTerrainGenCheck",
        "StructureGeneration",
        "TerrainLogicSystem",
        "StatisticsSystem",
    ],
    "TerrainLogicSystem": [
        "GetUpdates",
        "ReevaluatePropagateMarker",
        "PropagateLogicState",
        "CheckGateState",
    ],
}


for main_column, subset_columns in subsets.items():
    if main_column in average_df.columns and all(
        col in average_df.columns for col in subset_columns
    ):
        subset_sum = average_df[subset_columns].sum(axis=1)
        average_df[main_column + "_other"] = average_df[main_column] - subset_sum

average_df.to_csv(f"{experiment_directory}averaged_output.csv", index=True)
final_columns = [
    "GetUpdates",
    "ReevaluatePropagateMarker",
    "PropagateLogicState",
    "CheckGateState",
    "TerrainLogicSystem_other",
    "StructureGeneration",
    "TerrainGeneration",
    "PlayerTerrainGenCheck",
    "StatisticsSystem",
    # "ServerFixedUpdate_other",
    # "Main Thread_other",
]
final_columns.reverse()

final_columns = [col for col in final_columns if col in average_df.columns]

ax = average_df[final_columns].plot(kind='area', stacked=True, figsize=(10, 6), alpha=0.6)

plt.xlabel('Experiment')
plt.ylabel('Average Values')
plt.title('Stacked Area Plot')

plt.xticks(rotation=90)

plt.ylim(bottom=0)
plt.legend(title='Columns')

plt.tight_layout()
plt.show()