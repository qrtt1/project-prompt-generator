# cli.py
import argparse
import os
import sys

from prompts.events import (EndEvent, FileProcessedEvent, OutlineCreatedEvent,
                            StartEvent)
from prompts.file_walker import FileWalker
from prompts.generator import generate
from prompts.ignore_handler import build_ignores
from prompts.options import Options
from prompts.output_handler import (IndividualFilesOutputHandler,
                                    SingleFileOutputHandler)


def cli():
    # Create the top-level parser with expanded help
    parser = argparse.ArgumentParser(
        description="""A CLI tool that converts project files into markdown for LLM prompts.

Project Prompt Generator (ppg) takes your codebase and creates nicely
formatted markdown files for large language models.""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ppg generate              # Generate individual markdown files
  ppg g                     # Same as above (shorthand)
  ppg generate --no-mask    # Generate files without masking sensitive data
  ppg all                   # Generate a single all-in-one file

Environment Variables:
  PPG_OUTPUT_DIR           # Custom output directory (default: ppg_generated)
  PPG_OUTPUT_FILE          # Custom output filename (default: ppg_created_all.md.txt)
  PPG_IGNORE_FILES         # Comma-separated list of .gitignore files

For more information, visit: https://github.com/qrtt1/project-prompt-generator
"""
    )

    # Create subparsers for commands
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Common arguments for all commands
    common_args = {
        "--no-mask": {
            "action": "store_true",
            "help": "Disable sensitive data masking (default: enabled)"
        },
    }

    # Add generate command
    generate_parser = subparsers.add_parser(
        "generate",
        aliases=["g", "gen"],
        help="Generate markdown files for each project file",
        description="""Generate individual markdown files for all project files,
respecting .gitignore rules. Output is in ppg_generated directory.

Output location can be customized with the PPG_OUTPUT_DIR environment variable.""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    for arg, config in common_args.items():
        generate_parser.add_argument(arg, **config)

    # Add generate_all_in_one command
    all_in_one_parser = subparsers.add_parser(
        "generate_all_in_one",
        aliases=["a", "all"],
        help="Generate a single markdown file with all project contents",
        description="""Generate one consolidated file with all project files converted to markdown.
Output is saved as ppg_created_all.md.txt in the current directory.

Output location can be customized with the PPG_OUTPUT_FILE environment variable.""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    for arg, config in common_args.items():
        all_in_one_parser.add_argument(arg, **config)

    # Parse arguments
    args = parser.parse_args()

    # Show current environment configuration if requested
    output_dir = os.environ.get("PPG_OUTPUT_DIR", "ppg_generated")
    output_file = os.environ.get("PPG_OUTPUT_FILE", "ppg_created_all.md.txt")

    project_root = os.getcwd()
    ignore_spec = build_ignores(project_root)
    file_walker = FileWalker(project_root, ignore_spec)
    files_to_process = file_walker.get_files()

    no_mask = getattr(args, 'no_mask', False)  # Get no_mask, default to False
    options = Options(no_mask=no_mask, output_dir=output_dir, output_file=output_file)

    if args.command in ["generate", "g", "gen"]:
        print(f"Using output directory: {output_dir}")
        output_handler = IndividualFilesOutputHandler(output_dir)
        generate(files_to_process, options, output_handler)
    elif args.command in ["generate_all_in_one", "a", "all"]:
        print(f"Using output file: {output_file}")
        output_handler = SingleFileOutputHandler(output_file)
        generate(files_to_process, options, output_handler)


if __name__ == "__main__":
    cli()
