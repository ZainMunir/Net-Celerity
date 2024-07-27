import pandas as pd
import glob
import os
import shared_config as sc

def run_summer():
    csv_files = glob.glob(f"{sc.formatted_stats_directory}*.csv")
    if len(csv_files) == 0:
        print("No CSV files found!")
        exit()

    summed_data = []

    for file in csv_files:
        df = pd.read_csv(file)
        summed_series = df.sum()
        summed_df = summed_series.to_frame().T
        summed_df['filename'] = os.path.basename(file)    
        summed_df['original_row_count'] = df.shape[0]    
        summed_data.append(summed_df)

    result_df = pd.concat(summed_data, ignore_index=True)
    
    result_df.to_csv(sc.summed_output, index=False)
    print("Summed CSV created successfully!")
    
if __name__ == "__main__":
    run_summer()