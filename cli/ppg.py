import argparse
import os
import sys

from outputs import JSONOutputHandler, SingleFileOutputHandler
from prompts.generator import generate
from prompts.options import JSONFormat, Options, OutputFormat
from utils.envrc import update_envrc
from utils.file_walker import FileWalker
from utils.ignore_handler import build_ignores


def is_git_repository(path):
    """
    Check if a directory or any of its parent directories contains a .git directory.
    """
    current_path = os.path.abspath(path)
    while current_path != os.path.dirname(current_path):  # Stop at the root directory
        if os.path.exists(os.path.join(current_path, ".git")):
            return True
        current_path = os.path.dirname(current_path)
    return False


def cli():
    # Create the top-level parser with expanded help
    parser = argparse.ArgumentParser(
        description="""A CLI tool that converts project files into markdown for LLM prompts.

Project Prompt Generator (ppg) takes your codebase and creates nicely
formatted markdown files for large language models.""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ppg              # Generate JSON output with content split into lines (default)
  ppg --markdown       # Generate markdown output (compact format)
  ppg --force      # Force execution outside of a git repository
  ppg --update-env # Update .envrc with output paths and exit

Environment Variables:
  PPG_OUTPUT_FILE          # Custom output filename (default: project_docs.md)
  PPG_IGNORE_FILES         # Comma-separated list of .gitignore files
  PPG_JSON_OUTPUT_FILE     # Custom JSON output filename (default: project_data.json)

For more information, visit: https://github.com/qrtt1/project-prompt-generator
""",
    )

    # Add common arguments
    parser.add_argument(
        "--no-mask",
        action="store_true",
        help="Disable sensitive data masking (default: enabled)",
    )

    # Add --force argument
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force execution outside of a git repository",
    )

    # Add --markdown argument
    parser.add_argument(
        "--markdown",
        action="store_true",
        dest="markdown",
        help="Generate markdown output (compact format)",
    )

    parser.add_argument(
        "--update-env",
        action="store_true",
        help="Update .envrc with output paths and exit",
    )

    # Parse arguments
    args = parser.parse_args()

    # If --update-env is used, just update .envrc and exit
    if args.update_env:
        update_envrc(os.getcwd())
        return

    # Check if it's a git repo
    if not args.force and not is_git_repository(os.getcwd()):
        print("Error: Not a git repository. Use --force to run anyway.")
        sys.exit(1)

    # Determine output file and directory
    output_file = os.environ.get("PPG_OUTPUT_FILE", "project_docs.md")
    json_output_file = os.environ.get("PPG_JSON_OUTPUT_FILE", "project_data.json")

    # Expand ~ to user's home directory
    output_file = os.path.expanduser(output_file)
    json_output_file = os.path.expanduser(json_output_file)

    if args.markdown:
        output_path = os.path.abspath(output_file)
    else:
        output_path = os.path.abspath(json_output_file)

    print(f"Outputting to: {output_path}")

    project_root = os.getcwd()
    ignore_spec = build_ignores(project_root)
    file_walker = FileWalker(project_root, ignore_spec)
    files_to_process = file_walker.get_files()

    no_mask = args.no_mask
    options = Options(
        no_mask=no_mask,
        output_file=output_file,
        output_format=OutputFormat.MARKDOWN if args.markdown else OutputFormat.JSON,
        json_output_file=json_output_file,
        json_format=JSONFormat.COMPACT if args.markdown else JSONFormat.SPLIT,
    )

    if args.markdown:
        output_handler = SingleFileOutputHandler(output_file)
    else:
        output_handler = JSONOutputHandler(json_output_file, options.json_format)

    generate(files_to_process, options, output_handler)


if __name__ == "__main__":
    cli()
