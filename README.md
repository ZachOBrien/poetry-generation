# Poetry Generation

Zach O'Brien

December 2022

## Project Structure

| Name | Purpose |
| ---- | ------- |
| [data/](data/) | Holds raw base data, and intermediate derived datasets used for model training |
| [scripts/](scripts/) | Scripts to run steps in the processing pipeline like extracting poems from raw data or training a model. These are largely glued together in `poetry-generation.ipynb` so that the project can be completely re-created from that notebook. |
| [src/](src/) | Modular, reusable code which is shared among `scripts/`, `test/`, and `poetry-generation.ipynb` |
| [test/](test/) | Unit tests for code in `src/` |
| [poetry-generation.ipynb](poetry-generation.ipynb) | A jupyter notebook which presents the project's work and final product. It can be run to reproduce the entire project from only the raw data file. |
| [requirements.txt](requirements.txt) | External packages required by code in this project |

## Set up Environment

This project's dependencies are specified in a `requirements.txt` file, intended for use with Python's built-in `venv` virtual environment tool. 

**This project uses Python version 3.9.10. You can attempt to install the packages and run the code with a different version of Python and it might work, but using version 3.9.10 is probably best**.

1. Install Python version 3.9.10, and use that version for the following steps

2. Create a new virtual environment for this project

    ```console
    python3 -m venv poetry-generation
    ```

3. Activate the virtual environment

    ```console
    # On windows:
    poetry-generation\Scripts\activate.bat
    ```
    
    ```console
    # On Unix or MaxOS:
    source poetry-generation/bin/activate
    ```
    
4. Install dependencies

    ```console
    # With the poetry-generation virtual environment activated:
    python -m pip install -r requirements.txt
    ```

5. Install this project's modular source code. **This step is CRITICAL**. If skipped, imports will not work.

    ```console
    # With the poetry-generation virtual environment activated:
    cd src/

    # Now, in src/ directory:
    python -m pip install -e .
    ```
    
6. Verify the installation was succesful by running the unit test suite

    ```console
    # In top-level project directory
    python -m pytest test/
    ```

    **Steps 7 and 8 are only required if you wish to run the Jupyter Notebook**

7. Create an `ipykernel` kernel so that the jupyter notebook can access the virtual environment

    ```console
    # With the poetry-generation virtual environment activated:
    python -m ipykernel install --user --name=poetry-generation
    ```

8. Open Jupyter Lab and navigate to `poetry-generation.ipynb` 

    ```console
    # With the poetry-generation virtual environment activated:
    jupyter-lab
    ```

## How to Run Unit Test Suite

First, activate the `poetry-generation` virtual environment. Then:

```shell
python -m pytest test/
```
