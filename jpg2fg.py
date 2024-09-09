##### Script written by Anqi Mao (2024.09.07).

# This script converts JPG files to FG files using the FaceGen SDK.

# Usage: python fg2dea.py [img-dir] [fg-dir]
# [img-dir] is the directory containing the JPG images to convert.
# [fg-dir] is the directory where the FG files will be saved.

# Place this file (fg2dae.py) in the SDK bin folder alongside other FaceGen functions (fg3, fgbl, fg3pf);
# Alternatively, ensure that fg3 and fgbl are accessible from anywhere (i.e., added to the system PATH)
# or temporarily add them to the PATH if not already configured.

import os
import sys
import subprocess

def main():
    # Check if the correct number of arguments is passed
    if len(sys.argv) != 3:
        print("Usage: python fg2dea.py [img-dir] [fg_dir]")
        exit(1)

    # Get directories from command-line arguments
    jpg_dir = sys.argv[1]  # First argument: directory containing JPG files
    fg_dir = sys.argv[2]   # Second argument: directory to store FG files

    # Ensure directories exist
    if not os.path.exists(jpg_dir):
        print(f"Error: JPG directory {jpg_dir} does not exist.")
        exit(1)

    if not os.path.exists(fg_dir):
        os.makedirs(fg_dir)
        print(f"Created FG directory: {fg_dir}")

    # Iterate through all JPG files in the folder
    for jpg_file in os.listdir(jpg_dir):
        if jpg_file.endswith(".jpg"):
            base_name = os.path.splitext(jpg_file)[0]
            jpg_file_path = os.path.join(jpg_dir, jpg_file)
            fg_file_path = os.path.join(fg_dir, f"{base_name}.fg")
            lms_file_path = f"{jpg_file_path}.lms.txt"  # Expected landmark file

            # Step 1: Generate landmark file (only for frontal images)
            lms_command = ['fg3pf', 'lms', jpg_file_path]
            result_lms = subprocess.run(lms_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if result_lms.returncode != 0:
                print(f"Error generating landmarks for {jpg_file}: {result_lms.stderr.decode('utf-8')}")
                continue  # Skip to the next image if landmark generation fails

            # Step 2: Convert JPG to FG using the photofit command
            photofit_command = ['fg3pf', 'photofit', fg_file_path, jpg_file_path]
            result_photofit = subprocess.run(photofit_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if result_photofit.returncode == 0:
                print(f"Successfully converted {jpg_file} to {fg_file_path}")
            else:
                print(f"Error converting {jpg_file} to FG: {result_photofit.stderr.decode('utf-8')}")

if __name__ == "__main__":
    main()
