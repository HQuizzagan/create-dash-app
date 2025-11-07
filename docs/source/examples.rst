**Examples and Use Cases**
==========================

This section provides practical examples and common use cases for the ``create-dash-app`` CLI and the generated Dash applications.

**Creating a Data Analytics Dashboard**
---------------------------------------

**Scenario**: You need to create a dashboard for visualizing sales data.

**Steps**:

1. Generate the project with analytics-focused configuration:

   .. code-block:: bash

      $ create-dash-app

   When prompted:
   - Project Name: ``sales-dashboard``
   - Description: ``Sales analytics dashboard with interactive charts``
   - Styling: ``Tailwind CSS`` (for modern, responsive design)
   - Include Pages: ``Yes`` (for multiple dashboard views)

2. Add data processing callbacks in ``src/callbacks/data_processing.py``:

   .. code-block:: python

      from dash import Input, Output
      from callbacks import register_callback
      import pandas as pd

      @register_callback(
          Output("sales-chart", "figure"),
          Input("date-range", "value"),
          Input("category-filter", "value")
      )
      def update_sales_chart(date_range, category):
          """Update sales chart based on filters."""
          # Your data processing logic here
          df = load_sales_data(date_range, category)
          fig = create_chart(df)
          return fig

3. Create reusable chart components in ``src/components/charts.py``:

   .. code-block:: python

      from dash import dcc, html
      import plotly.graph_objects as go

      def sales_chart(figure: go.Figure) -> html.Div:
          """Reusable sales chart component."""
          return html.Div([
              dcc.Graph(figure=figure, id="sales-chart")
          ], className="p-4 bg-white rounded shadow")

4. Store filtered data in ``src/stores/data_stores.py``:

   .. code-block:: python

      from dash import dcc
      from stores import register_store

      @register_store
      def create_data_stores():
          """Create data-related stores."""
          return [
              dcc.Store(id="filtered-data", storage_type="memory"),
              dcc.Store(id="chart-config", storage_type="session")
          ]

**Creating a Multi-Page Application**
--------------------------------------

**Scenario**: You need an application with multiple pages (Home, Analytics, Settings).

**Steps**:

1. Generate project with pages enabled:

   .. code-block:: bash

      $ create-dash-app

   When prompted, select ``Include Pages: Yes``.

2. Create page layouts in ``src/pages/``:

   **``src/pages/home.py``**:

   .. code-block:: python

      import dash
      from dash import html
      from components import welcome_card

      dash.register_page(__name__, path="/", name="Home")

      layout = html.Div([
          welcome_card("Welcome", "Dashboard Home Page"),
          # Your home page content
      ])

   **``src/pages/analytics.py``**:

   .. code-block:: python

      import dash
      from dash import html

      dash.register_page(__name__, path="/analytics", name="Analytics")

      layout = html.Div([
          html.H1("Analytics Dashboard"),
          # Your analytics content
      ])

3. Navigation is automatically handled by Dash Pages. The pages are registered and accessible via their paths.

**Using Custom Styling**
------------------------

**Scenario**: You want to use a custom CSS framework or add your own styles.

**Steps**:

1. The generated project includes ``src/assets/styles.scss`` for your custom styles.

2. Add your custom CSS:

   .. code-block:: scss

      // src/assets/styles.scss
      .custom-card {
          padding: 1rem;
          border-radius: 0.5rem;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }

3. The styles are automatically included in your application. For Tailwind CSS, you can also use utility classes directly in your components.

**Adding Real-Time Updates**
------------------------------

**Scenario**: You need a dashboard that updates in real-time.

**Steps**:

1. Use Dash's interval component for periodic updates:

   .. code-block:: python

      from dash import dcc, Input, Output
      from callbacks import register_callback

      @register_callback(
          Output("live-data", "children"),
          Input("interval-component", "n_intervals")
      )
      def update_live_data(n):
          """Update data every interval."""
          data = fetch_latest_data()
          return format_data(data)

2. Add the interval component to your layout in ``src/app.py``:

   .. code-block:: python

      dcc.Interval(
          id="interval-component",
          interval=5000,  # Update every 5 seconds
          n_intervals=0
      )

**Deploying to Production**
----------------------------

**Scenario**: You want to deploy your application using Docker.

**Steps**:

1. The generated project includes ``Dockerfile`` and ``docker-compose.yml``.

2. Build and run with Docker:

   .. code-block:: bash

      $ docker-compose build
      $ docker-compose up -d

3. For production, configure environment variables in ``docker-compose.yml``:

   .. code-block:: yaml

      services:
        app:
          environment:
            - PORT=8000
            - DEBUG=False

4. The application uses gunicorn for production WSGI serving, configured in the Dockerfile.

**Testing Your Application**
-----------------------------

**Scenario**: You want to write tests for your Dash application.

**Steps**:

1. The generated project includes pytest scaffolding in ``tests/``.

2. Write tests for your components:

   .. code-block:: python

      def test_welcome_card():
          """Test welcome card component."""
          from components.welcome import welcome_card
          from dash import html

          result = welcome_card("Test", "Description")
          assert isinstance(result, html.Div)

3. Run tests:

   .. code-block:: bash

      $ uv run pytest

**Best Practices**
-------------------

**Organizing Callbacks**
   - Group related callbacks in the same file
   - Use descriptive file names (e.g., ``data_processing.py``, ``ui_interactions.py``)
   - Keep callbacks focused on a single responsibility

**Component Design**
   - Make components reusable and composable
   - Accept parameters (props) for flexibility
   - Keep components small and focused

**State Management**
   - Use stores for data that needs to persist across callbacks
   - Use ``memory`` storage for temporary data
   - Use ``session`` storage for user-specific data

**Code Quality**
   - Run pre-commit hooks before committing: ``pre-commit run --all-files``
   - Write tests for critical functionality
   - Follow the generated code style (enforced by Ruff)

