# Net-Celerity

## Setting up Virtual Environment

In order to simplify the installation process we use [miniconda3](https://docs.anaconda.com/miniconda/) virtual environment and store all dependencies in the `environment.yml` file. Make sure to install it first.

To create conda environment do

```bash
conda env create -f environment.yml
```

and then activate it with

```bash
conda activate net-celerity-env
```

## Running the Experiments

### Editing config.cfg

Before running the experiments the `config.cfg` needs to be configured. The process is straightforward:

Path and execution related variables:

- **prototype_name**: the name of the prototype
- **prototype_logs**: location of the log folder for the prototype
- **prototype_server_command**: bash command to start the server
- **prototype_client_command**: bash command to start the client. Command can be further edited in the `prototype_experiment.sh` in case ip address that the user needs to connect to is not static and has to be configured once the server is initialized.
- **collection_script**: location of python script to execute log data collection.

Server/Client nodes related variables:

- **server_node**: name of a server node to ssh into. Can be only one.
- **client_nodes_number**: the amount of client nodes that needs to be reserved.
- **client_nodeN**: name of the client node to ssh into. Replace N with a number. Add as many as necessary by starting with 1 and incrementing the number. The amount of client nodes must be 1 to **client_nodes_number** for the script to work as intended.

### Collection Script

Collection script is a python script that is run at the end of experiment to collect all relevant metrics and store them in one `<NAME>_results.csv` file. Currently it works by counting how many player scripts are available in the folder and then going individually through them and storing the round-trip time in a common .csv file with dedicated ID for the player. The headers of .csv are:

```
Player_ID;Total_Players;RoundTripDelay_ms
```

One drawback to this approach is that it is individual to a prototype since the logging is done with different fields. However, for the future prototypes if the field names are the same as in one of the provided collector script they can be reused.

In total we have three scripts: `mirror_collect_script.py` for M-KCP, `mirror_t_collect_script.py` for M-TP, and `entities_collect_script.py` for DOTS-NFE.

### Monitoring Script

System metrics monitoring is done using `psutil` python script and is the same for every prototype. It is attached to the server and monitors quite a few metrics. All of them can be seen in the `system_monitor.py`. They are later stored in the following manner:

```bash
system_logs/${prototype_name}/system_log_${num_players}p_${benchmark_duration}s.csv
```

### Example Experiment

All the experiments provided can be reproduced, however, it is quite time consuming. To analyze different player activities of a single prototype we would require: 2 * ( (20 * 3 + 120) + (40 * 3 + 120) + (60 * 3 + 120) + (80 * 3 + 120) ) = 2160 second or 36 minutes, where 3 is a time for spawning a player and 2 is how many player activities we use.

In order to reproduce the experiments and not change the `config.cfg` too often we recommend going through all the workload within the same prototype and then move on.

To make it even simpler it is possible to copy the bash commands from `prototype_experiment.sh` and into a separate script per prototype if there are several machine at your disposal to run concurrently. We provide three examples: `mirror_experiment.sh` for M-KCP, `entities_experiment.sh` for DOTS-NFE, and `prototype_experiment.sh` applicable to any prototype, and currently set up for M-TP. Once values in the `config.cfg` are configured the scripts can be run.

**IMPORTANT NOTE:** make sure that the folders that the scripts are using exists (even empty).

### Plotting Script

All the plotting is done in `plot_results.py`. It can be executed whenever user wants to visualize the results. The user can feel free to adjust any styling choices and make them suitable for their needs. Currently we provide 12 functions for various plots, which, once again, user can choose freely.

## How to Proceed

If you want to use your own prototype with Net-Celerity make sure to fulfil the following requirements:

1. It can headlessly run player emulation from input traces.
2. The controls are: W - move forward, S - move backwards, A - move left, D - move right, Left Mouse Key - destroy a block, Right Mouse Key - place a block.
3. Build of the game is for Linux.

However, those requirements, besides the third one, are necessary only in case the new prototype wants to be compared with our existing work. If developer wants to compare their own implementations of different games, it is also possible, and player emulation can be also tested but not with out input traces.

Overall, we hope that this benchmark will be useful for the developers and they will have fun experimenting and testing different prototypes!
