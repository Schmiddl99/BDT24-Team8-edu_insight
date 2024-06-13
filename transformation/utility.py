import nbformat
from nbconvert import PythonExporter
from nbconvert.preprocessors import ExecutePreprocessor


### convert ipynb to extract variables

def extract_variables_from_notebook(notebook_path):
    # Read the notebook
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    # Execute the notebook
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb) #, {'metadata': {'path': '.'}})

    # Convert the notebook to a Python script
    python_exporter = PythonExporter()
    python_script, _ = python_exporter.from_notebook_node(nb)

    # Create a dictionary to capture the notebook variables
    notebook_vars = {}
    
    # Execute the Python script and capture the variables
    exec(python_script, notebook_vars)
    
    return notebook_vars