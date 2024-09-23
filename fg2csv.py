#!/usr/bin/env python3

import sys
import os
import csv
import FGBinTools

def print_usage():
    print("Usage: python fg2csv.py <input_fg> <output_csv>")
    print("  <input_fg>: Path to input FG file or directory containing FG files")
    print("  <output_csv>: Path to output CSV file or directory")

def process_fg(fg_file, csv_writer):
    if fg_file.endswith('.fg'):
        fgdata = FGBinTools.readFG(fg_file)
        filename = os.path.basename(fg_file)
        row = [filename[:-3], filename[12:-3], filename[6:11]] + fgdata['SS'] + fgdata['TS']
        csv_writer.writerow(row)

def main():
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if os.path.isdir(input_path):
        os.makedirs(output_path, exist_ok=True)
        output_file = os.path.join(output_path, 'faces.csv')
        with open(output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['Filename', 'Identity', 'Expression'] + [f'SS{i}' for i in range(50)] + [f'TS{i}' for i in range(50)])
            for filename in os.listdir(input_path):
                if filename.endswith('.fg'):
                    fg_file = os.path.join(input_path, filename)
                    process_fg(fg_file, csv_writer)
    else:
        with open(output_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['Filename', 'Identity', 'Expression'] + [f'SS{i}' for i in range(50)] + [f'TS{i}' for i in range(50)])
            process_fg(input_path, csv_writer)

    print("Done.")

if __name__ == "__main__":
    main()
