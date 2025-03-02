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

## Installation 🛠️

```bash
pip install .
```

## Usage 🚀

Navigate to your project's root directory and use one of the following commands:

### Generate Individual Markdown Files

```bash
# Full command
ppg generate

# Aliases
ppg g
ppg gen
```

This creates a `ppg_generated` directory containing:

- `000_outline.md`: 🗺️ A table of contents for all generated markdown files.
- Individual markdown files for each project file (e.g., `001_cli.py.md`, `002_README.md`, etc.).

### Generate a Single All-in-One File

```bash
# Full command
ppg generate_all_in_one

# Aliases
ppg a
ppg all
```

This creates a single file `ppg_created_all.md.txt` in the current directory containing:

- An outline listing all processed files.
- The content of all files converted to markdown format.

### Security Options

The tool automatically masks sensitive data by default. You can control this behavior with:

```bash
# Disable sensitive data masking
ppg generate --no-mask

# Add custom patterns for sensitive data detection
ppg generate --add-pattern "your_custom_regex_pattern"
```

Default patterns will detect common sensitive information like:

- API keys and tokens
- Passwords
- Database connection strings
- AWS access keys
- Generic secrets

## Example Output Structure 🌳

### When using `ppg generate`:

```
ppg_generated/
├── 000_outline.md
├── 001_.gitignore.md
├── 002_cli.py.md
├── 003_prompts___init__.py.md
└── 004_setup.py.md
```

### When using `ppg generate_all_in_one`:

```
./ppg_created_all.md.txt
```

### Environment Variable Configuration 🔧

You can customize the output locations and ignored directories using environment variables:

```bash
# Change the output directory (default: ppg_generated)
export PPG_OUTPUT_DIR=custom_output_folder
ppg generate

# Change the all-in-one output file name (default: ppg_created_all.md.txt)
export PPG_OUTPUT_FILE=project_documentation.md
ppg all

# Define custom directories to ignore (comma-separated)
export CUSTOM_IGNORE_DIRS="dir1,dir2,dir3"
ppg generate

# Use all together
export PPG_OUTPUT_DIR=docs
export PPG_OUTPUT_FILE=full_project.md
export CUSTOM_IGNORE_DIRS="temp,cache"
ppg all
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

These environment variables provide flexibility for:

- Integration with automated workflows 🤖
- Customizing output for different projects 📂
- Directing output to specific documentation folders 📚
- Ignoring specific directories from prompt generation 🙈

## Project Structure 📁

```
project-prompt-generator/
├── cli.py                     # Command-line interface
├── prompts/
│   ├── __init__.py            # Package exports
│   ├── generator.py           # Core generation functionality
│   ├── file_processor.py      # File processing utilities
│   └── sensitive_masker.py    # Sensitive data masking
├── setup.py                   # Package configuration
└── README.md                  # Documentation
```

## How it Works ⚙️

1. The tool scans your project directory, respecting `.gitignore` and any custom ignore patterns specified via the `CUSTOM_IGNORE_DIRS` environment variable. 🔍
2. Each file is converted into a markdown file with a header showing the filename and path, followed by its content enclosed in a code block with appropriate language highlighting. 📝
3. Sensitive data is automatically detected and masked with asterisks (*) to protect your credentials. 🔒
4. Depending on the command used, the tool generates either individual markdown files or a single consolidated file. 🧩

## License 📄

This project is licensed under the MIT License. 🎉

---

## Additional Notes

- This is a simple, experimental project created to assist with daily tasks.
- If you need a more mature solution, consider exploring [Repomix](https://repomix.com/).
- We intend to learn from Repomix's features and may integrate new ideas in future updates.
