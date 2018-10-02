# ECSOpenData

### This is a work in progress demostration for a combined data management engine

#### To setup the `conda` environment to run the Flask application:
```
conda env create -f environment.yml
```
Note, that the above is one time step.

#### To run this from the command line:
```
# The `conda activate` step only needs to be done once per shell.
conda activate ecsopendata
# Start the server
python ecsopendata/server.py
# Open a web browser with the following URL: http://127.0.0.1:5000/login
```
