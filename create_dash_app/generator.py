import json
import os
import shutil
import subprocess
from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader

from .models.project_config import ProjectConfig


# TODO: Add support for `create-dash-app build-tailwind-css` script to build `tailwind-output` file.
class ProjectGenerator:
    """
    Generates a Plotly Dash application project with boilerplate code
    which uses our **opinionated** layout and architecture which mainly includes
    the following:

    - use `pyproject.toml` and `uv` for dependency and environment management.
      This includes use of `[project.scripts]` in `pyproject.toml` for entry
      points which allows running the app via:
      `<project_name>` or `python -m <project_name>` or `uv run python -m <project_name>`
    - use of a pre-configured pre-commit hooks configuration which uses
      `ruff` for linting and formatting, and `pre-commit-hooks` for
      trailing whitespace, end of file fixer, and check-yaml.
    - use of `React.js`-style component-based architecture
    - using a shared registry for managing:
        - callbacks for event handling
        - stores for state management
      to lessen user complexity in managing the project especially as the app
      grows in complexity. This allows user to:
        - seggregate/group together related callbacks but still still
          having a single APP-wide registry for callbacks (no need to
          manually import and register callbacks in app.py)
        - seggregate/group together related stores but still still
          having a single APP-wide registry for stores (no need to
          manually import and register stores in app.py)
    """

    def __init__(self, project_name: str, template_type: str = "basic"):
        self.project_name = project_name
        self.template_type = template_type

        # Will be set in _create_project_dirs to handle "." case
        self.project_path: Path = Path(".")

        # Contains the root-level file templates regardless of template type
        self.templates_base_path = Path(__file__).parent / "templates"

        # Contains the template files for the specific template type
        self.template_path = self.templates_base_path / template_type

        # Create Jinja2 environment that can load from both templates/ and templates/<type>/
        self.jinja_env = Environment(
            loader=FileSystemLoader(searchpath=[self.templates_base_path, self.template_path]),
            autoescape=True,
            trim_blocks=True,
        )

    def generate_project(self, config: ProjectConfig) -> None:
        """Generate the complete project structure."""
        try:
            self._create_project_dirs(config)
            self._generate_files(config)
            self._setup_tailwind_css(config)
            self._initialize_uv_dependencies()
            self._make_executable_files()
            click.echo(
                click.style(f"✅ Successfully created {self.project_name}", fg="green", bold=True)
            )
            self._display_next_steps(config)
        except Exception as e:
            self._cleanup_on_error()
            click.echo(click.style(f"❌ Error creating project: {e}", fg="red"), err=True)

    def _create_project_dirs(self, config: ProjectConfig) -> None:
        """
        Create the main project directory, and configures the environment
        to use `uv` for dependency management, and `.env.<FLASK_ENV>` for environment variables.
        """
        # Handle case where project_name is "." (initialize current directory)
        if self.project_name == ".":
            # Use current directory name as project name for file generation
            self.project_name = os.path.basename(os.getcwd())
            self.project_path = Path(".")
            click.echo(
                click.style(f"Initializing current directory: {self.project_name}", fg="blue")
            )
        else:
            # Create the project's ROOT directory
            if os.path.exists(self.project_name):
                raise FileExistsError(
                    f"Directory {self.project_name} already exists! "
                    "Please choose a different project name."
                )
            os.makedirs(self.project_name)
            self.project_path = Path(self.project_name)
            click.echo(click.style(f"Created project directory: {self.project_name}", fg="blue"))

        # Create the `pages/` directory (always created for homepage sample)
        (self.project_path / "src" / "pages").mkdir(parents=True, exist_ok=True)
        click.echo(click.style("Created `pages/` directory", fg="blue"))

    def _generate_files(self, config: ProjectConfig) -> None:
        """Generate all project files from templates."""
        # Process shared root-level templates (files directly in templates/)
        for template in self.templates_base_path.iterdir():
            if template.is_file():
                # Allow hidden files if they have .jinja extension
                # (e.g., .env.development.jinja)
                if not template.name.startswith(".") or template.suffix == ".jinja":
                    self._process_template_file(template, config, is_root_template=True)

        # Process template-specific files (files in templates/<type>/)
        for template in self.template_path.rglob("*"):
            if template.is_file():
                # Allow hidden files if they have .jinja extension
                # (e.g., .env.development.jinja)
                if not template.name.startswith(".") or template.suffix == ".jinja":
                    self._process_template_file(template, config, is_root_template=False)

        click.echo(click.style("✅ Successfully generated template files!", fg="green", bold=True))

    def _process_template_file(
        self, template: Path, config: ProjectConfig, is_root_template: bool
    ) -> None:
        """
        Generate a single template file.

        Args:
            template: Path to the template file
            config: Project configuration
            is_root_template: If True, file goes to project root; if False, goes to src/

        NOTE: With template generation, the `create_dash_app` CLI has a `templates/` directory which
        also is structured to mimic the actual project structure. Thus, for each detected `.jinja`
        file, the parent directory of the file (up to the `create_dash_app/templates/` directory)
        will be the corresponding ACTUAL directory of the project, and thus needs to be created.
        Files directly in `templates/` go to project root (shared across template types).
        Files in `templates/<type>/` go to `src/` directory (template-specific).
        """
        # Determine the base path for relative path calculation
        base_path = self.templates_base_path if is_root_template else self.template_path
        template_rel_path = template.relative_to(base_path)

        # Load template - try with relative path first
        try:
            template_file = self.jinja_env.get_template(str(template_rel_path))
        except Exception:
            # Fallback: try with just the filename if relative path fails
            template_file = self.jinja_env.get_template(template.name)

        # Prevent rendering of baseline pre-commit hook configurations if not chosen
        if not config.configure_pre_commit and "pre-commit" in template.name.lower():
            click.echo(
                click.style(f"Skipping {template_file.name} configurations ...", fg="yellow")
            )
            return

        # Render the template file by unpacking the provided config as a dictionary
        rendered_template = template_file.render(**config.model_dump())

        # Determine target directory based on whether it's a root template
        if is_root_template:
            # Root templates go directly to project root
            target_dir = self.project_path
        else:
            # Template-specific files go to src/
            file_directory = template.parent.relative_to(self.template_path)
            target_dir = self.project_path / "src" / file_directory

        target_dir.mkdir(parents=True, exist_ok=True)

        # Write the rendered template to the target file (remove .jinja extension)
        output_filename = template.stem if template.suffix == ".jinja" else template.name
        target_file = target_dir / output_filename
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(rendered_template)

    def _initialize_uv_dependencies(self) -> None:
        """
        Initialize uv dependencies by running `uv sync` to generate uv.lock and
        install dependencies. This should be run after pyproject.toml is generated.

        The templated pyproject.toml is used, and uv sync will generate the lock file
        and install all dependencies defined in pyproject.toml.
        """
        pyproject_path = self.project_path / "pyproject.toml"
        if not pyproject_path.exists():
            click.echo(click.style("⚠️  pyproject.toml not found, skipping uv sync", fg="yellow"))
            return

        try:
            click.echo(
                click.style(
                    "Running uv sync to generate lock file and install dependencies ...", fg="blue"
                )
            )
            subprocess.run(
                ["uv", "sync"],
                cwd=str(self.project_path),
                capture_output=True,
                text=True,
                check=True,
            )
            # Install the package in editable mode so console scripts work
            click.echo(
                click.style(
                    "Installing package in editable mode for console scripts ...", fg="blue"
                )
            )
            subprocess.run(
                ["uv", "pip", "install", "-e", "."],
                cwd=str(self.project_path),
                capture_output=True,
                text=True,
                check=True,
            )
            click.echo(
                click.style(
                    "✅ Successfully generated uv.lock and installed dependencies",
                    fg="green",
                    bold=True,
                )
            )
        except subprocess.CalledProcessError as e:
            click.echo(
                click.style(f"⚠️  Warning: uv sync failed: {e.stderr}", fg="yellow"),
                err=True,
            )
        except FileNotFoundError:
            click.echo(
                click.style(
                    "⚠️  Warning: uv command not found. "
                    "Please install uv and run 'uv sync' manually.",
                    fg="yellow",
                ),
                err=True,
            )

    def _setup_tailwind_css(self, config: ProjectConfig) -> None:
        """
        Set up Tailwind CSS if it's selected in the styling configuration.

        This method:
        - Initializes npm in the project
        - Installs tailwindcss and @tailwindcss/cli as dev dependencies
        - Creates tailwind.css entry file
        - Creates tailwind.config.js
        - Updates package.json with build scripts
        - Runs the production build to generate the compiled CSS
        """
        if "tailwind" not in config.styling:
            return

        package_json_path = self.project_path / "package.json"

        try:
            # Initialize npm if package.json doesn't exist
            if not package_json_path.exists():
                click.echo(click.style("Initializing npm for Tailwind CSS setup ...", fg="blue"))
                subprocess.run(
                    ["npm", "init", "-y"],
                    cwd=str(self.project_path),
                    capture_output=True,
                    text=True,
                    check=True,
                )
                click.echo(click.style("✅ Initialized npm", fg="green"))

            # Install Tailwind CSS and CLI
            click.echo(
                click.style("Installing Tailwind CSS and CLI as dev dependencies ...", fg="blue")
            )
            subprocess.run(
                ["npm", "install", "-D", "tailwindcss", "@tailwindcss/cli"],
                cwd=str(self.project_path),
                capture_output=True,
                text=True,
                check=True,
            )
            click.echo(click.style("✅ Installed Tailwind CSS dependencies", fg="green"))

            # Create tailwind.css entry file
            tailwind_css_path = self.project_path / "src" / "assets" / "tailwind.css"
            tailwind_css_path.parent.mkdir(parents=True, exist_ok=True)
            with open(tailwind_css_path, "w", encoding="utf-8") as f:
                f.write('@import "tailwindcss";\n')
            click.echo(click.style("✅ Created tailwind.css entry file", fg="green"))

            # Create tailwind.config.js
            tailwind_config_path = self.project_path / "tailwind.config.js"
            tailwind_config_content = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{py,html,js}",
    "./src/**/*.py",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
            with open(tailwind_config_path, "w", encoding="utf-8") as f:
                f.write(tailwind_config_content)
            click.echo(click.style("✅ Created tailwind.config.js", fg="green"))

            # Update package.json with build scripts
            with open(package_json_path, "r", encoding="utf-8") as f:
                package_json = json.load(f)

            package_json.setdefault("scripts", {})
            package_json["scripts"]["build:css"] = (
                "tailwindcss -i ./src/assets/tailwind.css "
                "-o ./src/assets/tailwind-output.css --watch"
            )
            package_json["scripts"]["build:css:prod"] = (
                "tailwindcss -i ./src/assets/tailwind.css "
                "-o ./src/assets/tailwind-output.css --minify"
            )

            with open(package_json_path, "w", encoding="utf-8") as f:
                json.dump(package_json, f, indent=2)
            click.echo(click.style("✅ Updated package.json with build scripts", fg="green"))

            # Run the production build
            click.echo(click.style("Building Tailwind CSS (production build) ...", fg="blue"))
            subprocess.run(
                ["npm", "run", "build:css:prod"],
                cwd=str(self.project_path),
                capture_output=True,
                text=True,
                check=True,
            )
            click.echo(
                click.style("✅ Successfully built Tailwind CSS output file", fg="green", bold=True)
            )

        except subprocess.CalledProcessError as e:
            click.echo(
                click.style(
                    f"⚠️  Warning: Tailwind CSS setup failed: {e.stderr}",
                    fg="yellow",
                ),
                err=True,
            )
        except FileNotFoundError:
            click.echo(
                click.style(
                    "⚠️  Warning: npm or node not found. "
                    "Please install Node.js and npm, then run 'npm install' "
                    "and 'npm run build:css:prod' manually.",
                    fg="yellow",
                ),
                err=True,
            )
        except Exception as e:
            click.echo(
                click.style(
                    f"⚠️  Warning: Tailwind CSS setup encountered an error: {e}",
                    fg="yellow",
                ),
                err=True,
            )

    def _make_executable_files(self) -> None:
        """Make shell scripts and other executable files executable."""
        click.echo(
            click.style(
                "Skipping making executable files as this is not implemented yet.", fg="yellow"
            )
        )

    def _display_next_steps(self, config: ProjectConfig) -> None:
        """Display helpful next steps after project creation."""
        project_slug = config.project_name.lower().replace(" ", "-").replace("_", "-")

        click.echo("")
        click.echo(click.style("📋 Next Steps:", fg="cyan", bold=True))
        click.echo("")

        # Step 1: Navigate to project directory (skip if initializing current dir)
        if self.project_path != Path("."):
            click.echo(click.style("1. Navigate to your project:", fg="yellow"))
            click.echo(f"   cd {self.project_name}")
        click.echo("")

        # Step 2: Activate virtual environment (if using uv)
        click.echo(click.style("2. Activate the virtual environment:", fg="yellow"))
        click.echo("   # If using uv (recommended):")
        click.echo("   uv venv")
        click.echo("   source .venv/bin/activate  # On macOS/Linux")
        click.echo("   .venv\\Scripts\\activate     # On Windows")
        click.echo("")
        click.echo("   # Or use uv run directly (no activation needed):")
        click.echo("   uv run <command>")
        click.echo("")

        # Step 3: Install dependencies (if not already done)
        click.echo(click.style("3. Install dependencies (if not already done):", fg="yellow"))
        click.echo("   uv sync")
        click.echo("")

        # Step 4: Build Tailwind CSS (if configured)
        if "tailwind" in config.styling:
            click.echo(click.style("4. Build Tailwind CSS:", fg="yellow"))
            click.echo("   npm run build:css:prod")
            click.echo("   # Or for watch mode during development:")
            click.echo("   npm run build:css")
            click.echo("")

        # Step 5: Run the application
        step_num = 5 if "tailwind" in config.styling else 4
        click.echo(click.style(f"{step_num}. Run your Dash application:", fg="yellow"))
        click.echo("   # Option 1: Using the console script")
        click.echo(f"   {project_slug}")
        click.echo("")
        click.echo("   # Option 2: Using Python module")
        click.echo("   python -m src.app")
        click.echo("")
        click.echo("   # Option 3: Using uv run")
        click.echo(f"   uv run {project_slug}")
        click.echo("   # Or")
        click.echo("   uv run python -m src.app")
        click.echo("")

        # Step 6: Development tips
        step_num += 1
        click.echo(click.style(f"{step_num}. Development tips:", fg="yellow"))
        click.echo("   • The app will automatically open in your browser")
        click.echo("   • Default URL: http://127.0.0.1:8050")
        click.echo("   • Edit files in src/ to customize your app")
        if config.include_pages:
            click.echo("   • Add new pages in src/pages/")
        click.echo("   • Add callbacks in src/callbacks/")
        click.echo("   • Add components in src/components/")
        click.echo("")

        # Step 7: Additional resources
        step_num += 1
        click.echo(click.style(f"{step_num}. Additional resources:", fg="yellow"))
        click.echo("   • Dash documentation: https://dash.plotly.com/")
        if "tailwind" in config.styling:
            click.echo("   • Tailwind CSS docs: https://tailwindcss.com/docs")
        click.echo(
            "   • Dash Bootstrap Components: https://dash-bootstrap-components.opensource.faculty.ai/"
        )
        click.echo("")

        click.echo(click.style("🎉 Happy coding!", fg="green", bold=True))
        click.echo("")

    def _cleanup_on_error(self) -> None:
        """
        Remove partially created project directory on error.

        If project generation fails mid-process, we remove the
        created project directory to prevent leaving partial/broken projects
        on the filesystem. Only cleans up if self.project_name exists.
        """
        # Only cleanup if we created a new directory (not if initializing current dir)
        if (
            self.project_path
            and self.project_path != Path(".")
            and os.path.exists(self.project_path)
        ):
            # Remove the project directory and its contents
            shutil.rmtree(self.project_path)
            click.echo(
                click.style(
                    f"Removed partially created project directory: {self.project_name}", fg="blue"
                )
            )
        elif self.project_path == Path("."):
            click.echo(
                click.style(
                    "Note: Current directory was being initialized. Manual cleanup may be needed.",
                    fg="yellow",
                )
            )
