"""
Entry point if user decides to run `python -m create_dash_app` instead of the
CLI command `create-dash-app`.
"""

from .cli import create_dash_app

if __name__ == "__main__":
    create_dash_app()
