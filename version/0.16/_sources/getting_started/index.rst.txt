.. _ref_getting_started:

===============
Getting started
===============
`Sphinx <Sphinx_>`_ is a Python documentation
generator for creating documentation. If you are new to using Sphinx, see
`Sphinx Getting Started <Sphinx_Getting_Started_>`_.

This section explains how to install the Ansys Sphinx theme and then set up your
Sphinx ``conf.py`` file to use this theme to generate your documentation.

Dependencies
------------

Ansys sphinx theme build on top of ``pydata sphinx theme``.
The theme requires the following dependencies:

- `Sphinx <Sphinx_PyPI_>`_
- `pydata-sphinx-theme <PyData_PyPI_>`_
- `Jinja2 <Jinja2_PyPI_>`_

Optional dependencies
---------------------

Ansys Sphinx theme includes optional dependencies for autoapi documentation.
To utilize `sphinx-autoapi` with custom templates provided by the theme,
you need to install the following dependencies:

- `sphinx-autoapi <Sphinx_AutoAPI_PyPI_>`_
- `sphinx-design <Sphinx_Design_PyPI_>`_
- `sphinx-jinja <Sphinx_Jinja_PyPI_>`_

An example page demonstrating autoapi rendering with the Ansys sphinx theme template can
be found on the ``API Reference`` page of the
`PyAnsys Geometry documentation <PyAnsys_Geometry_Docs_>`_.

Install the theme
-----------------
Install the Ansys Sphinx theme with:

.. code::

   pip install ansys-sphinx-theme

For installing the optional dependencies, use:

.. code::

   pip install ansys-sphinx-theme[autoapi]

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

.. LINKS and References

.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _Sphinx_Getting_Started: https://www.sphinx-doc.org/en/master/usage/quickstart.html
.. _Sphinx_PyPI: https://pypi.org/project/Sphinx/
.. _PyData_PyPI: https://pypi.org/project/pydata-sphinx-theme/
.. _Jinja2_PyPI: https://pypi.org/project/Jinja2/
.. _Sphinx_AutoAPI_PyPI: https://pypi.org/project/sphinx-autoapi/
.. _Sphinx_Design_PyPI: https://pypi.org/project/sphinx-design/
.. _Sphinx_Jinja_PyPI: https://pypi.org/project/sphinx-jinja/
.. _PyAnsys_Geometry_Docs: https://geometry.docs.pyansys.com/
