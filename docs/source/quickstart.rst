Quick Start Tutorial
====================

This tutorial will walk you through creating your first Dash application using ``create-dash-app``, step by step.

Step 1: Install the CLI
-----------------------

Install ``create-dash-app`` from GitHub:

.. code-block:: bash

   $ uv pip install git+https://github.com/hquizzagan/create-dash-app.git@v0.1.dev20251106

Verify the installation:

.. code-block:: bash

   $ create-dash-app --help

Step 2: Create Your Project
----------------------------

Run the CLI command:

.. code-block:: bash

   $ create-dash-app

You'll be prompted with an interactive configuration form:

Project Name
   Enter a name for your project (e.g., ``my-dashboard``). This will be the directory name.

Author Name
   Your name (defaults to your system username).

Author Email
   Your email address (validated for proper format).

Description
   Brief description of your project (e.g., "Sales analytics dashboard").

Styling Framework
   Choose from:
   - Tailwind CSS (utility-first CSS framework)
   - Bootstrap (popular CSS framework)
   - Bulma (modern CSS framework)
   - DaisyUI (Tailwind component library)
   - UnoCSS (atomic CSS engine)
   - Windi CSS (on-demand Tailwind CSS)

Animation Library
   Optional animation library:
   - None (no animations)
   - animate.css
   - anime.js
   - ScrollReveal
   - Framer Motion
   - etc.

Include Pages
   Whether to include multi-page routing support (Dash Pages).

Include Tests
   Whether to include pytest scaffolding (recommended: ``True``).

After completing the prompts, the CLI will display your configuration and generate the project.

Step 3: Explore the Generated Structure
---------------------------------------

Navigate to your project directory:

.. code-block:: bash

   $ cd my-dashboard

The generated structure follows an opinionated architecture:

Main Application (``src/app.py``)
   The entry point of your Dash application. This file initializes the app and sets up the layout.

Callbacks (``src/callbacks/``)
   Place your callback functions here. They're automatically discovered and registered using the ``@register_callback`` decorator.

Components (``src/components/``)
   Reusable Dash components. Create functional components that return Dash HTML elements.

Pages (``src/pages/``)
   Page-level layouts for multi-page applications (if enabled).

Stores (``src/stores/``)
   State management stores using ``dcc.Store`` components. Auto-discovered via ``@register_store`` decorator.

Assets (``src/assets/``)
   Static files like CSS, images, and fonts. The ``styles.scss`` file contains your application styles.

Step 4: Run Your Application
------------------------------

The scaffolding automatically runs ``uv sync`` and installs dependencies during project generation, so you're ready to run immediately!

Run your application using one of these methods:

Using the Project Name Directly (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The generated ``pyproject.toml`` includes a console script entry point that installs a command named after your project. After generation, you can run your app directly:

.. code-block:: bash

   $ my-dashboard

This is the simplest way to run your application. The command is available because the scaffolding automatically installs the package in editable mode.

Using uv run
^^^^^^^^^^^^

Alternatively, you can use ``uv run`` to execute the project command:

.. code-block:: bash

   $ uv run my-dashboard

This is equivalent to running ``my-dashboard`` directly and ensures the command runs in the correct virtual environment.

Using Python Module
^^^^^^^^^^^^^^^^^^^

You can also run the app directly as a Python module:

.. code-block:: bash

   $ uv run python -m src.app

Using Docker
^^^^^^^^^^^^

For containerized deployment:

.. code-block:: bash

   $ docker-compose up

Your application will start on ``http://localhost:8000`` (or your configured port).

Why the Project Name Works as a Command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The generated ``pyproject.toml`` includes a console script entry point:

.. code-block:: toml

   [project.scripts]
   my-dashboard = "src.app:main"

During project generation, the scaffolding automatically runs ``uv sync`` and ``uv pip install -e .``, which installs the package in editable mode and makes the console script available. Executing ``my-dashboard`` simply calls ``src.app.main()``, which is equivalent to ``uv run python -m src.app``. This is part of the design philosophy: every generated project ships with a first-class CLI command out of the box, ready to use immediately.

Step 5: Make Your First Change
------------------------------

Let's add a simple component. Create a new file ``src/components/welcome.py``:

.. code-block:: python

   from dash import html

   def welcome_card(title: str, description: str) -> html.Div:
       """A simple welcome card component."""
       return html.Div([
           html.H1(title, className="text-2xl font-bold"),
           html.P(description, className="text-gray-600")
       ], className="p-4 border rounded")

Then use it in ``src/app.py`` by importing and adding it to your layout.

Step 6: Add Your First Callback
--------------------------------

Create a new file ``src/callbacks/interactions.py``:

.. code-block:: python

   from dash import Input, Output
   from callbacks import register_callback

   @register_callback(
       Output("output-div", "children"),
       Input("input-field", "value")
   )
   def update_output(value):
       """Update output based on input."""
       if value:
           return f"You entered: {value}"
       return "Enter something..."

The callback is automatically registered - no need to import it in ``app.py``!

Understanding the Architecture
--------------------------------

Auto-Discovery Pattern
   The CLI uses decorator-based auto-discovery for callbacks and stores. This means:
   - Add a new callback file → automatically included
   - Add a new store file → automatically included
   - No manual imports or registration needed

Component Pattern
   Components are functions that accept parameters and return Dash HTML elements. This React-style pattern makes components reusable and testable.

State Management
   Stores provide client-side state management using Dash's ``dcc.Store`` component. They're automatically discovered and added to your app layout.

Next Steps
----------

- Explore the :doc:`examples` for real-world use cases
- Check the :doc:`api` for detailed API documentation
- Read the generated ``README.md`` in your project for project-specific guidance

