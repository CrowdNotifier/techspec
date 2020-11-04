# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import re

# -- Change font size of code blocks in the LaTeX output
from sphinx.highlighting import PygmentsBridge
from pygments.formatters.latex import LatexFormatter

class CustomLatexFormatter(LatexFormatter):
    def __init__(self, **options):
        super(CustomLatexFormatter, self).__init__(**options)
        self.verboptions = r"formatcom=\footnotesize"

PygmentsBridge.latex_formatter = CustomLatexFormatter

# -- Project information -----------------------------------------------------

import git
repo = git.Repo("../")
try:
    branch = repo.active_branch.name
    last_commit = str(repo.head.commit)[:8]
except TypeError:
    # Depending on CI environment, the git things might fail
    branch = ''
    last_commit = ''

# The short X.Y version
version = branch + "/" + last_commit
# The full version, including alpha/beta/rc tags
release = "v0.1.5"

project = u'CrowdNotifier'
copyright = u'2021, EPFL. CC BY-SA 4.0' + ". Version " + release
author = u'CrowdNotifier Team'

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.githubpages',
    'sphinx.ext.imgconverter'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'collapse_navigation': True
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'CrowdNotifierTechnicalSpecification'


# -- Options for LaTeX output ------------------------------------------------

LATEX_MACROS_FILE = "macros.tex.txt"

latex_additional_files = [LATEX_MACROS_FILE]
latex_elements = {
    'papersize': 'a4paper',
    'preamble': r'''
\usepackage{xspace}
\input{macros.tex.txt}
''',
    'figure_align': 'tbp',
    'extraclassoptions': 'openany',
    'fontpkg': r'''
\usepackage{tgtermes}
\usepackage[scale=0.85]{tgheros}
\usepackage{tgcursor}
%\renewcommand\ttdefault{txtt}
''',
    'sphinxsetup': 'hmargin={1.45in,1.45in}, vmargin={1in,1in}, marginpar=1in',
    'fvset': '\\fvset{fontsize=\\small}'
}


# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'CrowdNotifierTechnicalSpecification.tex', u'CrowdNotifier Technical Specification',
     u'Wouter Lueks (SPRING Lab, EPFL) \\and Linus Gasser (C4DT, EPFL) \\and Carmela Troncoso (SPRING Lab, EPFL)', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'CrowdNotifierTechnicalSpecification', u'CrowdNotifierTechnical Specification Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'CrowdNotifierTechnicalSpecification', u'CrowdNotifier Technical Specification Documentation',
     author, 'CrowdNotifierTechnicalSpecification', 'Technical specifications for the CrowdNotifier project, '
                                                    'for all involved parties',
     'Miscellaneous'),
]


# -- Extension configuration -------------------------------------------------

extensions = ['sphinx.ext.mathjax',
              'sphinxcontrib.bibtex']
bibtex_bibfiles = ['sources.bib']

# -- Options for todo extension ----------------------------------------------


latex_macros = ""
with open(LATEX_MACROS_FILE, "r") as macros:
    latex_macros = macros.read()

# Disable some macros that are not supported by MathJax
extra_latex_macros = r"""
\newcommand{\allowbreak}{}
\newcommand{\ensuremath}{}
\newcommand{\xspace}{}
"""

# HTML output specific tweaks
fixes_for_mathjax_macros = r"""
% WARNING: also change this in LATEX_MACROS_FILE
\newcommand{\cnversionstring}{\texttt{"CrowdNotifier_v3"}}
"""

all_macros = latex_macros + extra_latex_macros + fixes_for_mathjax_macros

def macros_to_mathjax(latex_macros):
    macros = {}
    pattern = re.compile(r'^\\newcommand\{\\([^}]+)\}(\[(\d)+\])?\{(.*)\}$')
    for line in latex_macros.split("\n"):
        if "newcommand" not in line:
            continue

        m = pattern.match(line)
        cmd = None
        if m.group(2):
            cmd = [m.group(4), m.group(3)]
        else:
            cmd = m.group(4)
        macros[m.group(1)] = cmd

    return macros

mathjax_config = {
    'showProcessingMessages': 'true',
    'TeX': {
        'Macros': macros_to_mathjax(all_macros)
    },
}

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# Allow numerical references
numfig = True