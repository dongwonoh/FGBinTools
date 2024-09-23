#!/usr/bin/env python3

import sys
import os
import csv
from FGBinTools import insertSlider
from LinAlgTools import normalize
from numpy import array

def print_usage():
    print("Usage: python csv2ctl.py <input_csv> <output_ctl> [controls_file]")
    print("  <input_csv>: Path to input CSV file or directory containing CSV files")
    print("  <output_ctl>: Path to output CTL file or directory")
    print("  [controls_file]: Optional. Path to file containing list of controls to convert")

def process_csv(csv_file, ctl_file, controls=None):
    with open(csv_file, 'r') as source, open(ctl_file, 'w') as ctlfile:
        csv_reader = csv.reader(source)
        header = next(csv_reader)
        
        for line in csv_reader:
            label = line[0]
            if controls and label not in controls:
                continue
            
            print(f"Processing: {label}")
            
            SS = normalize(array([float(i) for i in line[1:51]]))
            TS = normalize(array([float(i) for i in line[51:101]]))
            
            insertSlider(label, SS.tolist(), 'SS', ctlfile)
            insertSlider(label, TS.tolist(), 'TS', ctlfile)

def main():
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    controls_file = sys.argv[3] if len(sys.argv) > 3 else None

    controls = None
    if controls_file:
        with open(controls_file, 'r') as f:
            controls = [line.strip() for line in f]

    if os.path.isdir(input_path):
        os.makedirs(output_path, exist_ok=True)
        for filename in os.listdir(input_path):
            if filename.endswith('.csv'):
                csv_file = os.path.join(input_path, filename)
                ctl_file = os.path.join(output_path, filename.replace('.csv', '.ctl'))
                process_csv(csv_file, ctl_file, controls)
    else:
        process_csv(input_path, output_path, controls)

    print("Done.")

if __name__ == "__main__":
    main()
