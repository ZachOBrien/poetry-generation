# cs4120 - Natural Language Processing Final Project

# Poetry Generation

Zach O'Brien

Fall 2022

## Project Structure

**The main submission is `FINAL-PROJECT-DELIVERABLE.ipynb`.**

| Name | Purpose |
| ---- | ------- |
| data/ | Directory which holds raw base data, and intermediate derived datasets to use for model training. |
| scripts/ | Scripts to run steps in the processing pipeline like extracting poems from raw data or train a model. These are largely duplicated into `FINAL-PROJECT-DELIVERABLE.ipynb` so that the project can be completely re-created from that Jupyter Notebook. |
| src/ | Reusable code which is shared among `scripts/`, `test/`, and `FINAL-PROJECT-DELIVERABLE.ipynb` |
| test/ | Unit tests for code in `src/` |
| FINAL-PROJECT-DELIVERABLE.ipynb | A jupyter notebook which presents the project's work and final product. It can be run to reproduce the entire project from only the raw data file. |
| requirements.txt | External packages required by code in this project |

## Set up Environment

This project's dependencies are specified in a `requirements.txt` file, for use with Python's built-in `venv` virtual environment tool. 

**This project uses Python version 3.9.10. You can attempt to install the packages and run the code with a different version of Python and it might work, but using version 3.9.10 is probably best**.

1. Install Python version 3.9.10, and use that version for the following steps
    <br />

2. Create a new virtual environment for this project

    ```console
    python3 -m venv 4120_fp_obrien
    ```
    <br />
    
3. Activate the virtual environment

    ```console
    # On windows:
    4120_fp_obrien\Scripts\activate.bat
    ```
     <br />
    
    ```console
    # On Unix or MaxOS:
    source 4120_fp_obrien/bin/activate
    ```
     <br />
    
4. Install dependencies

    ```console
    # With the 4120_fp_obrien virtual environment activated:
    python -m pip install -r requirements.txt
    ```
     <br />

5. Install this project's modular source code. **This step is CRITICAL**. If skipped, imports will not work.

    ```console
    # With the 4120_fp_obrien virtual environment activated:
    cd src/

    # Now, in src/ directory:
    python -m pip install -e .
    ```
     <br />
    
6. Verify the installation was succesful by running the unit test suite

    ```console
    # In top-level project directory
    python -m pytest test/
    ```
    <br />

    **Steps 7 and 8 are only required if you wish to run the final submission Jupyter Lab Notebook**

7. Create an `ipykernel` kernel so that the jupyter notebook can access the virtual environment

    ```console
    # With the 4120_fp_obrien virtual environment activated:
    python -m ipykernel install --user --name=4120_fp_obrien
    ```
    <br />

8. Open Jupyter Lab and navigate to `FINAL-PROJECT-DELIVERABLE.ipynb` 

    ```console
    # With the 4120_fp_obrien virtual environment activated:
    jupyter-lab
    ```

## How to Run Unit Tests

First, activate the `4120-fp` conda environment. Then:

```shell
python -m pytest test/
```
