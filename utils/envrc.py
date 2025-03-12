import os


def update_envrc(cwd):
    """
    Updates the .envrc file with PPG_OUTPUT_FILE and PPG_JSON_OUTPUT_FILE variables.
    PPG_ENABLE_CLIPBOARD is only added if it doesn't already exist.
    """
    envrc_path = os.path.join(cwd, ".envrc")
    output_file_line = f'export PPG_OUTPUT_FILE="~/Downloads/$(basename $PWD).txt"\n'
    json_output_file_line = f'export PPG_JSON_OUTPUT_FILE="~/Downloads/$(basename $PWD).json.txt"\n'
    tree_json_output_file_line = f'export PPG_TREE_JSON_OUTPUT_FILE="~/Downloads/$(basename $PWD).tree.json.txt"\n'
    clipboard_enabled_line = 'export PPG_ENABLE_CLIPBOARD="false"\n'

    # Read existing .envrc
    existing_lines = []
    if os.path.exists(envrc_path):
        with open(envrc_path, "r") as f:
            existing_lines = f.readlines()

    # Normalize existing lines: strip whitespace and newlines
    existing_lines = [line.strip() for line in existing_lines]

    new_lines = []

    # Function to check if a variable is already defined (ignoring value)
    def is_variable_defined(variable_name, lines):
        for line in lines:
            if line.startswith(f'export {variable_name}='):
                return True
        return False

    if not is_variable_defined('PPG_OUTPUT_FILE', existing_lines):
        new_lines.append(output_file_line)
    if not is_variable_defined('PPG_JSON_OUTPUT_FILE', existing_lines):
        new_lines.append(json_output_file_line)
    if not is_variable_defined('PPG_TREE_JSON_OUTPUT_FILE', existing_lines):
        new_lines.append(tree_json_output_file_line)

    # Check if PPG_ENABLE_CLIPBOARD is defined, if not, append it
    if not is_variable_defined('PPG_ENABLE_CLIPBOARD', existing_lines):
        new_lines.append(clipboard_enabled_line)

    updated_variables = []
    if new_lines:
        if output_file_line in new_lines:
            updated_variables.append("PPG_OUTPUT_FILE")
        if json_output_file_line in new_lines:
            updated_variables.append("PPG_JSON_OUTPUT_FILE")
        if tree_json_output_file_line in new_lines:
            updated_variables.append("PPG_TREE_JSON_OUTPUT_FILE")
        if clipboard_enabled_line in new_lines:
            updated_variables.append("PPG_ENABLE_CLIPBOARD")

        # Append only new lines
        with open(envrc_path, "a") as f:
            f.writelines(new_lines)

        print(f"Updated {envrc_path} with " + ", ".join(updated_variables))
