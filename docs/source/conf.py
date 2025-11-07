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
html_static_path = ["_static", "assets"]

# -- Other Configurations ----------------------------------------------------
primary_domain = "py"
