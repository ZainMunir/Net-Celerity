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
    
    fps = 1 / (average_df["Main Thread"] / 1e9)
    average_df["FPS"] = fps       

    ax = average_df["FPS"].plot(kind='bar', figsize=(10, 6), alpha=0.6, color='blue')

    plt.xlabel('Circuit Chunks')
    plt.ylabel('Server FPS')
    
    plt.ylim(bottom=0)

    plt.tight_layout()
    # plt.show()
    plt.savefig(f"{sc.plots_directory}{sc.experiment_name}-fps.pdf", format='pdf')
    
    
if __name__ == "__main__":
    create_stacked_line_graph()