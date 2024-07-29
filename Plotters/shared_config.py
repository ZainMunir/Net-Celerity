import os

data_directory = "../Data/"
experiment_name = "players_1-Layer"
filter_by_max_terrainarea = True
filter_by_max_players = True
all_data = True

experiment_directory = f"{data_directory}{experiment_name}/"
formatted_stats_directory = f"{experiment_directory}formatted_stats/"
if not os.path.exists(formatted_stats_directory):
    os.makedirs(formatted_stats_directory)
plots_directory = f"../Plots/"
if not os.path.exists(plots_directory):
    os.makedirs(plots_directory)

summed_output = f"{experiment_directory}summed_output.csv"
average_output = f"{experiment_directory}averaged_output.csv"

terrain_to_layer_num = {
    "Empty": 0,
    "1-Layer": 1,
    "2-Layer": 2,
    "3-Layer": 3,
    "TerrainCircuitry": 1,
    "RollingHills": 0,
}

gate_blocks_per_chunk = 32
input_blocks_per_chunk = 15

def get_circuit_chunks(chunkX, chunkZ, layer):
    return chunkX * chunkZ * terrain_to_layer_num[layer]

def get_total_circuit_blocks(chunks):
    return chunks * (gate_blocks_per_chunk + input_blocks_per_chunk)