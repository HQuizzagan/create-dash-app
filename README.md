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

**Prerequisites**: Python 3.13+ and `uv` package manager.

### ⭐ Recommended: Use `uvx` (Like `npx` for Python)

**`uvx`** is the **strongly recommended** way to run CLI tools. It's Python's equivalent to Node.js's `npx` - you can run tools without installing them. Since this project uses `uv` for dependency management, `uvx` is the natural choice.

```bash
# Run directly without installation (like npx)
uvx --from git+https://github.com/hquizzagan/create-dash-app.git@v0.1.dev20251106 create-dash-app
```

**Benefits of `uvx`:**
- ✅ **No installation needed** - run tools on-demand (like `npx`)
- ✅ **Always up-to-date** - uses latest version automatically
- ✅ **Isolated execution** - runs in isolated environment (no dependency conflicts)
- ✅ **Fast** - `uv` is 10-100× faster than traditional tools
- ✅ **Cached** - subsequent runs are instant
- ✅ **Prevents nested project structures** - run from any directory

**Create an alias for convenience:**
```bash
# Add to your ~/.zshrc or ~/.bashrc
alias create-dash-app='uvx --from git+https://github.com/hquizzagan/create-dash-app.git@v0.1.dev20251106 create-dash-app'
```

After adding the alias, you can simply run:
```bash
create-dash-app
```

### Alternative: Install with `pipx` (Persistent Installation)

If you prefer a persistent installation (like `npm install -g`), use `pipx`:

```bash
# Install pipx if you don't have it
pip install pipx
pipx ensurepath

# Install create-dash-app globally
pipx install git+https://github.com/hquizzagan/create-dash-app.git@v0.1.dev20251106
```

**When to use `pipx`:**
- You want the tool permanently installed
- You prefer explicit installation/updates
- You're not using `uv` in your workflow

**Note**: You'll need to update manually: `pipx upgrade create-dash-app`

### Understanding the Difference

**Why not global system installation?**
- `pip install --user` or `sudo pip install` installs directly to system Python
- Can cause dependency conflicts and pollute your Python environment
- **This is what's discouraged**

**`pipx` vs `uvx`:**
- **`pipx`**: Installs tools in isolated environments (like `npm install -g`)
- **`uvx`**: Runs tools without installation (like `npx`) - **recommended for modern workflows**

### ⚠️ Not Recommended: Install in Virtual Environment

Installing in a project's virtual environment can lead to nested project structures and confusion. However, if you must:

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
uv pip install git+https://github.com/hquizzagan/create-dash-app.git@v0.1.dev20251106
```

**Important**: When using this method:
1. Run `create-dash-app` from the **parent directory** where you want your project created
2. **Do NOT** run it from inside an existing project directory (this creates nested structures)
3. The CLI will warn you if it detects you're in a project directory

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

