# ECSOpenData

### This is a work in progress demostration for a combined data management engine

[![Build Status](https://travis-ci.org/ECSHackWeek/ECSOpenData.svg?branch=master)](https://travis-ci.org/ECSHackWeek/ECSOpenData)
[![Coverage Status](https://coveralls.io/repos/github/ECSHackWeek/ECSOpenData/badge.svg?branch=master)](https://coveralls.io/github/ECSHackWeek/ECSOpenData?branch=master)

#### To setup the `conda` environment to run the Flask application:
```
conda env create -f environment.yml
```
Note, that the above is one time step.

#### To run this from the command line:
```
# The `conda activate` step only needs to be done once per shell instance
conda activate ecsopendata
# Start the server using the run script
./run
# Open a web browser with the following URL: http://127.0.0.1:5000/login
```
