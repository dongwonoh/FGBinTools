#!/usr/bin/env python3

# Script to convert csv to FaceGen face file (.fg)
# DongWon Oh (dongwonohphd@gmail.com) (National University of Singapore)
# original code by Ron Dotsch (rdotsch@gmail.com) circa 2017
#
# prerequisite: FaceGen Modeller SDK, FGBinTools
# 
# Last update: 22 Aug 2024
# - takes output path argument (default: current folder)
# - takes parameter length argument (default: 100)
# - deletes a cache directory at the end 
# - made Python-3 compatible (2023)
#
# prerequisite: FaceGen Modeller SDK, FGBinTools

import sys
import csv
import shutil
import os
from FGBinTools import writeFG

# For the 130 parameter-long csv: First column is the name of the fg file, the 50 coulumns after are the symmetric shape values, 30 asymmetric shape values, and 50 symmetric texture values.
# For the 100 parameter-long csv: First column is the name of the fg file, the 50 coulumns after are the symmetric shape values and 50 symmetric texture values.

def print_usage():
    print("Usage: python csv2fg.py <face_file.csv> [num_parameters] [output_path]")
    print("  <face_file.csv>: Path to the CSV file containing face data")
    print("  [num_parameters]: Optional. Number of parameters (130 or 100). Default is 100.")
    print("  [output_path]: Optional. Path where the output files will be saved. Default is current directory.")
    print("\nExample:")
    print("  python csv2fg.py faces.csv 130 ./output")

def process_csv(file_path, num_params=100, output_path="."):
    with open(file_path, 'r') as source:
        csv_reader = csv.reader(source)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            filename = os.path.join(output_path, row[0])
            if num_params == 130:
                writeFG(filename, 
                        SymShape=[int(i) for i in row[1:51]], 
                        ASymShape=[int(i) for i in row[51:81]], 
                        SymTexture=[int(i) for i in row[81:131]])
            elif num_params == 100:
                writeFG(filename, 
                        SymShape=[int(i) for i in row[1:51]], 
                        SymTexture=[int(i) for i in row[51:101]])
            else:
                raise ValueError(f"Invalid number of parameters: {num_params}")
    print("Done.")

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    face_file = sys.argv[1]
    num_params = 100 if len(sys.argv) < 3 or not sys.argv[2].isdigit() else int(sys.argv[2])
    output_path = "." if len(sys.argv) < 4 else sys.argv[3]

    if num_params not in [100, 130]:
        print(f"Error: Number of parameters must be 100 or 130. Got {num_params}")
        print_usage()
        sys.exit(1)

    try:
        process_csv(face_file, num_params, output_path)
        print("Conversion complete. Output saved to: " + output_path)
        # Attempt to delete __pycache__ directory
        shutil.rmtree('__pycache__', ignore_errors=True)
        print("__pycache__ directory deleted.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
