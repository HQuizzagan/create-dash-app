# create-dash-app

A CLI tool for generating opinionated Plotly Dash application scaffolds with auto-discovered callbacks, stores, and modern tooling.

## Overview

`create-dash-app` generates Dash application boilerplates designed for **scalability**, **maintainability**, and **developer experience**. The generated projects feature:

- **Auto-discovered callbacks and stores** — No manual imports needed
- **React-style functional components** — Reusable and composable
- **Modern dependency management** — Uses `uv` for fast, reliable dependency resolution
- **Docker support** — Production-ready configuration included
- **Code quality tools** — Pre-configured Ruff and pre-commit hooks

## Installation

```bash
uv pip install git+https://github.com/hquizzagan/create-dash-app.git@v1.0.dev20251106
```

## Quick Start

```bash
create-dash-app
```

This launches an interactive prompt to configure your project. After generation, dependencies are automatically installed and the project is ready to run.

## Documentation

Full documentation is available in the `docs/` directory. Build with:

```bash
cd docs
make html
```

## For Developers

### Development Setup

```bash
# Clone the repository
git clone https://github.com/hquizzagan/create-dash-app.git
cd create-dash-app

# Install dependencies
uv sync

# Install in editable mode
uv pip install -e .

# Run the CLI
create-dash-app
```

### Project Structure

```
create-dash-app/
├── create_dash_app/      # Main package
│   ├── cli.py            # CLI entry point
│   ├── generator.py       # Project generation logic
│   ├── prompts.py         # Interactive configuration
│   └── templates/         # Jinja2 templates
├── docs/                  # Sphinx documentation
└── tests/                 # Test suite
```

### Key Features

- **Template Engine**: Jinja2-based templating for personalized project generation
- **Interactive Prompts**: Uses `questionary` for enhanced user experience
- **Auto-Discovery**: Decorator-based registry for callbacks and stores
- **Modern Tooling**: `uv` for dependencies, Docker for deployment

## Contributing

Contributions are welcome! To get started:

1. Fork the repository and create a new branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Install dependencies and the package in editable mode:

   ```bash
   uv sync
   uv pip install -e .
   ```

3. Run the CLI locally and add tests/docs as needed.
4. Submit a pull request describing your changes.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE) (GPL-3.0).

