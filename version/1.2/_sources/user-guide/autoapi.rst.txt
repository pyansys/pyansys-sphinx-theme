.. _ref_user_guide_autoapi:

Sphinx AutoAPI
==============

To use Sphinx AutoAPI with the Ansys Sphinx Theme, you must
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
- ``ignore``: The list of directories to ignore. By default, this is empty.
- ``add_toctree_entry``: If set to ``True``, the autoapi extension adds the generated files to the TOC tree.
  By default, this is set to ``False``.
- ``package_depth``: The depth of the package. By default, this is set to ``3``. This is the ``namespace`` depth of the package.
  For example, if the package is ``ansys``, the depth is ``1``. If the package is ``ansys.foo``, the depth is ``2``.
- ``member_order``: The order to document members. By default, this is set to ``bysource``. Other options include
  ``alphabetical``, which orders members by their name (case sensitive), or ``groupwise``, which orders members by their type
  and alphabetically.

All these options can be set in the ``conf.py`` file of your Sphinx project.

.. code:: python

    html_theme_options = {
        "ansys_sphinx_theme_autoapi": {
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
            "ignore": [],
            "add_toctree_entry": False,
            "package_depth": 3,
            "member_order": "bysource",
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


