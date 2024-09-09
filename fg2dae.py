## First, add facegen sdk into path (where fg* commands located e.g., ~sdk/bin/macos/x64/fg*)

import os
import subprocess

# Set directories
fg_dir = "~"   # Directory of FG files
dae_dir = "~" # Directory to store DAE files
headhires_path = "~sdk/data/csam/Animate/Head/HeadHires"

# Ensure directories exist
if not os.path.exists(fg_dir):
    print(f"Error: FG directory {fg_dir} does not exist.")
    exit(1)

if not os.path.exists(dae_dir):
    print(f"Error: DAE directory {dae_dir} does not exist.")
    exit(1)

if not os.path.exists(headhires_path):
    print(f"Error: HeadHires directory {headhires_path} does not exist.")
    exit(1)


# Iterate through all FG files in the folder
for fg_file in os.listdir(fg_dir):
    if fg_file.endswith(".fg"):
        base_name = os.path.splitext(fg_file)[0]
        fg_file_path = os.path.join(fg_dir, fg_file)

        # Step 1: Create mesh from FG file
        fgmesh_file = os.path.join(dae_dir, f"{base_name}.fgmesh")
        mesh_command = f"fg3 apply ssm {headhires_path} {fg_file_path} {fgmesh_file}"
        result_mesh = subprocess.run(mesh_command, shell=True)
        
        if result_mesh.returncode != 0:
            print(f"Error creating mesh for {fg_file}")
            continue  # Skip this file if there's an error

        # Step 2: Create color map
        output_jpg = os.path.join(dae_dir, f"{base_name}.jpg")
        color_map_command = f"fg3 apply scm {headhires_path} {fg_file_path} {output_jpg}"
        result_color_map = subprocess.run(color_map_command, shell=True)
        
        if result_color_map.returncode != 0:
            print(f"Error creating color map for {fg_file}")
            continue  # Skip this file if there's an error

        # Step 3: Convert to DAE
        dae_file = os.path.join(dae_dir, f"{base_name}.dae")
        dae_command = f"fgbl mesh export {dae_file} {fgmesh_file} {output_jpg}"
        result_dae = subprocess.run(dae_command, shell=True)

        if result_dae.returncode == 0:
            print(f"Successfully converted {fg_file} to {dae_file}")
        else:
            print(f"Error converting {fg_file} to {dae_file}")

##### Script written by Anqi Mao (2024.09.06).
