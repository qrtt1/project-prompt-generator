# ✨ project-prompt-generator (ppg) 📝

A command-line tool to convert your project's files into structured markdown documents, ideal for generating prompts for large language models (LLMs) 🤖.

## Features 🌟

- **Flexible Output Options:** 🔀 Generate individual markdown files or a single consolidated file.
- **Automatic Markdown Conversion:** 🔄 Converts all project files (excluding those in `.gitignore`) into individual markdown files.
- **Structured Output:** 📂 Option to create an all-in-one file that includes an outline and the content of all converted files for easy use with LLMs.
- **Code Highlighting:** 🌈 Automatically detects file extensions and applies proper markdown code highlighting.
- **Customizable Ignored Files:** 🛡️ Respects `.gitignore` and supports additional custom ignore patterns.
- **Organized Output:** 📋 Generates an outline file that clearly lists all converted files.
- **Sensitive Data Masking:** 🔒 Automatically detects and masks API keys, passwords, and other sensitive information (enabled by default).
- **Event-Based Architecture:** 📡 Uses an event system to process files and handle output generation.

## Installation 🛠️

```bash
pip install .
```

## Usage 🚀

Navigate to your project's root directory and use the following command:

```bash
# Generate a single all-in-one file (default)
ppg

# Generate individual markdown files
ppg --split
```

This creates either:

- A single file `ppg_created_all.md.txt` in the current directory containing:
    - An outline listing all processed files.
    - The content of all files converted to markdown format.

Or, when using `--split`:

- A `ppg_generated` directory containing:
    - Individual markdown files for each project file with a sequential numbering system (e.g., `001_cli.py.md`, `002_README.md.md`, etc.).
    - Each file includes both the original filename and its relative path in the project.

### Security Options

The tool automatically masks sensitive data by default. You can control this behavior with:

```bash
# Disable sensitive data masking
ppg --no-mask
```

Default patterns detect common sensitive information like:

- API keys and tokens
- Passwords
- Database connection strings
- AWS access keys
- Generic secrets
- PowerShell secure strings

## Environment Variable Configuration 🔧

You can customize the output locations and ignored files using environment variables:

```bash
# Change the output directory (default: ppg_generated, used with --split)
export PPG_OUTPUT_DIR=custom_output_folder
ppg --split

# Change the all-in-one output file name (default: project_docs.md)
export PPG_OUTPUT_FILE=project_documentation.md
ppg

# Define custom ignore files (comma-separated)
export PPG_IGNORE_FILES=".gitignore,.dockerignore"
ppg
```

Advanced path features:

```bash
# Use home directory paths with ~
export PPG_OUTPUT_DIR=~/documents/project_docs
export PPG_OUTPUT_FILE=~/documents/project_docs/full_docs.md

# Use shell environment variables
export PPG_OUTPUT_DIR=$HOME/documents/project_docs
export PPG_OUTPUT_FILE=${HOME}/documents/project_docs/full_docs.md

# Use absolute paths
export PPG_OUTPUT_DIR=/var/www/docs/project
export PPG_OUTPUT_FILE=/shared/documents/project_output.md

# Use nested paths that don't exist yet (directories will be created automatically)
export PPG_OUTPUT_DIR=docs/markdown/generated
export PPG_OUTPUT_FILE=reports/2025/q1/project_report.md
```

## Project Structure 📁

```
project-prompt-generator/
├── cli.py                     # Command-line interface
├── prompts/
│   ├── __init__.py            # Package exports
│   ├── events.py              # Event classes for file processing
│   ├── file_processor.py      # File processing utilities
│   ├── file_walker.py         # Directory traversal and file filtering
│   ├── generator.py           # Core generation functionality
│   ├── ignore_handler.py      # Handles .gitignore and custom ignores
│   ├── language_mapping.py    # Maps file extensions to language hints
│   ├── options.py             # Configuration options
│   ├── output_handler.py      # Output handling for files/all-in-one
│   └── sensitive_masker.py    # Sensitive data masking
├── tests/
│   └── test_sensitive_masker.py  # Tests for sensitive data masking
├── setup.py                   # Package configuration
└── README.md                  # Documentation
```

## How it Works ⚙️

1. The tool scans your project directory, respecting `.gitignore` and any custom ignore patterns. 🔍
2. Each file is converted into a markdown format with a header showing the filename and path, followed by its content enclosed in a code block with appropriate language highlighting. 📝
3. An event-based system handles file processing and output generation, making the code extensible. 🔄
4. Sensitive data is automatically detected and masked with asterisks (*) to protect your credentials. 🔒
5. Depending on the command used, the tool generates either individual markdown files or a single consolidated file. 🧩

## License 📄

This project is licensed under the MIT License. 🎉
