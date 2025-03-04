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
  ppg              # Generate a single all-in-one file (default)
  ppg --split      # Generate individual markdown files

Environment Variables:
  PPG_OUTPUT_DIR           # Custom output directory (default: ppg_generated, used with --split)
  PPG_OUTPUT_FILE          # Custom output filename (default: project_docs.md)
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

    # Parse arguments
    args = parser.parse_args()

    # Determine output file and directory
    output_dir = os.environ.get("PPG_OUTPUT_DIR", "ppg_generated")
    output_file = os.environ.get("PPG_OUTPUT_FILE", "project_docs.md")

    if args.split:
        output_path = os.path.abspath(output_dir)
    else:
        output_path = os.path.abspath(output_file)

    print(f"Outputting to: {output_path}")

    project_root = os.getcwd()
    ignore_spec = build_ignores(project_root)
    file_walker = FileWalker(project_root, ignore_spec)
    files_to_process = file_walker.get_files()

    no_mask = args.no_mask
    options = Options(no_mask=no_mask, output_dir=output_dir, output_file=output_file)

    if args.split:
        output_handler = IndividualFilesOutputHandler(output_dir)
        generate(files_to_process, options, output_handler)
    else:
        output_handler = SingleFileOutputHandler(output_file)
        generate(files_to_process, options, output_handler)


if __name__ == "__main__":
    cli()
