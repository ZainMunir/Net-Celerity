import pandas as pd
import matplotlib.pyplot as plt
import shared_config as sc
import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-colorblind')
sns.set_palette('colorblind')

def create_stacked_line_graph():
    average_df = pd.read_csv(sc.average_output)
    if average_df.empty:
        print("Average CSV is empty!")
        exit()
    average_df.set_index("Chunks", inplace=True)

    final_columns = [
        "Main Thread_other",
        "ServerFixedUpdate_other",
        "StatisticsSystem",
        "PlayerTerrainGenCheck",
        "TerrainGeneration",
        "StructureGeneration",
        "TerrainLogicSystem_other",
        "GetUpdates",
        "ReevaluatePropagateMarker",
        "PropagateLogicState",
        "CheckGateState", 
        # "Main Thread"   
    ]

    final_columns = [col for col in final_columns if col in average_df.columns]
    average_df[final_columns] = average_df[final_columns] / 1e6

    ax = average_df[final_columns].plot(kind='area', stacked=True, figsize=(10, 6), alpha=0.6)

    plt.xlabel('Circuit Chunks')
    plt.ylabel('Average Frame Time (ms)')


    plt.ylim(bottom=0)
    plt.legend(title='Columns', loc='upper left')

    plt.tight_layout()
    # plt.show()
    plt.savefig(f"{sc.plots_directory}{sc.experiment_name}-stacked-line-1.pdf", format='pdf', bbox_inches="tight")
    
    
if __name__ == "__main__":
    create_stacked_line_graph()