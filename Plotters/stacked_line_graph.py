import pandas as pd
import matplotlib.pyplot as plt
import shared_config as sc
import seaborn as sns
import matplotlib.pyplot as plt

def create_stacked_line_graph():

    if sc.average_output is None:
        print("No average output file found!")
        exit()

    average_df = pd.read_csv(sc.average_output)
    average_df.set_index("filename", inplace=True)

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
    ]

    final_columns = [col for col in final_columns if col in average_df.columns]

    ax = average_df[final_columns].plot(kind='area', stacked=True, figsize=(10, 6), alpha=0.6)

    plt.xlabel('Circuit Chunks')
    plt.ylabel('Average Frame Time (ns)')
    plt.title('Affect of Increasing Circuits')

    plt.xticks(rotation=90)

    plt.ylim(bottom=0)
    plt.legend(title='Columns')

    plt.tight_layout()
    plt.show()
    
    
if __name__ == "__main__":
    create_stacked_line_graph()