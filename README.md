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

This project's dependencies are specified in a `requirements.txt` (and `requirements-apple-silicon.txt`) file, intended for use with Python's built-in `venv` virtual environment tool. 

**This project uses Python version 3.9.10. You can attempt to install the packages and run the code with a different version of Python and it might work, but using version 3.9.10 is probably best**.

1. Install Python version 3.9.10, and use that version for the following steps

2. Create a new virtual environment for this project

    ```
    python3 -m venv env
    ```

3. Activate the virtual environment

    ```
    # On windows:
    env\Scripts\activate.bat
    ```
    
    ```
    # On Unix or MaxOS:
    source env/bin/activate
    ```
    
4. Install dependencies

    On Apple silicon:
    ```
    # With the env virtual environment activated:
    python -m pip install -r requirements-apple-silicon.txt
    ```

    On all other platforms, including intel-based macs:
    ```
    # With the env virtual environment activated:
    python -m pip install -r requirements.txt
    ```

5. Install prerequisite Natural Language Toolkit (NLTK) data

    ```
    # With the env virtual environment activated:
    python
    >>> import nltk
    >>> nltk.download("punkt")
    ```

6. Install this project's modular source code. **This step is CRITICAL**. If skipped, imports will not work.

    ```
    # With the env virtual environment activated:
    cd src/

    # Now, in src/ directory:
    python -m pip install -e .
    ```
    
7. Verify the installation was succesful by running the unit test suite

    ```
    # In top-level project directory
    python -m pytest test/
    ```

    **Steps 7 and 8 are only required if you wish to run the Jupyter Notebook**

8. Create an `ipykernel` kernel so that the jupyter notebook can access the virtual environment

    ```
    # With the env virtual environment activated:
    python -m ipykernel install --user --name=env
    ```

9. Open Jupyter Lab and navigate to `env.ipynb` 

    ```
    # With the env virtual environment activated:
    jupyter-lab
    ```

## How to Run Unit Test Suite

First, activate the `env` virtual environment. Then:

```shell
python -m pytest test/
```
