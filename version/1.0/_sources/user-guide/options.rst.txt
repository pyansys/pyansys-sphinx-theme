.. _ref_user_guide_html_theme:

HTML theme options
==================

In the Sphinx configuration (``conf.py``) file in the ``doc`` directory, you can use the
``html_theme_options`` dictionary to customize the Ansys Sphinx theme.

Show breadcrumbs
----------------

Showing breadcrumbs at the top of your documentation pages makes navigation easier.
Breadcrumbs are shown by setting ``"show_breadcrumbs": True``. To add additional
*root* breadcrumbs, ``"additional_breadcrumbs"`` is set to a list of tuples in
this form: ``("Link text", "url")``.

This ``html_theme_options`` dictionary show breadcrumbs, including a root breadcrumb
for the documentation landing page for the Ansys repository:

.. code:: python

   html_theme_options = {
       "github_url": "https://github.com/ansys/ansys-sphinx-theme",
       "show_prev_next": False,
       "show_breadcrumbs": True,
       "additional_breadcrumbs": [
           ("PyAnsys", "https://docs.pyansys.com/"),
       ],
   }

When you are on the landing page for your documentation, the breadcrumb shows the title for this
page. However, Sphinx cannot access this title from other documentation pages. Thus, after
``html_theme_options`` dictionary, you must set ``html_short_title`` to the display text to
use for this breadcrumb.

To ensure a consistent user experience, always set the ``html_short_title``
(or optionally ``html_title`` if ``html_short_title`` is not used) to the library name.

For example, in the ``conf.py`` file for the Ansys Sphinx Theme, this line is added
after the ``html_theme_options`` dictionary:

.. code:: python

   html_short_title = html_title = "Ansys Sphinx Theme"

If you want the title for your documentation's main ``index.rst`` file to show the version,
include ``|version|`` in the title:

.. code:: python

   html_short_title = html_title = "Ansys Sphinx Theme |version|"


Add and hide icons in the navigation bar
----------------------------------------

The navigation bar shows two icons on the right by default. The first is for
switching between light and dark modes. The second is for going to the library's
GitHub repository.

- For comprehensive information on adding custom link behavior, see
  `Add custom attributes to icon links <https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/header-links.html#add-custom-attributes-to-icon-links>`_
  in the PyData Theme documentation.
- For comprehensive information on how to use Font Awesome to add icons, see `How To Add Icons <https://fontawesome.com/v6/docs/web/add-icons/how-to>`_
  in the Font Awesome documentation.

The following sections explain how to add icons and hide icons.

Add icons
~~~~~~~~~

In the ``conf.py`` file, the ``html_theme_options`` dictionary has a child ``icon_links``
dictionary. To add icons to the navigation bar, add them to the ``icon_links``
dictionary. For each icon to add, specify its ``name``, the associated ``url``,
the ``icon``, and the ``type``.

This example adds an icon for sending an email:

.. code-block:: pycon

    html_theme_options = {
     "icon_links": [
         dict(name="Mail", url="mailto:me", icon="fas fa-envelope")
     ],
     ...
    }

Hide icons
~~~~~~~~~~

To hide icons so that they do not show in the navigation bar, add their names
to the ``hidden_icons`` dictionary:

.. code-block:: pycon

    html_theme_options = {
        "hidden_icons": ["GitHub"],
        ...
    }


If you want to hide all icons, use the ``show_icons`` Boolean variable:

.. code-block:: pycon

    html_theme_options = {
        "show_icons": False,
        ...
    }

Use MeiliSearch
----------------

MeiliSearch is an open source search engine that allows developers to
easily integrate search functionality into their applications.

To use MeiliSearch in your documentation, in the ``conf.py`` file,
a child dictionary named ``use_meilisearch``is added to the ``html_theme_options``
dictionary.

This dictionary contains these keys, in the order given:

#. ``host``: Host name of your MeiliSearch instance. If no value is provided,
   the default public host for PyAnsys is used: ``https://backend.search.pyansys.com``
   on port ``7700``. If added security is needed, you can use the ``os.getenv()`` function
   to set the instance using an environment variable.

