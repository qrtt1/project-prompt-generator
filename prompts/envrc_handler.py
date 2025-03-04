
import os

def update_envrc(cwd):
    """
    Updates the .envrc file with PPG_OUTPUT_FILE and PPG_OUTPUT_DIR variables.
    """
    envrc_path = os.path.join(cwd, ".envrc")
    output_file_line = f'export PPG_OUTPUT_FILE="~/Downloads/$(basename $PWD).txt"\n'
    output_dir_line = f'export PPG_OUTPUT_DIR="~/Downloads/$(basename $PWD)"\n'

    # Read existing .envrc to avoid duplicates
    existing_lines = []
    if os.path.exists(envrc_path):
        with open(envrc_path, "r") as f:
            existing_lines = f.readlines()

    # Add/Update the lines in memory
    new_lines = []
    if not any(output_file_line in line for line in existing_lines):
        new_lines.append(output_file_line)
    if not any(output_dir_line in line for line in existing_lines):
        new_lines.append(output_dir_line)

    with open(envrc_path, "a") as f:
        f.writelines(new_lines)
    print(f"Updated {envrc_path} with PPG_OUTPUT_FILE and PPG_OUTPUT_DIR")
