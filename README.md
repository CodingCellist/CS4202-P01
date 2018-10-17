# CS4202 P01 - Branch Prediction
## Aim
The point of this practical is to implement and evaluate several branch-
prediction techniques, e.g. a 2-bit predictor.

## Tools Used
- Intel's [PIN](https://software.intel.com/en-us/articles/pin-a-dynamic-binary-instrumentation-tool)

## Required Programs
- [Python 3](https://www.python.org/downloads/) (>=3.6.6)
- tkinter

## Setup Instructions
- [OPTIONAL] create a python virtual environtment
  ```
  python3 -m venv <virtual_env_name>
  ```
  then, activate the virtual environment
  ```
  .  <virtual_env_name>/bin/activate
  ```
- install the python requirements
  ```
  pip3 install -r requirements.txt
  ```

## Run Instructions
- running a specific branch-predictor:
  ```
  python3 <path/to/specific_predictor.py> <path/to/infile.out>
  ```
  (some of the predictors take a table size. This can be specified through the
  `-s` or `--size` flag. For further help, use the `-h`/`--help` flag when
  running a program).
- running the data-generator (which runs all 5 branch-predictors):
  ```
  python3 <path/to/gen_data.py> <path/to/data/directory/> <path/to/outputfile.csv>
  ```
  See `-h`/`--help` for information about the optional flags.
- running the plotting tool (intended to work with data from the data-generator):
  ```
  python3 <path/to/draw_plots.py> <path/to/datafile.csv>
  ```
  See `-h`/`--help` for information about the optional flags.

## Programs Used for Testing
- [ffmpeg](https://ffmpeg.org/)
- `jpegtran` (part of [libjpeg-turbo](https://libjpeg-turbo.org/))
- my sudoku-solver written as part of CS2002
