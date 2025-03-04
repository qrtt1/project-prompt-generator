# last-run

A command-line tool to quickly run recently modified scripts in your Downloads directory.

## Features

*   **Lists Recent Scripts:** Displays the top 3 most recently modified `.sh` and `.py` scripts in your `~/Downloads` directory.
*   **Displays File Age:** Shows how long ago each script was modified (e.g., `01m30s`).
*   **Easy Execution:**  Run the first script by pressing Enter, choose a different script by entering its number (2 or 3), or quit by pressing any other key.
*   **Handles Permissions:** Automatically adds execute permissions to the script before running it.
*   **Handles Script Types:** Executes `.sh` scripts with `bash` and `.py` scripts with `python`.
*   **Graceful Exit:** Handles Ctrl+C (KeyboardInterrupt) to exit cleanly.

## Installation

`last-run` is installed as part of the `project-prompt-generator` package.  After installing or updating `project-prompt-generator`, you'll have access to the `last-run` command.

```bash
pip install -e .  # Install in editable mode (if developing)
# or
pip install project-prompt-generator # if install from pypi
```

## Usage

Simply run `last-run` from your terminal:

```bash
last-run
```

The tool will then display a list of recent scripts and prompt you to choose one to run.

## Example

```
Recent scripts in ~/Downloads: 📜
1.  01m15s | my_script.sh
2.  02m00s | another_script.py
3.  05m30s | utility.sh
Run script (Enter=1, 2/3, or other to quit): 🚀
```

*   Press **Enter** to run `my_script.sh`.
*   Type **2** and press Enter to run `another_script.py`.
*   Press any other key to quit without running a script.

## Error Handling

*   If no scripts are found in `~/Downloads`, the tool will display a "No scripts found" message.
*   If you enter an invalid choice (e.g., a number outside the range 1-3), the tool will display an "Invalid choice" message and quit.
*   The tool handles `KeyboardInterrupt` (Ctrl+C) gracefully, allowing you to exit cleanly.
*   If a file can't be found, the tool will display "Script not found".
