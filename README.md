# ✨ project-prompt-generator (ppg) 📝

A command-line tool to convert your project's files into structured markdown documents, ideal for generating prompts for
large language models (LLMs) 🤖.

## Features 🌟

- **Flexible Output Options:** 🔀 Generate individual markdown files or a single consolidated file.
- **Automatic Markdown Conversion:** 🔄 Converts all project files (excluding those in `.gitignore`) into individual
  markdown files.
- **Structured Output:** 📂 Optional creation of a comprehensive all-in-one file containing an outline and the content of all
  converted files, making it easy to feed into LLMs.
- **Code Highlighting:** 🌈 Automatically detects file extensions and applies appropriate markdown code highlighting.
- **Customizable Ignored Files:** 🛡️ Respects `.gitignore` and includes additional custom ignore patterns.
- **Organized Output:** 📋 Generates an outline file to provide a clear overview of all converted files.
- **Sensitive Data Masking:** 🔒 Automatically detects and masks API keys, passwords, and other sensitive information (
  enabled by default).
- **Modular Architecture:** 🧩 Easy to extend with new features and functionality.

## Installation 🛠️

```bash
pip install .
```

## Usage 🚀

Navigate to your project's root directory and use one of the following commands:

### Generate Individual Markdown Files

```bash
ppg generate
```

This creates a `ppg_generated` directory containing:
- `000_outline.md`: 🗺️ A table of contents for all generated markdown files.
- Individual markdown files for each project file (e.g., `001_cli.py.md`, `002_README.md`, etc.).

### Generate a Single All-in-One File

```bash
ppg generate_all_in_one
```

This creates a single file `ppg_created_all.md.txt` in the current directory containing:
- An outline listing all processed files.
- The content of all files converted to markdown format.

### Legacy Command (Backward Compatibility)

```bash
ppg gen
```

The original command that combines both functionalities above. Creates a `ppg_generated` directory with individual files plus an `000_all.md` combined file. This command is maintained for backward compatibility.

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

1. The tool scans your project directory, respecting `.gitignore` and custom ignore patterns. 🔍
2. Each file is converted into a markdown file with a header containing the filename and path, followed by the file's
   content enclosed in a code block with appropriate language highlighting. 📝
3. Sensitive data in the content is automatically detected and masked with asterisks (*) to protect security
   credentials. 🔒
4. Depending on the command used, the tool either generates individual files or a single combined file. 🧩

## License 📄

This project is licensed under the MIT License. 🎉