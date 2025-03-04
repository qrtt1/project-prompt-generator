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
  ppg generate              # Generate a single all-in-one file (default)
  ppg generate --split      # Generate individual markdown files

Environment Variables:
  PPG_OUTPUT_DIR           # Custom output directory (default: ppg_generated, used with --split)
  PPG_OUTPUT_FILE          # Custom output filename (default: ppg_created_all.md.txt)
  PPG_IGNORE_FILES         # Comma-separated list of .gitignore files

For more information, visit: https://github.com/qrtt1/project-prompt-generator
"""
    )

    # Add common arguments
    parser.add_argument(
        "--no-mask",
        action="store_true",
        help="Disable sensitive data masking (default: enabled)"
    )

    # Add --split argument
    parser.add_argument(
        "--split",
        action="store_true",
        help="Generate individual markdown files instead of a single all-in-one file"
    )

    # Add aliases for generate command
    parser.add_argument(
        "command",
        nargs="?",
        choices=["generate", "g"],
        default="generate",
        help=argparse.SUPPRESS  # Hide from help message
    )

    # Parse arguments
    args = parser.parse_args()

    # Handle aliases
    if args.command == "g":
        args.command = "generate"

    # Show current environment configuration if requested
    output_dir = os.environ.get("PPG_OUTPUT_DIR", "ppg_generated")
    output_file = os.environ.get("PPG_OUTPUT_FILE", "ppg_created_all.md.txt")

    project_root = os.getcwd()
    ignore_spec = build_ignores(project_root)
    file_walker = FileWalker(project_root, ignore_spec)
    files_to_process = file_walker.get_files()

    no_mask = args.no_mask
    options = Options(no_mask=no_mask, output_dir=output_dir, output_file=output_file)

    if args.split:
        print(f"Using output directory: {output_dir}")
        output_handler = IndividualFilesOutputHandler(output_dir)
        generate(files_to_process, options, output_handler)
    else:
        print(f"Using output file: {output_file}")
        output_handler = SingleFileOutputHandler(output_file)
        generate(files_to_process, options, output_handler)


if __name__ == "__main__":
    cli()
