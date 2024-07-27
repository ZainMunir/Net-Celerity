import pandas as pd
import glob
import os
import shared_config as sc

def main():
    if sc.summed_output is None:
        print("No summed output file found!")
        exit()

    summed_df = pd.read_csv(sc.summed_output)
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

    average_df.to_csv(sc.average_output, index=True)
    print("Averaged CSV created successfully!")