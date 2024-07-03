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

- **prototype_name**: the name of the prototype
- **prototype_logs**: location of the log folder for the prototype
- **prototype_server_command**: bash command to start the server
- **prototype_client_command**: bash command to start the client. Command can be further edited in the `prototype_experiment.sh` in case ip address that the user needs to connect to is not static and has to be configured once the server is initialized.
- **collection_script**: location of python script to execute log data collection.

### Collection Script

### Monitoring Script

### Example Experiment

### Plotting Script

### How to Procede 