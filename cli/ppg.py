import argparse
import os
import sys

from prompts.events import (EndEvent, FileProcessedEvent, OutlineCreatedEvent, StartEvent)
from utils.file_walker import FileWalker
from prompts.generator import generate
from utils.ignore_handler import build_ignores
from utils.envrc_handler import update_envrc
from prompts.options import Options, OutputFormat, JSONFormat
from prompts.output_handler import (IndividualFilesOutputHandler, SingleFileOutputHandler,
                                    JSONOutputHandler, XMLOutputHandler)


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
  ppg              # Generate a single all-in-one file (default)
  ppg --split      # Generate individual markdown files
  ppg --force      # Force execution outside of a git repository
  ppg --json       # Generate JSON output (compact format)
  ppg --json-lines # Generate JSON output with content split into lines
  ppg --xml        # Generate XML output
  ppg --update-env # Update .envrc with output paths and exit

Environment Variables:
  PPG_OUTPUT_DIR           # Custom output directory (default: ppg_generated, used with --split)
  PPG_OUTPUT_FILE          # Custom output filename (default: project_docs.md)
  PPG_IGNORE_FILES         # Comma-separated list of .gitignore files
  PPG_JSON_OUTPUT_FILE     # Custom JSON output filename (default: project_data.json)

For more information, visit: https://github.com/qrtt1/project-prompt-generator
"""
    )

    # Add common arguments
    parser.add_argument(
        "--no-mask",
        action="store_true",
        help="Disable sensitive data masking (default: enabled)"
    )

    parser.add_argument(
        "--split",
        action="store_true",
        help="Generate individual markdown files instead of a single all-in-one file"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force execution outside of a git repository"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Generate JSON output instead of markdown"
    )

    parser.add_argument(
        "--json-lines",
        action="store_true",
        help="Generate JSON output with content split into lines"
    )

    parser.add_argument(
        "--xml",
        action="store_true",
        help="Generate XML output instead of markdown"  # 新增 XML 選項
    )

    parser.add_argument(
        "--update-env",
        action="store_true",
        help="Update .envrc with output paths and exit"
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
    output_dir = os.environ.get("PPG_OUTPUT_DIR", "ppg_generated")
    output_file = os.environ.get("PPG_OUTPUT_FILE", "project_docs.md")
    json_output_file = os.environ.get("PPG_JSON_OUTPUT_FILE", "project_data.json")
    xml_output_file = os.environ.get("PPG_XML_OUTPUT_FILE", "project_data.xml")  # 新增 XML 輸出檔案

    output_dir = os.path.expanduser(output_dir)
    output_file = os.path.expanduser(output_file)
    json_output_file = os.path.expanduser(json_output_file)
    xml_output_file = os.path.expanduser(xml_output_file)

    if args.split:
        output_path = os.path.abspath(output_dir)
    elif args.json or args.json_lines:
        output_path = os.path.abspath(json_output_file)
    elif args.xml:
        output_path = os.path.abspath(xml_output_file)
    else:
        output_path = os.path.abspath(output_file)

    print(f"Outputting to: {output_path}")

    project_root = os.getcwd()
    ignore_spec = build_ignores(project_root)
    file_walker = FileWalker(project_root, ignore_spec)
    files_to_process = file_walker.get_files()

    no_mask = args.no_mask
    options = Options(
        no_mask=no_mask,
        output_dir=output_dir,
        output_file=output_file,
        output_format=OutputFormat.XML if args.xml else (OutputFormat.JSON if (args.json or args.json_lines) else OutputFormat.MARKDOWN),
        json_output_file=json_output_file,
        json_format=JSONFormat.SPLIT if args.json_lines else JSONFormat.COMPACT,
        xml_output_file=xml_output_file
    )

    if args.split:
        output_handler = IndividualFilesOutputHandler(output_dir)
    elif args.json or args.json_lines:
        output_handler = JSONOutputHandler(json_output_file, options.json_format)
    elif args.xml:
        output_handler = XMLOutputHandler(xml_output_file)  # 使用 XML 輸出處理
    else:
        output_handler = SingleFileOutputHandler(output_file)

    generate(files_to_process, options, output_handler)


if __name__ == "__main__":
    cli()
