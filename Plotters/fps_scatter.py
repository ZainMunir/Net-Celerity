import pandas as pd
import matplotlib.pyplot as plt
import shared_config as sc
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-v0_8-colorblind')
sns.set_palette('colorblind')

def create_stacked_line_graph():
    average_df = pd.read_csv(sc.average_output)
    if average_df.empty:
        print("Average CSV is empty!")
        exit()
    if "base" in sc.experiment_name: 
        average_df.set_index("Chunks", inplace=True)
        x_label = "Circuits"
    elif  "players" in sc.experiment_name:
        average_df.set_index("players", inplace=True)
        x_label = "Players"
    else:
        raise ValueError("Invalid experiment name")

    fps = 1 / (average_df["Main Thread"] / 1e9)
    average_df["FPS"] = fps       
    
    
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[10, 1])
    x = average_df.index
    y = average_df["FPS"]
    min_y = y.min()
    a, b = np.polyfit(x, y, 1)

    
    ax1.scatter(x, y,   alpha=0.6, color='blue')
    ax1.plot(x, a*x+b)       
    
    ax1.set_ylim(min_y - 20, 300)
    ax2.set_ylim(0, 10) 
    
    ax1.spines.bottom.set_visible(False)
    ax2.spines.top.set_visible(False)
    ax1.xaxis.tick_top()
    ax1.tick_params(labeltop=False, top=False) 
    ax2.xaxis.tick_bottom()
    
    d = .5  
    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
              linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
    ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)
            
    fig.text(0.5, 0, x_label, ha='center')
    fig.text(0, 0.5, 'Server FPS', va='center', rotation='vertical')
    
    plt.ylim(bottom=0)

    plt.tight_layout()
    # plt.show()
    plt.savefig(f"{sc.plots_directory}{sc.experiment_name}-fps.pdf", format='pdf')
    
    
if __name__ == "__main__":
    create_stacked_line_graph()