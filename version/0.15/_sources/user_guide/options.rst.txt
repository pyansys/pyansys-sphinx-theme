.. _ref_user_guide_html_theme:

HTML theme options
==================
In the ``conf.py`` file for Sphinx, you can use the ``html_theme_options`` dictionary
to customize the Ansys Sphinx theme.

Show breadcrumbs
----------------
Breadcrumbs make navigation easier. While breadcrumbs are hidden by default,
you can add ``"show_breadcrumbs": True`` to the ``html_theme_options`` dictionary
to show them.

If you want to add additional *root* breadcrumbs, such as to the Ansys
documentation homepage, you add them to the ``html_theme_options`` dictionary as a
list of tuples with the ``"additional_breadcrumbs"`` key. The tuples are of the
form ``("Link text", "url")``.

For example:

.. code:: python

   html_theme_options = {
       "github_url": "https://github.com/ansys/ansys-sphinx-theme",
       "show_prev_next": False,
       "show_breadcrumbs": True,
       "additional_breadcrumbs": [
           ("Ansys", "https://www.ansys.com/"),
       ],
   }

When you are on the documentation's homepage, the breadcrumb shows the homepage
title. Because Sphinx cannot access this title from other documentation pages,
you must use ``html_short_title`` to specify the display text for this breadcrumb.

To ensure a consistent user experience, ensure that the ``html_short_title``
(or optionally ``html_title`` if ``html_short_title`` is not used) is set
to the same value as the title for the main ``index.rst`` page:

.. code:: python

   html_short_title = html_title = "Ansys Sphinx Theme"

If you want to title for the main ``index.rst`` file to show the package version,
include ``|version|`` in the title:

.. code:: python

   html_short_title = html_title = "Ansys Sphinx Theme |version|"

Customize icons
---------------
The navigation bar shows two icons on the right by default. The first is for
switching between light and dark modes. The second is for going to the library's
GitHub repository.

- For comprehensive information on customizing icons, see
  `Configure icon links <https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/header-links.html#add-custom-attributes-to-icon-links>`_
  in the *PyData Theme* documentation.
- For comprehensive information on `Font Awesome <https://fontawesome.com/>`_, an icon
  library and toolkit, see its `documentation <https://fontawesome.com/v6/docs>`_,
  particularly `How To Add Icons <https://fontawesome.com/v6/docs/web/add-icons/how-to>`_.

The following sections explain how you can add icons and hide icons.

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
to the ``hidden_icons`` list:

.. code-block:: pycon

    html_theme_options = {
        "hidden_icons": ["GitHub"],
        ...
    }


If you want to hide all icons, use the ``show_icons`` boolean variable:

.. code-block:: pycon

    html_theme_options = {
        "show_icons": False,
        ...
    }

Use MeiliSearch
----------------

MeiliSearch is an open-source search engine that allows developers to 
easily integrate search functionality into their applications.

To use MeiliSearch in your Sphinx project, you can add a child 
dictionary called ``use_meilisearch`` to the ``html_theme_options``
dictionary in the ``conf.py`` file. 

This dictionary should contain the following keys:

#. ``host``: The host name of your MeiliSearch instance. It is hosted at
    https://backend.search.pyansys.com on port 7700 (default).
    You can set this to an environment variable using 
    ``os.getenv()`` for added security. If no value is provided, the default
    public host for PyAnsys is used.

#. ``api_key``: The API key for your MeiliSearch instance.
   You can also set this to an environment variable using ``os.getenv()``. If no
   value is provided, the default public API key for PyAnsys is used.

#. ``index_uids``: A dictionary that provides a mapping between the unique
   identifier (UID) of an index and its 
   corresponding user-friendly name. Each key-value pair in the dictionary 
   represents an index, with the key being the index UID and the value
   being the index name. The index UID points to an index on the server.


Here is an example configuration for using MeiliSearch in the ``conf.py`` file:

.. code-block:: python

    import os

    use_meilisearch = {
        "host": os.getenv("MEILISEARCH_HOST_NAME", ""),
        "api_key": os.getenv("MEILISEARCH_API_KEY", ""),
        "index_uids": {
            "index-uid of current project": "index name to be displayed",
            "another-index-uid": "index name to be displayed",
        },
    }

If your project features multiple documentation versions, it's crucial to adapt the ``index_uids``
mapping to accommodate different versions. 
To ensure seamless search integration across versions,
use the following format to dynamically generate version-specific index ``UIDs``:

.. code-block:: python

    from ansys_sphinx_theme import convert_version_to_pymeilisearch

    use_meilisearch = {
        "api_key": os.getenv("MEILISEARCH_PUBLIC_API_KEY", ""),
        "index_uids": {
            f"ansys-sphinx-theme-v{convert_version_to_pymeilisearch(__version__)}": "ansys-sphinx-theme",
        },
    }


Here is the example configuration of using MeiliSearch in 
``conf.py`` file of ``ansys-sphinx-theme``:

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

With these options set, your Sphinx project can use MeiliSearch 
to provide search functionality for your documentation.

.. note::

    If you do not set the "use_meilisearch" option,
    ``ansys-sphinx-theme`` uses the default search functionality 
    inherited from the PyData Sphinx Theme.

Cheat sheets
------------

The ``cheatsheet`` HTML theme option can be used to enable a cheat sheet in the Ansys Sphinx theme.

To enable a cheatsheet, in the ``conf.py`` file for your PyAnsys
library, you can add a child dictionary named ``cheatsheet`` to
the ``html_theme_options`` dictionary. 

This dictionary should contain these keys, in the order given:

#. ``url``: URL of the cheat sheet for downloading.
#. ``title``: Title of the cheat sheet.
#. ``thumbnail``: Thumbnail image for the cheat sheet.
#. ``needs_download``: Whether to download the cheat sheet locally during the build. The default is ``False``, in which case the cheat sheet is accessed directly from the provided URL. If ``True``, the cheat sheet is downloaded to the ``_build/html/_static/`` directory. 
#. ``pages``: List of pages to include in the cheat sheet (optional). If no list is provided, the cheat sheet includes the index page of the documentation.

.. code-block:: python

    html_theme_options = (
        {
            "cheatsheet": {
                "url": "<your cheat sheet URL>",
                "title": "<title of your cheat sheet>",
                "thumbnail": "<image URL>",
                "needs_download": True,  # True if you want to download the cheatsheet locally in the ``_build/html/_static/`` directory.
                "pages": "<list of pages to include the cheat sheet on>",  # Optional
            },
        },
    )

Here is an example configuration of using cheatsheet in 
``conf.py`` file of ``PyMAPDL``:

 .. code-block:: python

    html_theme_options = (
        {
            "cheatsheet": {
                "url": "https://cheatsheets.docs.pyansys.com/pymapdl_cheat_sheet.pdf",
                "title": "PyMAPDL cheatsheet",
                "thumbnail": "https://cheatsheets.docs.pyansys.com/pymapdl_cheat_sheet.png",
                "needs_download": True,
                "pages": ["index", "getting_started/learning"],
            },
        },
    )

.. note:: 

    if you set the "needs_download" option, you should provide the "html_static_path" option 
    in the ``conf.py`` file to specify the location of the cheat sheet.

    for example, if you need to download cheat sheet in the ``_build/html/_static/`` directory,
    you should add the following line in the ``conf.py`` file:

    .. code-block:: pycon

        html_static_path = ["_static"]
