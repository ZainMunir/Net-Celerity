import pandas as pd
import glob
import os

data_directory = "Data/"
experiment_name = "base"
experiment_directory = f"{data_directory}{experiment_name}/"
formatted_stats_directory = f"{experiment_directory}formatted_stats/"
if not os.path.exists(formatted_stats_directory):
    exit("No formatted stats directory found. Please run data_formatter.py first.")


csv_files = glob.glob(f"{formatted_stats_directory}*.csv")

summed_data = []

for file in csv_files:
    df = pd.read_csv(file)
    summed_series = df.sum()
    summed_df = summed_series.to_frame().T
    summed_df['filename'] = os.path.basename(file)    
    summed_df['original_row_count'] = df.shape[0]    
    summed_data.append(summed_df)

result_df = pd.concat(summed_data, ignore_index=True)
result_df.to_csv(f"{experiment_directory}summed_output.csv", index=False)
print("Summed CSV created successfully!")