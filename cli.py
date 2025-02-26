import os
import shutil
import click
import pathspec

from prompts.sensitive_masker import SensitiveMasker, DEFAULT_SENSITIVE_PATTERNS

OUTPUT_DIR = ".ppg_generated"

# Mapping file extensions to markdown language hints
EXTENSION_MAPPING = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.html': 'html',
    '.css': 'css',
    '.json': 'json',
    '.sh': 'bash',
    '.java': 'java',
    '.c': 'c',
    '.cpp': 'cpp',
    '.rb': 'ruby',
    '.php': 'php',
    '.go': 'go'
}


@click.group()
def cli():
    """A CLI tool that converts project files (excluding those in .gitignore) into markdown."""
    pass


@cli.command()
@click.option('--no-mask', is_flag=True, help='Disable sensitive data masking.')
@click.option('--add-pattern', multiple=True, help='Add custom regex patterns to mask sensitive data.')
def gen(no_mask, add_pattern):
    """Generate markdown files for all project files (recursively) excluding ignored ones,
    then combine all generated markdown content into 000_all.md."""
    # Define the project root as the current working directory.
    project_root = os.getcwd()

    # Remove the output directory if it exists and recreate it.
    output_dir_path = os.path.join(project_root, OUTPUT_DIR)
    if os.path.exists(output_dir_path):
        shutil.rmtree(output_dir_path)
    os.makedirs(output_dir_path)

    # Load .gitignore patterns if the file exists.
    gitignore_path = os.path.join(project_root, ".gitignore")
    ignore_spec = None
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            gitignore_lines = f.read().splitlines()
        ignore_spec = pathspec.PathSpec.from_lines("gitwildmatch", gitignore_lines)

    # Additional custom ignore patterns for directories.
    custom_ignore_dirs = {'promg.egg-info', 'venv', 'env', 'build', 'dist'}

    # Walk through the project directory and gather files.
    files_to_process = []
    for root, dirs, files in os.walk(project_root):
        rel_root = os.path.relpath(root, project_root)
        # Skip the output directory.
        if rel_root.startswith(OUTPUT_DIR):
            continue
        # Remove directories that you don't want to traverse.
        dirs[:] = [d for d in dirs if d not in custom_ignore_dirs and d != ".git"]
        for file in files:
            file_full_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_full_path, project_root)
            # Skip files ignored by .gitignore.
            if ignore_spec and ignore_spec.match_file(rel_path):
                continue
            files_to_process.append(file_full_path)

    # Sort files for a consistent sequence order.
    files_to_process.sort(key=lambda p: os.path.relpath(p, project_root))

    markdown_files_info = []
    seq_counter = 1

    # Setup sensitive data masker by default, unless disabled
    masker = None
    if not no_mask or add_pattern:
        # Initialize masker with default patterns if masking is enabled
        patterns = DEFAULT_SENSITIVE_PATTERNS.copy() if not no_mask else []
        masker = SensitiveMasker(patterns)

        # Add any custom patterns
        for pattern in add_pattern:
            masker.add_pattern(pattern)

        if not no_mask:
            click.echo("Sensitive data masking is enabled (use --no-mask to disable)")

    # Convert each file into a markdown file.
    for file_full_path in files_to_process:
        rel_path = os.path.relpath(file_full_path, project_root)
        # Generate a flat version of the relative path by replacing directory separators with underscores.
        flat_rel_path = rel_path.replace(os.path.sep, "_")
        try:
            with open(file_full_path, "r", encoding="utf-8") as f:
                file_content = f.read()
        except Exception as e:
            click.echo(f"Skipping {rel_path}: {e}")
            continue

        # Mask sensitive data by default unless disabled
        if masker and not no_mask:
            file_content = masker.mask_content(file_content)

        # Determine language hint based on file extension.
        _, ext = os.path.splitext(file_full_path)
        lang = EXTENSION_MAPPING.get(ext.lower(), '')
        code_block_start = f"```{lang}\n" if lang else "```\n"

        markdown_content = (
            "## file description\n\n"
            f"filename: {os.path.basename(file_full_path)}\n"
            f"path: {rel_path}\n\n"
            "## contenxt\n\n"
            f"{code_block_start}"
            f"{file_content}\n"
            "```"
        )
        seq_str = str(seq_counter).zfill(3)
        md_filename = f"{seq_str}_{flat_rel_path}.md"
        md_filepath = os.path.join(output_dir_path, md_filename)
        with open(md_filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        markdown_files_info.append((seq_str, os.path.basename(file_full_path), md_filename, rel_path))
        click.echo(f"Converted {rel_path} to markdown as {md_filename}")
        seq_counter += 1

    # Create an outline file listing all generated markdown files.
    outline_lines = ["# Outline\n"]
    for seq, original, md_filename, rel_path in markdown_files_info:
        outline_lines.append(f"- {md_filename} (original: {original}, path: {rel_path})")
    outline_content = "\n".join(outline_lines)
    outline_path = os.path.join(output_dir_path, "000_outline.md")
    with open(outline_path, "w", encoding="utf-8") as f:
        f.write(outline_content)
    click.echo("Outline file created as 000_outline.md")

    # Create 000_all.md that combines all generated markdown files.
    all_file_path = os.path.join(output_dir_path, "000_all.md")
    with open(all_file_path, "w", encoding="utf-8") as f_all:
        f_all.write("# All Markdown Content\n\n")
        f_all.write("## Outline\n\n")
        f_all.write(outline_content)
        f_all.write("\n\n")
        # Append content of each generated markdown file.
        for seq, original, md_filename, rel_path in markdown_files_info:
            file_path = os.path.join(output_dir_path, md_filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                click.echo(f"Error reading {md_filename}: {e}")
                continue
            f_all.write(f"---\n## {md_filename} (from {rel_path})\n\n")
            f_all.write(content)
            f_all.write("\n\n")
    click.echo("All content combined into 000_all.md")


if __name__ == "__main__":
    cli()
