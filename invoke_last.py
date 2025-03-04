import glob
import os
import stat
import subprocess


def main():
    """
    Finds the most recently modified .sh or .py scripts in ~/Downloads,
    lists the top 3, and allows the user to execute one.
    """
    downloads_dir = os.path.expanduser("~/Downloads")
    scripts = glob.glob(os.path.join(downloads_dir, "*.sh")) + glob.glob(os.path.join(downloads_dir, "*.py"))

    if not scripts:
        print("No shell or python scripts found in ~/Downloads.")
        return

    # Sort scripts by modification time (newest first)
    scripts.sort(key=os.path.getmtime, reverse=True)

    print("Most recently modified scripts in ~/Downloads:")
    for i, script in enumerate(scripts[:3]):
        print(f"{i+1}. {os.path.basename(script)}")

    choice = input("Press Enter to run the first script, enter a number to choose another, or any other key to quit: ")

    if choice == "":
        script_to_run = scripts[0]
    else:
        try:
            index = int(choice) - 1
            if 0 <= index < len(scripts[:3]):
                script_to_run = scripts[index]
            else:
                print("Invalid choice.")
                return
        except ValueError:
            print("Exiting.")
            return

    try:
        # Add execute permissions to the script
        os.chmod(script_to_run, os.stat(script_to_run).st_mode | stat.S_IEXEC)

        print(f"Running: {os.path.basename(script_to_run)}")
        subprocess.run([script_to_run], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")
    except FileNotFoundError:
        print("Script not found.")
    except OSError as e:
        print(f"Error changing permissions: {e}")


if __name__ == "__main__":
    main()