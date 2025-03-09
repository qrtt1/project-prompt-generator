# ✨ project-prompt-generator (ppg) 📝

A command-line tool to convert your project's files into structured markdown documents, ideal for generating prompts for large language models (LLMs) 🤖.

## Features 🌟

- **Flexible Output Options:** 🔀 Generate individual markdown files, a single consolidated file, or JSON output.
- **Automatic Markdown Conversion:** 🔄 Converts all project files (excluding those in `.gitignore`) into individual markdown files.
- **Structured Output:** 📂 Option to create an all-in-one file that includes an outline and the content of all converted files for easy use with LLMs.
- **Code Highlighting:** 🌈 Automatically detects file extensions and applies proper markdown code highlighting.
- **Customizable Ignored Files:** 🛡️ Respects `.gitignore` and supports additional custom ignore patterns.
- **Organized Output:** 📋 Generates an outline file that clearly lists all converted files.
- **Sensitive Data Masking:** 🔒 Automatically detects and masks API keys, passwords, and other sensitive information (enabled by default).
- **Event-Based Architecture:** 📡 Uses an event system to process files and handle output generation.
- **JSON Output Formats:** 📊 Supports both compact and line-split JSON formats for different use cases.

## Installation 🛠️

```bash
pip install .
```

## Usage 🚀

Navigate to your project's root directory and use the following command:

```bash
# Generate JSON output with content split into lines (default)
ppg

# Generate markdown output (compact format)
ppg --markdown

# Force execution outside of a git repository
ppg --force

# Update .envrc with output paths and exit
ppg --update-env
```

This creates either:

- A JSON file `project_data.json` in the current directory containing:
    - An outline of all processed files.
    - The content of all files converted to markdown format.

Or, when using `--markdown`:

- A single file `project_docs.md` in the current directory containing:
    - An outline listing all processed files.
    - The content of all files converted to markdown format.

Or, when using `--json` or `--json-lines`:

- A JSON file (default: `project_data.json`) containing:
    - An outline of all processed files
    - File contents in either:
        - Compact format (with `--json`): Content as single strings
        - Line-split format (with `--json-lines`): Content split into arrays of lines

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

You can customize the output locations using the `--update-env` option, which will automatically update your `.envrc` file with the appropriate environment variables:

```bash
# Update .envrc with default output paths
ppg --update-env
```

This will add the following environment variables to your `.envrc` file:
- `PPG_OUTPUT_FILE`: File for consolidated markdown output
- `PPG_JSON_OUTPUT_FILE`: File for JSON output

The paths will be automatically configured to use your Downloads directory with the current project name. You can then modify these paths in the `.envrc` file if needed.

Note: Make sure you have `direnv` installed and configured to use the `.envrc` file.

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
5. Depending on the command used, the tool generates either individual markdown files, a single consolidated file, or JSON output. 🧩

## License 📄

This project is licensed under the MIT License. 🎉
