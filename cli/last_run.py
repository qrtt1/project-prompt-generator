#!/usr/bin/env python3
import argparse
import glob
import os
import platform
import stat
import subprocess
import sys
import time


def main():
    """
    Finds the most recently modified .sh or .py scripts in ~/Downloads,
    lists the top 3 (or fewer), and allows the user to execute one.
    Ignores files older than 10 minutes by default.
    """
    parser = argparse.ArgumentParser(
        description="""
        Finds and runs recently modified scripts in ~/Downloads.
        Ignores files older than 10 minutes by default.
        """
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Show all scripts, regardless of age.",
    )
    args = parser.parse_args()

    downloads_dir = os.path.expanduser("~/Downloads")
    scripts = glob.glob(os.path.join(downloads_dir, "*.sh")) + glob.glob(
        os.path.join(downloads_dir, "*.py")
    )

    if not scripts:
        print("No scripts found in ~/Downloads. 😢")
        return

    # Sort scripts by modification time (newest first)
    scripts.sort(key=os.path.getmtime, reverse=True)

    # Filter out scripts older than 10 minutes, unless --all is specified
    if not args.all:
        cutoff_time = time.time() - (10 * 60)  # 10 minutes in seconds
        scripts = [s for s in scripts if os.path.getmtime(s) > cutoff_time]

    if not scripts:
        print("No recent scripts found in ~/Downloads (last 10 minutes). 😢")
        return

    print("Recent scripts in ~/Downloads: 📜")
    for i, script in enumerate(scripts[:3]):
        file_age = int(time.time() - os.path.getmtime(script))
        minutes = file_age // 60
        seconds = file_age % 60
        age_str = f"{minutes:2}m{seconds:2}s"

        filename = os.path.basename(script)
        print(f"{i + 1}. {age_str} | {filename}")

    # Add option to create script from clipboard content on macOS
    if platform.system() == "Darwin":
        print("c. Create script from clipboard (macOS only) 📝")

    try:
        if platform.system() == "Darwin":
            choice = input("Run script (Enter=1, 2/3, c to create, or other to quit): 🚀 ")
        else:
            choice = input("Run script (Enter=1, 2/3, or other to quit): 🚀 ")
    except KeyboardInterrupt:
        print("\nExiting. 👋")
        return

    # Handle clipboard script creation on macOS
    if platform.system() == "Darwin" and choice.lower() == "c":
        try:
            # Get clipboard content using pbpaste
            clipboard_content = subprocess.check_output(['pbpaste']).decode('utf-8')

            # Improved script type detection
            def detect_script_type(content):
                """
                Detect script type more comprehensively based on shebang and content features
                Returns a tuple of (extension, prefix)
                """
                # Remove potential leading whitespace
                clean_content = content.lstrip()

                # Check for shebang (common variants)
                python_shebangs = [
                    '#!/usr/bin/env python',
                    '#!/usr/bin/python',
                    '#!/bin/python',
                    '#! /usr/bin/env python',
                    '#! /usr/bin/python',
                    '#!/usr/local/bin/python'
                ]

                shell_shebangs = [
                    '#!/bin/bash',
                    '#!/bin/sh',
                    '#!/usr/bin/env bash',
                    '#!/usr/bin/env sh',
                    '#! /bin/bash',
                    '#! /bin/sh',
                    '#!/usr/bin/bash'
                ]

                # Check for shebang
                for shebang in python_shebangs:
                    if clean_content.startswith(shebang):
                        return ".py", "python"

                for shebang in shell_shebangs:
                    if clean_content.startswith(shebang):
                        return ".sh", "bash"

                # Detect based on content features
                python_indicators = ['import ', 'def ', 'class ', 'print(', '    ', 'if __name__ == "__main__":', '"""',
                                     "'''"]
                shell_indicators = ['function ', 'export ', 'echo ', 'if [ ', 'for i in', 'while ', '#!/', 'case ',
                                    'esac', '$', '${']

                python_score = sum(1 for ind in python_indicators if ind in clean_content)
                shell_score = sum(1 for ind in shell_indicators if ind in clean_content)

                return (".py", "python") if python_score > shell_score else (".sh", "bash")

            script_extension, script_prefix = detect_script_type(clipboard_content)

            # Ensure shell scripts have a shebang (if they don't already)
            if script_extension == ".sh" and not any(clipboard_content.lstrip().startswith(s) for s in shell_shebangs):
                clipboard_content = "#!/bin/bash\n\n" + clipboard_content

            # Allow user to override if Python was detected
            if script_extension == ".py":
                print(f"Python script detected. Press Enter to confirm, or type 'sh' to force Shell script:")
                force_type = input()
                if force_type.lower() == 'sh':
                    script_extension = ".sh"
                    script_prefix = "bash"

            # Create a temporary file
            temp_script_name = f"/tmp/temp_script_{int(time.time())}{script_extension}"
            with open(temp_script_name, "w") as temp_script_file:
                temp_script_file.write(clipboard_content)

            # Make the script executable
            os.chmod(temp_script_name, os.stat(temp_script_name).st_mode | stat.S_IEXEC)

            print(f"Running script from clipboard: {os.path.basename(temp_script_name)} 🏃‍♂️")

            # Run the script
            subprocess.run([script_prefix, temp_script_name], check=True)

        except subprocess.CalledProcessError as e:
            print(f"Error running script: {e} 💥")
        except FileNotFoundError:
            print("Script not found. 😓")
        except OSError as e:
            print(f"Error changing permissions: {e} 🔑")
        except Exception as e:
            print(f"Error creating or running script from clipboard: {e} 😕")
        return

    if choice == "":
        script_to_run = scripts[0]
    else:
        try:
            index = int(choice) - 1
            if 0 <= index < len(scripts[:3]):
                script_to_run = scripts[index]
            else:
                print("Invalid choice. ❌")
                return
        except ValueError:
            print("Exiting. 👋")
            return

    try:
        os.chmod(script_to_run, os.stat(script_to_run).st_mode | stat.S_IEXEC)

        print(f"Running: {os.path.basename(script_to_run)} 🏃‍♂️")

        if script_to_run.endswith(".sh"):
            subprocess.run(["bash", script_to_run], check=True)
        elif script_to_run.endswith(".py"):
            subprocess.run(["python", script_to_run], check=True)
        else:
            print("Unsupported script type. 😕")
            return

    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e} 💥")
    except FileNotFoundError:
        print("Script not found. 😓")
    except OSError as e:
        print(f"Error changing permissions: {e} 🔑")


if __name__ == "__main__":
    main()
