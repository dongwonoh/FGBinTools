#!/usr/bin/env python3

# Script to convert csv to FaceGen control file (.ctl)
#
# DongWon Oh (dongwonohphd@gmail.com) (National University of Singapore)
# original code by Ron Dotsch (rdotsch@gmail.com) circa 2017
#
# prerequisite: FaceGen Modeller SDK, FGBinTools
#
# Last update: 26 Aug 2024
# - takes output path argument (default: current folder) and parameter length argument (default: 100)
# - takes header argument (default: True)
# - made Python-3 compatible (2023)

import sys
import csv
from FGBinTools import insertSlider
from LinAlgTools import normalize
from numpy import array
import shutil
import os

def print_usage():
    print("Usage: python csv2ctl.py <control_file.csv> [num_parameters] [output_path] [has_header]")
    print("  <control_file.csv>: Path to the CSV file containing control data")
    print("  [num_parameters]: Optional. Number of parameters (100 or 130). Default is 100.")
    print("  [output_path]: Optional. Path where the output .ctl file will be saved. Default is current directory.")
    print("  [has_header]: Optional. 'True' if the CSV has a header row, 'False' otherwise. Default is True.")
    print("\nExample:")
    print("  python csv2ctl.py controls.csv 130 ./output True")

def process_csv(file_path, num_params=100, output_path=".", has_header=True):
    with open(file_path, 'r') as source:
        csv_reader = csv.reader(source)
        if has_header:
            next(csv_reader)  # Skip header row (first row) if there is one

        ctlfile_path = os.path.join(output_path, os.path.basename(file_path).replace('.csv', '.ctl'))
        with open(ctlfile_path, 'w') as ctlfile:
            for row in csv_reader:
                if row[0] == 'label':
                    continue

                if num_params == 130:
                    SS = normalize(array([float(i) for i in row[1:51]]))
                    TS = normalize(array([float(i) for i in row[-50:]]))  # Last 50 entries
                elif num_params == 100:
                    SS = normalize(array([float(i) for i in row[1:51]]))
                    TS = normalize(array([float(i) for i in row[51:101]]))
                else:
                    raise ValueError(f"Invalid number of parameters: {num_params}")
    insertSlider(line[0], SS.tolist(), 'SS', ctlfile)
    insertSlider(line[0], TS.tolist(), 'TS', ctlfile)

    print("Conversion complete. Output saved to: " + ctlfile_path)

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    control_file = sys.argv[1]
    num_params = 100 if len(sys.argv) < 3 or not sys.argv[2].isdigit() else int(sys.argv[2])
    output_path = "." if len(sys.argv) < 4 else sys.argv[3]
    has_header = True if len(sys.argv) < 5 or sys.argv[4].lower() != 'false' else False

    if num_params not in [100, 130]:
        print(f"Error: Number of parameters must be 100 or 130. Got {num_params}")
        print_usage()
        sys.exit(1)

    try:
        process_csv(control_file, num_params, output_path, has_header)
        # Attempt to delete __pycache__ directory
        shutil.rmtree('__pycache__', ignore_errors=True)
        print("__pycache__ directory deleted.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
