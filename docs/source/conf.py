# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# If extensions or modules to document with `autodoc` are in another directory,
# we need to add these directories to sys.path here.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# The above is important since we use `autodoc` to generate documentation from the code itself,
# and it needs to know where the code is located.

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "create-dash-app CLI"
copyright = "2025, Harlee Quizzagan (HQuizzagan)"
author = "Harlee Quizzagan (HQuizzagan)"
release = "v0.1.dev20251106"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.doctest",  # Includes code snippets in the documentation
    "sphinx.ext.autodoc",  # Automatically generate documentation from docstrings in the code itself
    "sphinx.ext.autosummary",  # Automatically generate summary pages for each module and class
    "sphinx.ext.napoleon",  # Support for Google style docstrings which we use in this project
    "sphinxcontrib.video",  # Support for embedding videos in the documentation
    "sphinx_new_tab_link",  # Open external links in a NEW tab
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for autodoc ----------------------------------------------------
autodoc_typehints = "description"  # Show type hints in descriptions
autodoc_member_order = "bysource"  # Order members by source code order
autodoc_default_options = {
    "members": True,  # Show all members
    "undoc-members": True,  # Show members that are not documented
    "show-inheritance": True,  # Show inheritance relationships
}

autosummary_generate = True  # Automatically generate summary pages for each module and class


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]

# -- Other Configurations ----------------------------------------------------
primary_domain = "py"
video_enforce_extra_source = True
new_tab_link_show_external_link_icon = True

# -- Sphinx Event Hooks ----------------------------------------------------
# These functions run at specific points during the documentation build process.
# See https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx-core-events
# for a complete list of available events.


def setup(app):
    """
    Register event handlers for Sphinx build process.

    This function is automatically called by Sphinx during initialization.
    You can connect functions to various build events here.

    The `app` parameter is the Sphinx application object, which provides:
    - app.connect(event_name, callback) - Register event handlers
    - app.add_config_value() - Add custom configuration options
    - app.add_directive() - Add custom reStructuredText directives
    - app.add_role() - Add custom roles

    Common events you can hook into:
    - 'builder-inited': Fired when the builder is initialized
    - 'autodoc-process-docstring': Fired when processing docstrings (allows modification)
    - 'autodoc-skip-member': Fired to determine if a member should be skipped
    - 'build-finished': Fired when the build completes
    - 'env-purge-doc': Fired when a document is removed from the environment

    Returns:
        dict: Extension metadata including version and parallel build safety flags
    """
    # Example: Run code before the build starts
    # def on_builder_inited(app):
    #     print("Builder initialized!")
    # app.connect('builder-inited', on_builder_inited)

    # Example: Modify docstrings during autodoc processing
    # def modify_docstring(app, what, name, obj, options, lines):
    #     # Modify lines list in-place to change the docstring
    #     if 'DEPRECATED' in ''.join(lines):
    #         lines.insert(0, '.. warning:: This is deprecated')
    # app.connect('autodoc-process-docstring', modify_docstring)

    # Example: Run code after the build completes
    # def on_build_finished(app, exception):
    #     if exception is None:
    #         print("Build completed successfully!")
    # app.connect('build-finished', on_build_finished)

    return {
        "version": "1.0",  # Extension version (for debugging/logging)
        "parallel_read_safe": True,  # Safe for parallel reading (enables parallel builds)
        "parallel_write_safe": True,  # Safe for parallel writing (enables parallel builds)
    }
