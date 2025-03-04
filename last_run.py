import os
import glob
import subprocess
import stat
import time
import sys

def main():
    """
    Finds the most recently modified .sh or .py scripts in ~/Downloads,
    lists the top 3, and allows the user to execute one.
    """
    downloads_dir = os.path.expanduser("~/Downloads")
    scripts = glob.glob(os.path.join(downloads_dir, "*.sh")) + glob.glob(os.path.join(downloads_dir, "*.py"))

    if not scripts:
        print("No scripts found in ~/Downloads. 😢")
        return

    # Sort scripts by modification time (newest first)
    scripts.sort(key=os.path.getmtime, reverse=True)

    print("Recent scripts in ~/Downloads: 📜")
    for i, script in enumerate(scripts[:3]):
        file_age = int(time.time() - os.path.getmtime(script))
        minutes = file_age // 60
        seconds = file_age % 60
        age_str = f"{minutes:2}m{seconds:2}s"  # Format with leading zeros and fixed width

        filename = os.path.basename(script)
        print(f"{i+1}. {age_str} | {filename}") # Time before Filename and remove the filename width

    try:
        choice = input("Run script (Enter=1, 2/3, or other to quit): 🚀 ")
    except KeyboardInterrupt:
        print("\\nExiting. 👋")
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
        # Add execute permissions to the script
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
