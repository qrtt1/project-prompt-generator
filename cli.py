import argparse
import os
import sys

from prompts.generator import generate_individual_files, generate_single_file
from prompts.output_formatters import get_output_formatter


def cli():
    # Create the top-level parser with expanded help
    parser = argparse.ArgumentParser(
        description="""A CLI tool that converts project files into various formats for LLM prompts.

Project Prompt Generator (ppg) takes your codebase and creates nicely
formatted files for large language models.""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Output Formats:
  - The tool supports pluggable output formats. The default is markdown.

Environment Variables:
  PPG_OUTPUT_DIR           # Custom output directory (default: ppg_generated)
  PPG_OUTPUT_FILE          # Custom output filename (default: ppg_created_all.md.txt)
  PPG_IGNORE_FILES         # Comma-separated list of .gitignore files

Examples:
  ppg generate --output-format markdown   # Generate individual markdown files
  ppg g -o markdown                     # Same as above (shorthand)
  ppg generate --no-mask                # Generate files without masking sensitive data
  ppg all -o text                       # Generate a single all-in-one text file

For more information, visit: https://github.com/qrtt1/project-prompt-generator
"""
    )

    # Create subparsers for commands
    subparsers = parser.add_subparsers(title="commands", dest="command",
                                     help="Commands to generate output files")

    # Common arguments for all commands
    common_args = {
        "--no-mask": {
            "action": "store_true",
            "help": "Disable sensitive data masking (default: enabled)"
        },
        "-o": {
            "dest": "output_format",
            "default": "markdown",
            "help": "Specify the output format (default: markdown)"
        },
        "--output-format": {
            "dest": "output_format",
            "default": "markdown",
            "help": "Specify the output format (default: markdown)"
        }
    }

    # Add generate command
    generate_parser = subparsers.add_parser(
        "generate",
        aliases=["g", "gen"],
        help="Generate individual files",
        description="""Generate files for all project files,
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
        help="Generate a single file with all project contents",
        description="""Generate one consolidated file with all project files.
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

    # Execute the appropriate command
    if not args.command:
        parser.print_help()
        return

    output_formatter = get_output_formatter(args.output_format)

    if args.command in ["generate", "g", "gen"]:
        print(f"Using output directory: {output_dir}")
        generate_individual_files(args.no_mask, output_formatter)
    elif args.command in ["generate_all_in_one", "a", "all"]:
        print(f"Using output file: {output_file}")
        generate_single_file(args.no_mask, output_formatter)


if __name__ == "__main__":
    cli()  # Changed from main() to cli()
