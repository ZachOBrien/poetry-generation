# cs4120 - Natural Language Processing Final Project

# Poetry Generation

Zach O'Brien

Fall 2022

## Set up Environment

This project's dependencies are specified in a **conda environment file**. To run the code in this repository, conda must be installed on your machine. See here for installation instructions: https://conda.io/projects/conda/en/latest/glossary.html#miniconda-glossary.

Once conda is installed on your machine, continue by creating a new environment for this project with the following commands.

```shell
# Create the new conda environment
conda env create -f environment.yml
```

```shell
# Show a list of conda environments to confirm that `4120-fp` is one of them
conda env list
```

```shell
# Activate the environment for your current shell
conda activate 4120-fp
```

Once the conda environment is set up, activate it and install the python source code for this project as a local, editable package. This **must** be done, or absolute imports will break and the code will not run.

```shell
# In src/ directory, with conda environment activated
(4120-fp) python -m pip install -e .
```

Verify that the package was installed by finding it with `conda list`

```shell
> (4120-fp) conda list
...
src     0.1.0     dev_0    <develop>
...
# Your version number will likely be different. That's not a problem.
```


## Run Unit Tests

First, activate the `4120-fp` conda environment. Then:

```shell
./run-unit-tests.sh
```
