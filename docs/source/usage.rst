Usage Guide
===========

This guide provides everything you need to get started with the ``create-dash-app`` CLI package. Whether you're new to Dash or an experienced developer, this guide will help you quickly scaffold and understand your generated Dash application.

Installation
------------

Since the CLI package is currently in development and not yet published to `PyPI`, installation is done directly from the GitHub repository.

**Prerequisites**:
- Python 3.13+ installed
- ``uv`` package manager installed (recommended)

⭐ Recommended: Use ``uvx`` (Like ``npx`` for Python)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**``uvx``** is the **strongly recommended** way to run CLI tools. It's Python's equivalent to Node.js's ``npx`` - you can run tools without installing them. Since this project uses `uv` for dependency management, ``uvx`` is the natural choice.

.. code-block:: bash

   $ uvx --from git+https://github.com/hquizzagan/create-dash-app.git@<version_number> create-dash-app

**Create an alias for convenience:**

.. code-block:: bash

   # Add to your ~/.zshrc or ~/.bashrc
   $ alias create-dash-app='uvx --from git+https://github.com/hquizzagan/create-dash-app.git@<version_number> create-dash-app'

After adding the alias, you can simply run:

.. code-block:: bash

   $ create-dash-app

Alternative: Install with `pipx` (Persistent Installation)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you prefer a persistent installation (like `npm install -g`), use `pipx`:

.. code-block:: bash

   # Install pipx if you don't have it
   $ pip install pipx
   $ pipx ensurepath

   # Install create-dash-app globally
   $ pipx install git+https://github.com/hquizzagan/create-dash-app.git@<version_number>

**When to use `pipx`:**
- You want the tool permanently installed
- You prefer explicit installation/updates
- You're not using `uv` in your workflow

**Note**: You'll need to update manually: ``pipx upgrade create-dash-app``

Quick Start
-----------

.. note::
   **Prerequisite**: This section assumes you've set up the alias as described in the Installation section above. If you haven't, use the full ``uvx`` command instead.

The fastest way to create your first `Dash` application:

.. code-block:: bash

   $ create-dash-app

This will launch an interactive prompt where you'll configure your project:

- **Project Name**: Name of your Dash application (default: ``my-dash-app``)
- **Author Name**: Your name (defaults to system username)
- **Author Email**: Your email address
- **Description**: Brief description of your project
- **Styling Framework**: Choose from Tailwind CSS, Bootstrap, Bulma, DaisyUI, UnoCSS, or Windi CSS
- **Animation Library**: Optional animation library (none, `animate.css`, `anime.js`, etc.)
- **Include Pages**: Whether to include multi-page routing support
- **Include Tests**: Whether to include `pytest` scaffolding (default: ``True``)

After answering the prompts, the CLI will generate a complete Dash application structure in the current directory.

What Gets Generated
-------------------

The CLI generates an **opinionated** project structure designed for scalability and maintainability:

Project Structure
^^^^^^^^^^^^^^^^^

.. code-block:: text

   my-dash-app/
   ├── Dockerfile                 # Docker configuration
   ├── docker-compose.yml         # Docker Compose setup
   ├── pyproject.toml            # Project metadata and dependencies
   ├── README.md                 # Project documentation
   ├── .pre-commit-config.yaml   # Pre-commit hooks configuration
   ├── src/
   │   ├── __init__.py
   │   ├── app.py                # Main Dash application entry point
   │   ├── callbacks/            # Callback functions (auto-discovered)
   │   │   └── __init__.py
   │   ├── components/           # Reusable Dash components
   │   │   └── __init__.py
   │   ├── pages/                # Page-level layouts
   │   │   └── __init__.py
   │   ├── stores/              # State management stores
   │   │   └── __init__.py
   │   └── assets/              # Static assets (CSS, images, etc.)
   │       └── styles.scss
   └── tests/                    # Test files
       └── test_smoke.py

Key Features
^^^^^^^^^^^^

**Decorator-Based Architecture**
   - **Callbacks**: Auto-discovered via ``@register_callback`` decorator
   - **Stores**: Auto-discovered via ``@register_store`` decorator
   - No manual imports needed or bloating the `app.py` file - just add files and they're automatically registered

**Component-Based Design**
   - React-style functional components
   - Reusable, composable components
   - Clean separation of concerns

**Console Script Entry Point**
   - ``pyproject.toml`` defines a console script via ``[project.scripts]``
   - After ``uv sync``, the command matching your project slug (for example ``my-dash-app``) is installed on your PATH
   - Running ``my-dash-app`` executes ``src.app:main``—the same code path as ``uv run python -m src.app``

Running Your Application
------------------------

After generation, navigate to your project directory. You have two options for running your application:

Option 1: Using the Console Script (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The generated project includes a console script entry point that allows you to run your app directly by its name.

**Step 1: Navigate to your project directory**

.. code-block:: bash

   $ cd my-dash-app

**Step 2: Activate the virtual environment**

The virtual environment (``.venv``) is automatically created during project generation. Activate it:

.. code-block:: bash

   # On macOS/Linux:
   $ source .venv/bin/activate

   # On Windows:
   $ .venv\Scripts\activate

**Step 3: Run your application**

Once the virtual environment is activated, you can run your app using the project name as a command:

.. code-block:: bash

   $ my-dash-app

The app will start and be available at ``http://127.0.0.1:8050`` (or your configured port).

Option 2: Using ``uv run`` (Alternative)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you prefer not to activate the virtual environment manually, you can use ``uv run``:

**Step 1: Navigate to your project directory**

.. code-block:: bash

   $ cd my-dash-app

**Step 2: Run with `uv run`**

.. code-block:: bash

   $ uv run my-dash-app

Or alternatively:

.. code-block:: bash

   $ uv run python -m src.app

**Why `my-dash-app` Works**

The generated ``pyproject.toml`` includes a console script entry point:

.. code-block:: toml

   [project.scripts]
   my-dash-app = "src.app:main"

During project generation, the scaffolding automatically runs ``uv sync`` and ``uv pip install -e .``, which installs the package in editable mode and makes the console script available. Executing ``my-dash-app`` simply calls ``src.app.main()``, which is equivalent to ``uv run python -m src.app``.

This is part of the design philosophy: every generated project ships with a first-class CLI command out of the box, so development and deployment workflows stay consistent and frictionless.

Docker
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   $ docker-compose up

The application will be available at ``http://localhost:8000`` (or the port you configured).

Next Steps
----------

- :doc:`quickstart` - Detailed step-by-step tutorial
- :doc:`examples` - Common use cases and examples
- :doc:`api` - Complete API reference
