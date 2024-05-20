"""
Actual entry point for the CLI command `create-dash-app`.
"""

import click

from .generator import ProjectGenerator
from .prompts import collect_project_config


@click.command(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Create a new Plotly Dash application with opinionated boilerplate code.",
)
def create_dash_app():
    """
    Create a new Plotly Dash application with opinionated boilerplate code.

    This command launches an interactive prompt to configure your Dash application,
    including project name, author information, styling framework, and optional features.

    The generated project includes:
    - Auto-discovered callbacks and stores (no manual imports needed)
    - React-style functional components
    - Modern dependency management with uv
    - Docker support for development and production
    - Pre-configured code quality tools (Ruff, pre-commit)

    After generation, dependencies are automatically installed and the project
    is ready to run immediately.

    Examples:
        $ create-dash-app
        $ create-dash-app --help
    """

    try:
        project_config = collect_project_config()
        click.echo(f"Your Project Configuration:\n\n{project_config.model_dump_json(indent=2)}\n\n")
    except FileExistsError as e:
        click.echo(click.style(f"\n\n‼️ ERROR! {e}\n\n", fg="bright_red", bold=True))
        return

    try:
        project_generator = ProjectGenerator(project_name=project_config.project_name)
        project_generator.generate_project(config=project_config)
    except Exception as e:
        click.echo(click.style(f"\n\n‼️ ERROR! {e}\n\n", fg="bright_red", bold=True))
        return
