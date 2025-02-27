import click
from prompts.generator import (
    generate_individual_files,
    generate_single_file,
)

@click.group()
def cli():
    """A CLI tool that converts project files (excluding those in .gitignore) into markdown."""
    pass


@cli.command(name="generate")
@click.option('--no-mask', is_flag=True, help='Disable sensitive data masking.')
@click.option('--add-pattern', multiple=True, help='Add custom regex patterns to mask sensitive data.')
def generate(no_mask, add_pattern):
    """Generate individual markdown files for all project files (recursively) excluding ignored ones."""
    generate_individual_files(no_mask, add_pattern)


# Add command aliases using Click's alternative method
@cli.command(name="g")
@click.option('--no-mask', is_flag=True, help='Disable sensitive data masking.')
@click.option('--add-pattern', multiple=True, help='Add custom regex patterns to mask sensitive data.')
def generate_alias1(no_mask, add_pattern):
    """Alias for generate command."""
    generate_individual_files(no_mask, add_pattern)


@cli.command(name="gen")
@click.option('--no-mask', is_flag=True, help='Disable sensitive data masking.')
@click.option('--add-pattern', multiple=True, help='Add custom regex patterns to mask sensitive data.')
def generate_alias2(no_mask, add_pattern):
    """Alias for generate command."""
    generate_individual_files(no_mask, add_pattern)


@cli.command(name="generate_all_in_one")
@click.option('--no-mask', is_flag=True, help='Disable sensitive data masking.')
@click.option('--add-pattern', multiple=True, help='Add custom regex patterns to mask sensitive data.')
def generate_all_in_one(no_mask, add_pattern):
    """Generate a single all-in-one markdown file for all project files."""
    generate_single_file(no_mask, add_pattern)


# Add command aliases for generate_all_in_one
@cli.command(name="a")
@click.option('--no-mask', is_flag=True, help='Disable sensitive data masking.')
@click.option('--add-pattern', multiple=True, help='Add custom regex patterns to mask sensitive data.')
def all_alias1(no_mask, add_pattern):
    """Alias for generate_all_in_one command."""
    generate_single_file(no_mask, add_pattern)


@cli.command(name="all")
@click.option('--no-mask', is_flag=True, help='Disable sensitive data masking.')
@click.option('--add-pattern', multiple=True, help='Add custom regex patterns to mask sensitive data.')
def all_alias2(no_mask, add_pattern):
    """Alias for generate_all_in_one command."""
    generate_single_file(no_mask, add_pattern)


if __name__ == "__main__":
    cli()