import os

data_directory = "../Data/"
experiment_name = "base"
filter_by_max_terrainarea = True
filter_by_max_players = True

experiment_directory = f"{data_directory}{experiment_name}/"
formatted_stats_directory = f"{experiment_directory}formatted_stats/"
if not os.path.exists(formatted_stats_directory):
    os.makedirs(formatted_stats_directory)
plots_directory = f"{experiment_directory}plots/"
if not os.path.exists(plots_directory):
    os.makedirs(plots_directory)

summed_output = f"{experiment_directory}summed_output.csv"
average_output = f"{experiment_directory}averaged_output.csv"