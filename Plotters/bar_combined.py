import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import shared_config as sc
import seaborn as sns
import numpy as np
import os
import sys
import re

#https://stackoverflow.com/questions/22787209/how-to-have-clusters-of-stacked-bars
def plot_clustered_stacked(dfall, labels=None,   H="/", **kwargs):
    """Given a list of dataframes, with identical columns and index, create a clustered stacked bar plot. 
labels is a list of the names of the dataframe, used for the legend
title is a string for the title of the plot
H is the hatch used for identification of the different dataframe"""

    n_df = len(dfall)
    n_col = len(dfall[0].columns) 
    n_ind = len(dfall[0].index)
    axe = plt.subplot(111)
    axe.figure.set_size_inches(16, 6)
    axe.figure.tight_layout(rect=[.05, 0.05,.75,1])
    
     
    for df in dfall : # for each data frame
        axe = df.plot(kind="bar",
                      linewidth=0,
                      stacked=True,
                      ax=axe,
                      legend=False,
                      grid=False,
                      **kwargs)  # make bar plots

    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
        for j, pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
                rect.set_hatch(H * int(i / n_col)) #edited part     
                rect.set_width(1 / float(n_df + 1))

    axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.)
    axe.set_xticklabels(df.index, rotation = 0)

    # Add invisible data to add another legend
    n=[]        
    for i in range(n_df):
        n.append(axe.bar(0, 0, color="gray", hatch=H * i))

    l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.01, 0.5])
    if labels is not None:
        l2 = plt.legend(n, labels, loc=[1.01, 0.1]) 
    axe.add_artist(l1)
    return axe


def create_bar_graph(all_data=False ):
    player_experiments = [
        f"{sc.data_directory}{x}/"
        for x in os.listdir(sc.data_directory)
        if "players" in x # and not "TerrainCircuitry" in x
    ]
    average_dfes = [exp + "averaged_output.csv" for exp in player_experiments]
    data_frames = []
    for average_df_file in average_dfes:
        if not os.path.exists(average_df_file):
            print(f"{average_df_file} does not exist")
            continue
        average_df = pd.read_csv(average_df_file)
        average_df.set_index("players", inplace=True)
        search = re.search(r"players(.+)\/", average_df_file)
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
        
        y = average_df[columns] / 1e6
        
        df = pd.DataFrame(y)
        df.insert(len(df.columns), 'name', [val for _ in range(len(df))], True)
        data_frames.append(df)
        

    dfall = pd.concat(data_frames)
    dfall.to_csv("test.csv")
    dfall = dfall.groupby('name')
    names = list(dfall["name"].head().unique())
    names.sort()
    dfall = [group for _, group in dfall]
    axe = plot_clustered_stacked(dfall, names, edgecolor='black')
    axe.set_yscale('log')
    axe.set_ylabel('Average frame time (ms)')
    axe.set_xlabel('Players')
    axe.figure.show()
    addition = 1
    if all_data:
        addition = 2
    axe.figure.savefig(f"{sc.plots_directory}players-stacked-bar-{addition}.pdf", format="pdf")



if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "all":
            create_bar_graph(True)
        else:
            print("Invalid argument. Usage: python3 bar_combined.py [all]")
    else:
        create_bar_graph()
    
    
