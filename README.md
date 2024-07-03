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

### Monitoring Script

### Example Experiment

### Plotting Script

### How to Procede 