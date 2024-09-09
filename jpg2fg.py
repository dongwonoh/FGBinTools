## First, add facegen sdk into path (where fg* commands located e.g., ~sdk/bin/macos/x64/fg*)

import os
import subprocess

# Set directories
jpg_dir = "~"  # Directory containing JPG files
fg_dir = "~"    # Directory to store FG files

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



##### Script written by Anqi Mao (2024.09.07).