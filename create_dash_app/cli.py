"""
Actual entry point for the CLI command `create-dash-app`.
"""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import click

from .generator import ProjectGenerator
from .prompts import collect_project_config


def get_version() -> str:
    """Get the package version from installed package metadata."""
    try:
        return version("create-dash-app")
    except PackageNotFoundError:
        # Fallback for development/editable installs
        return "dev"


def _warn_if_inside_project_directory() -> None:
    """
    Warn the user if they're running create-dash-app from inside a project directory.

    This helps prevent creating nested project structures like:
    business-dashboard/business-dashboard/
    """
    cwd = Path.cwd()

    # Check for common project indicators
    project_indicators = [
        "pyproject.toml",
        "src",
        ".venv",
        "venv",
        "requirements.txt",
        "setup.py",
    ]

    # Check if current directory looks like a project directory
    has_indicators = any((cwd / indicator).exists() for indicator in project_indicators)

    if has_indicators:
        warning_msg = (
            "\n⚠️  WARNING: You appear to be running this command from inside a project directory.\n"
            "This may create a nested project structure.\n\n"
            "💡 RECOMMENDED: Use 'uvx' to run without installation (like npx):\n"
            "   uvx --from "
            "git+https://github.com/hquizzagan/create-dash-app.git@<version> "
            "create-dash-app\n\n"
            "Or create an alias in your ~/.zshrc or ~/.bashrc:\n"
            "   alias create-dash-app='uvx --from "
            "git+https://github.com/hquizzagan/create-dash-app.git@<version> "
            "create-dash-app'\n\n"
            "Then run 'create-dash-app' from the parent directory "
            "where you want your project created.\n"
        )
        click.echo(click.style(warning_msg, fg="yellow", bold=True))
        if not click.confirm("Continue anyway?", default=False):
            click.echo(click.style("Cancelled.", fg="blue"))
            raise click.Abort()


@click.command(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Create a new Plotly Dash application with opinionated boilerplate code.",
)
@click.version_option(
    version=get_version(),
    prog_name="create-dash-app",
    message="%(prog)s version %(version)s",
    help="Show the version and exit.",
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
        $ create-dash-app --version
        $ create-dash-app -V
    """

    # Warn if running from inside a project directory
    _warn_if_inside_project_directory()

    try:
        project_config = collect_project_config()
        click.echo(f"Your Project Configuration:\n\n{project_config.model_dump_json(indent=2)}\n\n")
    except FileExistsError as e:
        click.echo(click.style(f"\n\n‼️ ERROR! {e}\n\n", fg="bright_red", bold=True))
        return
    except click.Abort:
        return

    try:
        project_generator = ProjectGenerator(project_name=project_config.project_name)
        project_generator.generate_project(config=project_config)
    except Exception as e:
        click.echo(click.style(f"\n\n‼️ ERROR! {e}\n\n", fg="bright_red", bold=True))
        return
