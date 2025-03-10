import os


def update_envrc(cwd):
    """
    Updates the .envrc file with PPG_OUTPUT_FILE and PPG_JSON_OUTPUT_FILE variables.
    """
    envrc_path = os.path.join(cwd, ".envrc")
    output_file_line = f'export PPG_OUTPUT_FILE="~/Downloads/$(basename $PWD).txt"\n'
    json_output_file_line = f'export PPG_JSON_OUTPUT_FILE="~/Downloads/$(basename $PWD).json"\n'

    # Read existing .envrc to avoid duplicates
    existing_lines = []
    if os.path.exists(envrc_path):
        with open(envrc_path, "r") as f:
            existing_lines = f.readlines()

    # Add/Update the lines in memory
    new_lines = []
    if not any(output_file_line in line for line in existing_lines):
        new_lines.append(output_file_line)
    if not any(json_output_file_line in line for line in existing_lines):
        new_lines.append(json_output_file_line)

    with open(envrc_path, "a") as f:
        f.writelines(new_lines)
    print(f"Updated {envrc_path} with PPG_OUTPUT_FILE and PPG_JSON_OUTPUT_FILE")
