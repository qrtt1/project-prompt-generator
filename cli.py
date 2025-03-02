import argparse
import sys
import os
from prompts.generator import (
    generate_individual_files,
    generate_single_file,
)


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
        "--add-pattern": {
            "action": "append",
            "default": [],
            "metavar": "REGEX",
            "help": "Add custom regex patterns to mask sensitive data"
        }
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

    # Execute the appropriate command
    if not args.command:
        parser.print_help()
        return

    if args.command in ["generate", "g", "gen"]:
        print(f"Using output directory: {output_dir}")
        generate_individual_files(args.no_mask, args.add_pattern)
    elif args.command in ["generate_all_in_one", "a", "all"]:
        print(f"Using output file: {output_file}")
        generate_single_file(args.no_mask, args.add_pattern)


if __name__ == "__main__":
    cli()  # Changed from main() to cli()