#. ``api_key``: API key for your MeiliSearch instance. If no value is provided,
   the default public API key for PyAnsys is used. If added security is needed,
   you can use the ``os.getenv()`` function to set the key using an environment
   variable.

#. ``index_uids``: Dictionary that provides the mapping between the unique
   identifier (UID) of an index and its corresponding user-friendly name.
   Each key-value pair in the dictionary represents an index, with the key
   being the index UID and the value being the index name. The index UID
   points to an index on the server.

Here is an example of how to configure MeiliSearch for use in the ``conf.py`` file:

.. code-block:: python

    import os

    use_meilisearch = {
        "host": os.getenv("MEILISEARCH_HOST_NAME", ""),
        "api_key": os.getenv("MEILISEARCH_API_KEY", ""),
        "index_uids": {
            "index-uid of current project": "index name to display",
            "another-index-uid": "index name to display",
        },
    }


If your project features multiple documentation versions, it's crucial to adapt the
``index_uids`` mapping to accommodate different versions. To ensure seamless search
integration across versions, use the following format to dynamically generate
version-specific index ``UIDs``:

.. code-block:: python

    from ansys_sphinx_theme import convert_version_to_pymeilisearch

    use_meilisearch = {
        "api_key": os.getenv("MEILISEARCH_PUBLIC_API_KEY", ""),
        "index_uids": {
            f"ansys-sphinx-theme-v{convert_version_to_pymeilisearch(__version__)}": "ansys-sphinx-theme",
        },
    }


Here is an example configuration of how to configure MeiliSearch in the ``conf.py`` file
for the Ansys Sphinx Theme:

.. code-block:: python

    import os

    html_theme_options = {
        "use_meilisearch": {
            "index_uids": {
                "ansys-sphinx-theme-sphinx-docs": "ansys-sphinx-theme",
                "pyansys-docs-all-public": "PyAnsys",
            },
        },
    }


With these options set, MeiliSearch is available for performing searches of
your documentation.

.. note::

    If you do not set the ``use_meilisearch`` dictionary, the
    Ansys Sphinx Theme uses the default search functionality
    inherited from the PyData Sphinx Theme.

Cheat sheets
------------

If a cheat sheet has been created for your PyAnsys library, with ``quarto``, you can
add it to the left navigation pane of your documentation.

In the ``html_theme_options`` dictionary, you add a child dictionary named ``cheatsheet``
that contain these keys, in the order given:

#. ``file``: File name including the extension of the cheat sheet. If the file is inside a directory,
   include the directory name relative to the root of the documentation. For example, if the cheat sheet
   is in the ``getting_started`` directory, the file name is ``getting_started/cheat_sheet.qmd``.
#. ``title``: Title of the cheat sheet to be displayed in the left navigation pane.
#. ``pages``: List of names for the pages to include the cheat sheet on. If no value is provided,
   the cheat sheet is displayed only on the main ``index.html`` file.

Here is an example of how to add the ``cheatsheet`` dictionary to the `html_theme_options`` dictionary:

.. code-block:: python

    html_theme_options = (
        {
            "cheatsheet": {
                "file": "<file name including the extension of the cheat sheet>",
                "pages": "<list of names for the pages to include the cheat sheet on>",  # Optional
            },
        },
    )

Here is an example of how to show a thumbnail of a PyMAPDL cheat sheet in the left navigation pane of its
main ``index.rst`` file and the ``learning.rst`` file in its "Getting started" section:

.. code-block:: python

    html_theme_options = (
        {
            "cheatsheet": {
                "file": "getting_started/cheat_sheet.qmd",
                "pages": ["index", "getting_started/learning"],
            },
        },
    )

.. note::

    To use this feature, you must have the `quarto <https://quarto.org/>` package installed. To create thumbnails of generated PDF files,
    the theme is using `pdf2image`. So you should have the ``poppler`` package installed in your system.
    For more information, see the `pdf2image documentation <https://pypi.org/project/pdf2image/>`_.
