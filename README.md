# ✨ prompt-generator (promg) 📝

A command-line tool to convert your project's files into structured markdown documents, ideal for generating prompts for
large language models (LLMs) 🤖.

## Features 🌟

- **Automatic Markdown Conversion:** 🔄 Converts all project files (excluding those in `.gitignore`) into individual
  markdown files.
- **Structured Output:** 📂 Generates a comprehensive `000_all.md` file containing an outline and the content of all
  converted files, making it easy to feed into LLMs.
- **Code Highlighting:** 🌈 Automatically detects file extensions and applies appropriate markdown code highlighting.
- **Customizable Ignored Files:** 🛡️ Respects `.gitignore` and includes additional custom ignore patterns.
- **Organized Output:** 📋 Generates an `000_outline.md` file to provide a clear overview of all converted files.
- **Sensitive Data Masking:** 🔒 Automatically detects and masks API keys, passwords, and other sensitive information (
  enabled by default).

## Installation 🛠️

```bash
pip install .
```

## Usage 🚀

Navigate to your project's root directory and run:

```bash
promg gen
```

This will create a `.ppg_generated` directory containing:

- `000_all.md`: 📚 A single markdown file with the content of all project files.
- `000_outline.md`: 🗺️ A table of contents for all generated markdown files.
- Individual markdown files for each project file (e.g., `001_cli.py.md`, `002_README.md`, etc.).

### Security Options

The tool automatically masks sensitive data by default. You can control this behavior with:

```bash
# Disable sensitive data masking
promg gen --no-mask

# Add custom patterns for sensitive data detection
promg gen --add-pattern "your_custom_regex_pattern"
```

Default patterns will detect common sensitive information like:

- API keys and tokens
- Passwords
- Database connection strings
- AWS access keys
- Generic secrets

## Example Output Structure 🌳

```
.ppg_generated/
├── 000_all.md
├── 000_outline.md
├── 001_.gitignore.md
├── 002_cli.py.md
├── 003_prompts___init__.py.md
└── 004_setup.py.md
```

## How it Works ⚙️

1. The tool scans your project directory, respecting `.gitignore` and custom ignore patterns. 🔍
2. Each file is converted into a markdown file with a header containing the filename and path, followed by the file's
   content enclosed in a code block with appropriate language highlighting. 📝
3. Sensitive data in the content is automatically detected and masked with asterisks (*) to protect security
   credentials. 🔒
4. An outline file (`000_outline.md`) is generated, listing all converted files. 📃
5. Finally, `000_all.md` is created by concatenating the outline and the content of all individual markdown files. 🧩

## License 📄

This project is licensed under the MIT License. 🎉