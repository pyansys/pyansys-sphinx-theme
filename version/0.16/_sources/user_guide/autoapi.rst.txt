.. _ref_user_guide_autoapi:

``ansys-sphinx-theme`` autoapi extension
========================================

Using ``sphinx-autoapi`` to generate API documentation
------------------------------------------------------

`sphinx-autoapi <https://github.com/readthedocs/sphinx-autoapi/>`_ is a tool that automatically generates API documentation from your source code.
It is a great way to keep your documentation up-to-date with your codebase.

The ``ansys-sphinx-theme`` includes a set of custom templates for ``sphinx-autoapi`` that is designed
to match the look and feel of the rest of the PyAnsys documentation.

Dependencies required
~~~~~~~~~~~~~~~~~~~~~

To use ``sphinx-autoapi`` with the ``ansys-sphinx-theme``, you need to install the ``autoapi`` target
of the theme. This can be done by defining your ``ansys-sphinx-theme`` dependency as
``ansys-sphinx-theme[autoapi]`` in your project's requirements location.

For example, if you are using a ``requirements.txt`` file, you would define your dependency as follows:

.. code-block: text

    ansys-sphinx-theme[autoapi]==X.Y.Z

If you are using a ``pyproject.toml`` file, you would define your dependency as follows:

.. code:: toml

    # For a typical PyAnsys pyproject.toml file
    [project.optional-dependencies]
    doc = [
        "ansys-sphinx-theme[autoapi]==X.Y.Z",
    ]

Configuring the Sphinx project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use ``sphinx-autoapi`` with the ``ansys-sphinx-theme``, and benefit from the shipped
templates, you need to add the following configuration to your Sphinx project's ``conf.py`` file.

.. code:: python

    from pathlib import Path

    from ansys_sphinx_theme import get_autoapi_templates_dir_relative_path

    ...

    # Configuration for Sphinx autoapi
    autoapi_type = "python"
    autoapi_dirs = ["../../src/ansys"]
    autoapi_root = "api"
    autoapi_options = [
        "members",
        "undoc-members",
        "show-inheritance",
        "show-module-summary",
        "special-members",
    ]
    autoapi_template_dir = get_autoapi_templates_dir_relative_path(Path(__file__))
    autoapi_python_use_implicit_namespaces = True
    autoapi_keep_files = True
    autoapi_own_page_level = "class"


The above configuration generates the API documentation for your package in the ``src`` directory
and places the generated files in the ``api`` directory. These files are based on the
``ansys-sphinx-theme`` templates. If you want to customize some of the previous options, you can
do so by modifying the configuration above. The line of code declaring the desired set of templates is the following one:

.. code:: python

    autoapi_template_dir = get_autoapi_templates_dir_relative_path(Path(__file__))


``ansys_sphinx_theme_autoapi`` theme options and extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use the ``autoapi`` along with the ``ansys-sphinx-theme``, you need to
add ``ansys_sphinx_theme.extension.autoapi`` to the ``extensions`` list in your ``conf.py`` file
and set the ``ansys_sphinx_theme_autoapi`` theme options in the ``html_theme_options`` dictionary.

- ``project``: The name of the project.
- ``output``: The path to the directory where the generated files are placed.
  By default, this is set to the ``api`` directory.
- ``templates``: The path to the directory containing the custom templates for ``sphinx-autoapi``.
  By default, this is set to the ``autoapi_templates`` directory in the theme package.
- ``directory``: The path to the directory containing the source code with respect to the ``conf.py`` file.
  By default, this is set to the ``src/ansys`` directory.
- ``use_implicit_namespaces``: If set to ``True``, the autoapi extension use `implicit namespaces`.
  By default, this is set to ``True``.
- ``keep_files``: If set to ``True``, the autoapi extension keeps the generated files.
  By default, this is set to ``True``.
- ``own_page_level``: The level of the page where the autoapi extension places the content of the class.
  By default, this is set to ``class``.
- ``type``: The type of the autoapi extension. By default, this is set to ``python``.
- ``options``: The options to pass to the autoapi extension. By default,
  this is set to ``["members", "undoc-members", "show-inheritance", "show-module-summary", "special-members"]``.
- ``class_content``: The content of the class. By default this is set to ``class``.

All these options can be set in the ``conf.py`` file of your Sphinx project.

.. code:: python

    html_theme_options = {
        "ansys-sphinx-theme-autoapi": {
            "project": "My Project",
            "output": "api",
            "directory": "src/ansys",
            "use_implicit_namespaces": True,
            "keep_files": True,
            "own_page_level": "class",
            "type": "python",
            "options": [
                "members",
                "undoc-members",
                "show-inheritance",
                "show-module-summary",
                "special-members",
            ],
            "class_content": "class",
        }
    }

You need to add ``ansys_sphinx_theme.extension.autoapi`` to the ``extensions`` list in your ``conf.py`` file:

.. code:: python

    extensions = [
        "ansys_sphinx_theme.extension.autoapi",
    ]

The complete configuration for ``sphinx-autoapi`` in your ``conf.py`` file should look like this:

.. code:: python


    html_theme_options = {
        "ansys_sphinx_theme_autoapi": {
            "project": "My Project",
            "output": "api",
            "use_implicit_namespaces": True,
            "directory": "src/ansys",
            "keep_files": True,
            "own_page_level": "class",
            "type": "python",
            "options": [
                "members",
                "undoc-members",
                "show-inheritance",
                "show-module-summary",
                "special-members",
            ],
            "class_content": "class",
        }
    }

    extensions = [
        "ansys_sphinx_theme.extension.autoapi",
    ]


