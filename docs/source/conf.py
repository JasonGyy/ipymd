# -*- coding: utf-8 -*-
#
# PyGauss documentation build configuration file, created by
# sphinx-quickstart on Sun Jun 14 01:13:38 2015.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os

class Mock(object):
    def __init__(self, *args, **kwargs):
        pass
    def __call__(self, *args, **kwargs):
        return Mock()
    @classmethod
    def __getattr__(cls, name):
        if name in ('__file__', '__path__', '__name__'):
            return '/dev/null'
        elif name[0] == name[0].upper():
            mockType = type(name, (), {})
            mockType.__module__ = __name__
            return Mock()
        else:
            return Mock()        
    def __getitem__(self, index):
        raise IndexError()
    def __mul__(self, other):
        return Mock()

MOCK_MODULES = ['cclib', 'cclib.parser', 'cclib.parser.utils', 
'chemlab', 'chemlab.graphics', 'chemlab.db', 'chemlab.graphics.renderers',
'chemlab.graphics.renderers.base','chemlab.graphics.renderers.sphere',
'chemlab.graphics.renderers.sphere_imp','chemlab.graphics.renderers.point',
'chemlab.graphics.colors', 'chemlab.graphics.buffers', 'chemlab.core',
'chemlab.io', 'chemlab.io.handlers', 'chemlab.graphics.qtviewer',
'chemlab.graphics.buffers', 'chemlab.graphics.shaders', 'chemlab.io.handlers.base',
'chemlab.graphics.camera', 'chemlab.graphics.renderers.wireframe',
'chemlab.graphics.renderers.line',
'chemlab.utils', 'chemlab.qc', 'chemlab.qc.pgbf',
'chemview', 'chemview.widget', 'chemview.utils', 'chemview.marchingcubes',
'paramiko', 'numpy', 'numpy.linalg',
'OpenGL', 'OpenGL.GL',
'matplotlib', 'matplotlib.pyplot', 'matplotlib.cm', 'matplotlib.offsetbox',
'matplotlib.colors', 'mpl_toolkits', 'mpl_toolkits.mplot3d','matplotlib.patches',
'pandas', 'pandas.tools', 'pandas.tools.plotting', 'pandas.core', 'pandas.core.index',
'sklearn', 'sklearn.cluster',
'IPython', 'IPython.display', 'IPython.core', 'IPython.core.display',
'IPython.utils', 'IPython.utils.traitlets',
'scipy', 'scipy.signal', 'scipy.interpolate','scipy.spatial',
'nose', 'nose_parameterized',
]
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = Mock()

import urllib2
import json

git_history = urllib2.urlopen('https://api.github.com/repos/chrisjsewell/ipymd/releases')
git_history_json = json.load(git_history)
with open('history.rst', 'w') as f:
	f.write('Whats New\n')
	f.write('---------\n')
	f.write('\n')
	for r in git_history_json:
		f.write(' '.join([r['tag_name'],'-',r['name'],'\n']))
		f.write('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
		f.write('\n')
		for line in r['body'].split('\n'):
			f.write(' '.join([line, '\n']))
		f.write('\n')

git_issues = urllib2.urlopen('https://api.github.com/repos/chrisjsewell/ipymd/issues')
git_issues_json = json.load(git_issues)
with open('enhancements.rst', 'w') as f:
	f.write('Whats To Come\n')
	f.write('--------------\n')
	f.write('\n')
	for r in git_issues_json:
		if not r["state"] == "open":
			continue
		labels = r['labels']
		for l in labels:
			if l['name'] == 'new feature':
				f.write(' '.join([r['title'],'\n']))
				f.write('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
				f.write('\n')
				for line in r['body'].split('\n'):
					f.write(' '.join([line, '\n']))
				f.write('\n')
				break

import inspect
sys.path.insert(0, os.path.abspath('../..'))
import ipymd

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.dirname(inspect.getfile(pygauss)))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.3'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'ipyMD'
copyright = u'2016, Chris Sewell'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ipymd.__version__
# The full version, including alpha/beta/rc tags.
release = ipymd.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = 'ipyMD'

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/molecule.jpg'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = 'molecule.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'ipyMDdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  ('index', 'ipyMD.tex', u'ipyMD Documentation',
   u'Chris Sewell', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'ipymd', u'ipyMD Documentation',
     [u'Chris Sewell'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'ipyMD', u'ipyMD Documentation',
   u'Chris Sewell', 'ipyMD', 'Analysis of Molecular Dynamics output in the IPython Notebook',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('http://docs.python.org/2.7/', None),
    'numpy': ('http://docs.scipy.org/doc/numpy/', None),
    'scipy': ('http://docs.scipy.org/doc/scipy/reference/', None),
    'matplotlib': ('http://matplotlib.sourceforge.net/', None),
    'pandas': ('http://pandas.pydata.org/pandas-docs/stable/', None),
    'IPython': ('http://ipython.org/ipython-doc/stable/', None),
    'PIL': ('http://pillow.readthedocs.org/', None),
    #'pygauss' : ('http://ipymd.readthedocs.org/en/stable/', None)
    }
autoclass_content = 'init'
# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
