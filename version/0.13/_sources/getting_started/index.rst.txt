.. _ref_getting_started:

===============
Getting started
===============
`Sphinx <https://www.sphinx-doc.org/en/master/>`_ is a Python documentation
generator for creating documentation. If you are new to using Sphinx, see
`Sphinx Getting Started <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_.

This section explains how to install the Ansys Sphinx theme and then set up your
Sphinx ``conf.py`` file to use this theme to generate your documentation.

Install the theme
-----------------
Install the Ansys Sphinx theme with:

.. code::

   pip install ansys-sphinx-theme

Modify the ``conf.py`` file
---------------------------
To use this theme, modify your Sphinx ``conf.py`` file::

   html_theme = "ansys_sphinx_theme"

Consider using the ``conf.py`` for this repository:

.. literalinclude:: ../conf.py
   :language: python
   :end-before: # ONLY FOR ANSYS-SPHINX-THEME

.. toctree::
   :hidden:
   :maxdepth: 2
