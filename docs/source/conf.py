# -*- coding: utf-8 -*-
# flake8: noqa

import sphinx_rtd_theme
from cryptonite import version as cryptonite

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
]
autodoc_default_flags = [
    'members',
    'private-members',
    'special-members',
    #'undoc-members',
    'show-inheritance'
]

def autodoc_skip_member(app, what, name, obj, skip, options):
    return name.startswith('_') or name.endswith('_')


def setup(app):
    app.connect('autodoc-skip-member', autodoc_skip_member)


templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'Cryptonite'
copyright = u'2016, Planet Earth'
author = u'Planet Earth'
man_pages = [
    'startdocname.rst',
    'name.rst',
    'description.rst',
    'authors.rst',
    'section.rst',
]
man_show_urls = True
version = release = cryptonite.version
language = 'en_US'
exclude_patterns = []
default_role = 'py'  # `~foo` becomes :py:`~foo`
add_function_parentheses = True
add_module_names = False
show_authors = False
pygments_style = 'colorful'
todo_include_todos = True
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']
htmlhelp_basename = 'Cryptonitedoc'
latex_elements = {
}
latex_documents = [
    (master_doc, 'Cryptonite.tex', u'Cryptonite Documentation',
     u'The World', 'manual'),
]
man_pages = [
    (master_doc, 'cryptonite', u'Cryptonite Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'Cryptonite', u'Cryptonite Documentation',
     author, 'Cryptonite', 'One line description of project.',
     'Miscellaneous'),
]
intersphinx_mapping = {'https://docs.python.org/': None}
