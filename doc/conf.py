#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# PennyLane documentation build configuration file, created by
# sphinx-quickstart on Tue Apr 17 11:43:51 2018.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.
import sys, os, re

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("_ext"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(".")), "doc"))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = "3.3"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.viewcode",
    "sphinxcontrib.bibtex",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx_automodapi.automodapi",
    "sphinx_copybutton",
    "m2r2",
]

os.environ["SPHINX_BUILD"] = "1"

autosummary_generate = True
autosummary_imported_members = False
automodapi_toctreedirnm = "code/api"
automodsumm_inherited_members = True

# Hot fix for the error: 'You must configure the bibtex_bibfiles setting'
bibtex_bibfiles = ["bibfile.bib"]

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

intersphinx_mapping = {"https://pennylane.ai/qml/": None}
mathjax_path = (
    "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"
)
ignore_warnings = [("code/api/qml_transforms*", "no module named pennylane.transforms")]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "PennyLane"
copyright = "2022, Xanadu Quantum Technologies"
author = "Xanadu Inc."

add_module_names = False

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

import pennylane

# The full version, including alpha/beta/rc tags.
release = pennylane.__version__

# The short X.Y version.
version = re.match(r"^(\d+\.\d+)", release).expand(r"\1")

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# today_fmt is used as the format for a strftime call.
today_fmt = "%Y-%m-%d"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------


# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme = "nature"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "_static/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

# If not "", a "Last updated on:" timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = "%b %d, %Y"

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
html_sidebars = {
    "**": [
        "searchbox.html",
        "globaltoc.html",
    ]
}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ""

# This is the file name suffix for HTML files (e.g., ".xhtml").
# html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   "da", "de", "en", "es", "fi", "fr", "h", "it", "ja"
#   "nl", "no", "pt", "ro", "r", "sv", "tr"
# html_search_language = "en"

# A dictionary with options for the search language support, empty by default.
# Now only "ja" uses this config value
# html_search_options = {"type": "default"}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
# html_search_scorer = "scorer.js"

# Output file base name for HTML help builder.
htmlhelp_basename = "PennyLanedoc"

# -- Xanadu theme ---------------------------------------------------------
html_theme = "xanadu"

# Xanadu theme options (see theme.conf for more information).
html_theme_options = {
    "navbar_logo_path": "_static/logo.png",
    "navbar_wordmark_path": "_static/pennylane.svg",
    # Specifying #19b37b is more correct but does not match the other PL websites.
    "navbar_logo_colour": "#2d7c7f",
    "navbar_home_link": "https://pennylane.ai",
    "navbar_left_links": [
        {
            "name": "Quantum machine learning",
            "href": "https://pennylane.ai/qml/",
        },
        {
            "name": "Demos",
            "href": "https://pennylane.ai/qml/demonstrations.html",
        },
        {
            "name": "Install",
            "href": "https://pennylane.ai/install.html",
        },
        {
            "name": "Plugins",
            "href": "https://pennylane.ai/plugins.html",
        },
        {
            "name": "Documentation",
            "href": "index.html",
            "active": True,
        },
        {
            "name": "Blog",
            "href": "https://pennylane.ai/blog/",
        },
    ],
    "navbar_right_links": [
        {
            "name": "FAQ",
            "href": "https://pennylane.ai/faq.html",
            "icon": "fas fa-question",
        },
        {
            "name": "Support",
            "href": "https://discuss.pennylane.ai/",
            "icon": "fab fa-discourse",
        },
        {
            "name": "GitHub",
            "href": "https://github.com/PennyLaneAI/pennylane",
            "icon": "fab fa-github",
        },
    ],
    "extra_copyrights": [
        "TensorFlow, the TensorFlow logo, and any related marks are trademarks " "of Google Inc."
    ],
    "google_analytics_tracking_id": "UA-130507810-1",
    "border_colour": "#19b37b",
    "prev_next_button_colour": "#19b37b",
    "prev_next_button_hover_colour": "#0e714d",
    "table_header_background_colour": "#edf7f4",
    "text_accent_colour": "#19b37b",
    "toc_marker_colour": "#19b37b",
}

edit_on_github_project = "PennyLaneAI/pennylane"
edit_on_github_branch = "master/doc"

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ("letterpaper" or "a4paper").
    #
    # "papersize": "letterpaper",
    # The font size ("10pt", "11pt" or "12pt").
    #
    # "pointsize": "10pt",
    # Additional stuff for the LaTeX preamble.
    #
    # "preamble": "",
    # Latex figure (float) alignment
    #
    # "figure_align": "htbp",
}

latex_additional_files = ["macros.tex"]

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "PennyLane.tex", "PennyLane Documentation", "Xanadu Inc.", "manual"),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "pennylane", "PennyLane Documentation", [author], 1)]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "PennyLane",
        "PennyLane Documentation",
        author,
        "PennyLane",
        "Xanadu quantum machine learning library.",
        "Miscellaneous",
    ),
]


# ============================================================

# the order in which autodoc lists the documented members
autodoc_member_order = "bysource"

# inheritance_diagram graphviz attributes
inheritance_node_attrs = dict(color="lightskyblue1", style="filled")
