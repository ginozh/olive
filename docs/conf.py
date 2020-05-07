#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Olive'
copyright = '2020, Olive Team'
author = 'Olive Team'

# The full version, including alpha/beta/rc tags
release = 'v0.2.0-alpha'
# The short X.Y version
version = release

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    #'sphinx.ext.todo',
    #'sphinx.ext.githubpages',
    'breathe',
    'sphinx.ext.autosectionlabel' # headline IDs for anchor linking
    # Blender:
    #'youtube',
    #'vimeo',
    #'sphinx.ext.mathjax',
    #'sphinx.ext.intersphinx',
    #'404'
]

# Blender:
## Is there a better way to check for PDF building?
#if "latex" in sys.argv:
#    # To convert gif's when making a PDF.
#    extensions.append('sphinx.ext.imgconverter')

# intersphinx_mapping = {'blender_api': ('https://docs.blender.org/api/' + blender_version + '/', None)}

# https://stackoverflow.com/questions/15394347/adding-a-cross-reference-to-a-subheading-or-anchor-in-another-page
autosectionlabel_prefix_document = True # document name + headline as ID?
#autosectionlabel_maxdepth = 2

breathe_projects = { 'doxygen_api': '_doxygen/xml/' }
breathe_default_project = 'doxygen_api'
# What does it actually do? It does not prevent WARNING: Duplicate declaration
# (maybe just because content is referenced multiple times? Or declaration in .h and definition in .cpp?)
# https://github.com/michaeljones/breathe/issues/405 ?
breathe_domain_by_extension = { 'h': 'cpp' }
# Is this supposed to suppress the duplicate declaration warnings, but only for unnamespaced code?
breathe_implementation_filename_extensions = ['.c', '.cc', '.cpp'] # default

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#source_suffix = ['.rst', '.md']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', '_doxygen', 'Thumbs.db', '.DS_Store']
# TODO: allow to skip api docs for faster user documentation turnaround
import os
if os.getenv('SKIP_APIDOCS', None):
    exclude_patterns.append('apidoc')

# The master toctree document.
#master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
#language = None
language = 'en'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    'css/custom.css'
]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#html_sidebars = {}

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#html_theme = 'neo_rtd_theme'
#import sphinx_theme
#html_theme_path = [sphinx_theme.get_html_theme_path()]

html_theme = "sphinx_rtd_theme"

# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
# https://developer.blender.org/diffusion/BM/browse/trunk/blender_docs/manual/conf.py
html_theme_options = {
#   'canonical_url': 'https://olive.readthedocs.org/latest/',
#   'analytics_id': 'UA-XXXXXXX-1',  #  Provided by Google in your dashboard
#   'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
#   'vcs_pageview_mode': '',
#   'style_nav_header_background': 'white',
    # Toc options
#   'collapse_navigation': True,
    'sticky_navigation': True,
#   'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# WARNING: Delete _build folder manually to avoid caching issues (even with make html -a -E)

# Copy of Sphinx 3.0.3 HTML5 translator to patch target and rel for external links in
# https://stackoverflow.com/questions/25583581/add-open-in-new-tab-links-in-sphinx-restructuredtext
from sphinx.writers.html import HTMLTranslator
from docutils import nodes
from docutils.nodes import Element
class PatchedHTMLTranslator(HTMLTranslator):

#   def visit_reference(self, node):
#       if node.get('newtab') or not (node.get('target') or node.get('internal') or 'refuri' not in node):
#           node['target'] = '_blank'
#           node['rel'] = 'noopener noreferrer' # original code does not set rel as attribute!
#       super().visit_reference(node)

    def visit_reference(self, node: Element) -> None:
        atts = {'class': 'reference'}
        if node.get('internal') or 'refuri' not in node:
            atts['class'] += ' internal'
        else:
            atts['class'] += ' external'
            # HACK: Customize behavior (open in new tab, secure site)
            atts['target'] = '_blank'
            atts['rel'] = 'noopener noreferrer'
        if 'refuri' in node:
            atts['href'] = node['refuri'] or '#'
            if self.settings.cloak_email_addresses and atts['href'].startswith('mailto:'):
                atts['href'] = self.cloak_mailto(atts['href'])
                self.in_mailto = True
        else:
            assert 'refid' in node, \
                   'References must have "refuri" or "refid" attribute.'
            atts['href'] = '#' + node['refid']
        if not isinstance(node.parent, nodes.TextElement):
            assert len(node) == 1 and isinstance(node[0], nodes.image)
            atts['class'] += ' image-reference'
        if 'reftitle' in node:
            atts['title'] = node['reftitle']
        if 'target' in node:
            atts['target'] = node['target']
        self.body.append(self.starttag(node, 'a', '', **atts))
 
        if node.get('secnumber'):
            self.body.append(('%s' + self.secnumber_suffix) %
                             '.'.join(map(str, node['secnumber'])))

def setup(app):
    app.set_translator('html', PatchedHTMLTranslator)