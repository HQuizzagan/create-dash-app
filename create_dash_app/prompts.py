"""
This module contains the CLI prompts the user will be seeing when
they run the `create-dash-app` CLI.
"""

import getpass
import os
import re

import questionary

from .models.project_config import ProjectConfig

custom_style = questionary.Style([
    ("qmark", "fg:#00d9ff bold"),  # Bright cyan
    ("question", "fg:#ff1493 bold"),  # Hot pink
    ("answer", "fg:#00ff7f bold"),  # Spring green
    ("pointer", "fg:#ff6600 bold"),  # Vibrant orange
    ("highlighted", "fg:#ffff00 bold"),  # Bright yellow
    ("selected", "fg:#9d00ff bold"),  # Electric purple
    ("separator", "fg:#00bfff bold"),  # Deep sky blue
    ("instruction", "fg:#ff69b4 italic"),  # Light pink
    ("text", ""),
    ("disabled", "fg:#888888"),  # Gray
    ("default", "fg:#00ff88 bold"),  # Mint green
])


def validate_email(email: str) -> bool:
    """Validate an email address."""
    return re.search(r"[^@]+@[^@]+\.[^@]+", email) is not None and email != ""


# Disable v1 flags until v0.2.0 is released.
DISABLE_V1_FLAGS = True


def collect_project_config() -> ProjectConfig:
    """
    Collect user configuration and generate a new Dash application boilerplate.
    """

    config = questionary.form(
        project_name=questionary.text("Project Name: ", default="my-dash-app", style=custom_style),
        author_name=questionary.text(
            "Author Name: ", default=getpass.getuser(), style=custom_style
        ),
        author_email=questionary.text(
            "Author Email: ", default="", validate=validate_email, style=custom_style
        ),
        description=questionary.text(
            "Project Description: ", default="A Dash application", style=custom_style
        ),
        styling=questionary.checkbox(
            "Which CSS framework would you like to use?",
            choices=[
                "none",
                questionary.Separator(),
                "tailwind",
                "bootstrap",
                "bulma",
                "daisyui",
                "unocss",
                "windi",
            ],
            default="tailwind",
            style=custom_style,
        ),
        animations=questionary.checkbox(
            "Which animation library would you like to use?",
            choices=[
                "none",
                questionary.Separator(),
                "animate.css",
                "animejs",
                "scrollreveal",
                "animatecss",
                "motion",
            ],
            default="none",
            style=custom_style,
        ),
        include_pages=questionary.confirm(
            "Would you like to include multi-page routing?",
            default=False,
            style=custom_style,
        ),
        include_tests=questionary.confirm(
            "Would you like to include pytest scaffolding?",
            default=True,
            instruction=(
                "\nSelecting `False` will not have any effect until `create-dash-app: v.0.2.0`."
            ),
            style=custom_style,
        ).skip_if(DISABLE_V1_FLAGS, default=True),
        include_auth=questionary.confirm(
            "Would you like to include authentication?",
            default=False,
            instruction=(
                "\nSelecting `True` will not have any effect until `create-dash-app: v.0.2.0`."
            ),
            style=custom_style,
        ).skip_if(DISABLE_V1_FLAGS, default=False),
        include_database=questionary.confirm(
            "Would you like to include a database?",
            default=False,
            instruction=(
                "\nSelecting `True` will not have any effect until `create-dash-app: v.0.2.0`."
            ),
            style=custom_style,
        ).skip_if(DISABLE_V1_FLAGS, default=False),
        include_docker=questionary.confirm(
            "Would you like to include a Dockerfile and docker-compose.yml?",
            default=True,
            instruction=(
                "\nSelecting `False` will not have any effect until `create-dash-app: v.0.2.0`."
            ),
            style=custom_style,
        ).skip_if(DISABLE_V1_FLAGS, default=True),
        configure_pre_commit=questionary.confirm(
            "Would you like to include baseline pre-commit hook configurations?",
            default=True,
            style=custom_style,
        ),
        port=questionary.text(
            "What port would you like to run the application on?",
            default="8000",
            style=custom_style,
        ),
    ).ask()

    # Smart detection: If CWD name matches project name, offer to initialize current directory
    cwd_name = os.path.basename(os.getcwd())
    project_name = config["project_name"]

    # Normalize names for comparison (handle hyphens, underscores, case)
    def normalize_name(name: str) -> str:
        return name.lower().replace("-", "_").replace(" ", "_")

    if normalize_name(cwd_name) == normalize_name(project_name):
        # Check if directory is empty or only has .venv
        dir_contents = set(os.listdir("."))
        dir_contents.discard(".venv")  # Ignore .venv if present
        dir_contents.discard(".git")  # Ignore .git if present

        if not dir_contents or (len(dir_contents) == 1 and ".git" in os.listdir(".")):
            # Directory is essentially empty
            if questionary.confirm(
                f"📁 You're in a directory named '{cwd_name}' and want to create '{project_name}'.\n"
                "Would you like to initialize the current directory instead of creating a nested one?",
                default=True,
                style=custom_style,
            ).ask():
                # Use current directory - don't create a nested one
                config["project_name"] = "."
                # Instantiate the Pydantic model to trigger validation and field validators
                return ProjectConfig(**config)

    # Validate uniqueness of `project_name`
    if os.path.exists(config["project_name"]) and config["project_name"] != ".":
        raise FileExistsError(
            f"Project `{config['project_name']}` already exists! "
            "Please choose a different project name. "
            "You can also run `create-dash-app` in a different directory. "
            "You can also delete the existing project and run `create-dash-app` again."
        )

    # Instantiate the Pydantic model to trigger validation and field validators
    return ProjectConfig(**config)
