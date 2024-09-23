#!/usr/bin/env python3

import sys
import os
import csv
import FGBinTools

def print_usage():
    print("Usage: python ctl2csv.py <input_ctl> <output_csv> [controls_file]")
    print("  <input_ctl>: Path to input CTL file or directory containing CTL files")
    print("  <output_csv>: Path to output CSV file or directory")
    print("  [controls_file]: Optional. Path to file containing list of controls to convert")

def process_ctl(ctl_file, csv_file, controls=None):
    print(f"Loading control vectors from {ctl_file}...")

    ctl = FGBinTools.readCtl(ctl_file)

    controlshapevec = {}
    controltexvec = {}

    for label, vector in ctl['GS']:
        if not controls or label in controls:
            print(f"+ Found: shape {label}")
            controlshapevec[label] = vector

    for label, vector in ctl['TS']:
        if not controls or label in controls:
            print(f"+ Found: texture {label}")
            controltexvec[label] = vector

    with open(csv_file, 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for label in sorted(controltexvec.keys()):
            row = [label] + controlshapevec[label] + controltexvec[label]
            csvWriter.writerow(row)

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
            if filename.endswith('.ctl'):
                ctl_file = os.path.join(input_path, filename)
                csv_file = os.path.join(output_path, filename.replace('.ctl', '.csv'))
                process_ctl(ctl_file, csv_file, controls)
    else:
        process_ctl(input_path, output_path, controls)

    print("Done.")

if __name__ == "__main__":
    main()
