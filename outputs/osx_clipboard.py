import os
import subprocess
import platform


def ensure_clipboard_tool():
    clipboard_dir = os.path.expanduser("~/.ppg/bin")
    clipboard_exe = os.path.join(clipboard_dir, "clipboard")
    swift_source = os.path.join(clipboard_dir, "clipboard.swift")

    # If the clipboard executable does not exist, create the directory, generate the Swift source file, and compile it.
    if not os.path.exists(clipboard_exe):
        print("Clipboard tool not found. Automatically generating and compiling...")
        os.makedirs(clipboard_dir, exist_ok=True)

        # If the clipboard.swift file doesn't exist, generate it with default content.
        if not os.path.exists(swift_source):
            swift_code = '''import Cocoa

func copyFilePathToClipboardLegacy(filePath: String) {
    let pasteboard = NSPasteboard.general
    pasteboard.clearContents()

    // Define legacy type NSFilenamesPboardType
    let filenamesType = NSPasteboard.PasteboardType("NSFilenamesPboardType")

    pasteboard.declareTypes([filenamesType], owner: nil)
    pasteboard.setPropertyList([filePath], forType: filenamesType)
}

if CommandLine.arguments.count > 1 {
    let filePath = CommandLine.arguments[1]
    copyFilePathToClipboardLegacy(filePath: filePath)
} else {
    print("Please provide a file path as an argument")
}
'''
            with open(swift_source, "w") as f:
                f.write(swift_code)
            print("clipboard.swift file has been generated.")

        # Compile clipboard.swift to create the executable
        try:
            subprocess.run(["swiftc", swift_source, "-o", clipboard_exe], check=True)
            print("Compilation successful. Clipboard tool installed at ~/.ppg/bin")
        except subprocess.CalledProcessError as e:
            print("Failed to compile the clipboard tool:", e)
            return False
    return True


def osx_copy_to_clipboard(file_path):
    # Check if clipboard functionality is enabled via environment variable
    if os.environ.get("PPG_ENABLE_CLIPBOARD", "false").lower() != "true":
        return

    if platform.system() == "Darwin":
        if ensure_clipboard_tool():
            try:
                subprocess.run([os.path.expanduser("~/.ppg/bin/clipboard"), file_path], check=True)
                print(f"Copied to clipboard {file_path}")
            except subprocess.CalledProcessError as e:
                print("Error executing clipboard tool:", e)
        else:
            print("Unable to compile the clipboard tool automatically.")
    else:
        print("Clipboard copy functionality is currently supported only on macOS.")


# For testing: copy a specified file path to the clipboard
if __name__ == "__main__":
    import os

    test_path = os.path.abspath(__file__)
    os.environ["PPG_ENABLE_CLIPBOARD"] = "true"  # Enable for testing
    osx_copy_to_clipboard(test_path)
