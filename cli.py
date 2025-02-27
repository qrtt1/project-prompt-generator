import click
from prompts.generator import (
    generate_individual_files,
    generate_single_file,
)

@click.group()
def cli():
    """A CLI tool that converts project files (excluding those in .gitignore) into markdown."""
    pass


@cli.command(name="generate", aliases=["g", "gen"])
@click.option('--no-mask', is_flag=True, help='Disable sensitive data masking.')
@click.option('--add-pattern', multiple=True, help='Add custom regex patterns to mask sensitive data.')
def generate(no_mask, add_pattern):
    """Generate individual markdown files for all project files (recursively) excluding ignored ones."""
    generate_individual_files(no_mask, add_pattern)


@cli.command(name="generate_all_in_one", aliases=["a", "all"])
@click.option('--no-mask', is_flag=True, help='Disable sensitive data masking.')
@click.option('--add-pattern', multiple=True, help='Add custom regex patterns to mask sensitive data.')
def generate_all_in_one(no_mask, add_pattern):
    """Generate a single all-in-one markdown file for all project files."""
    generate_single_file(no_mask, add_pattern)


if __name__ == "__main__":
    cli()