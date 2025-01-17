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

   html_short_title = html_title = 'Ansys Sphinx Theme'

If you want to title for the main ``index.rst`` file to show the package version,
include ``|version|`` in the title:

.. code:: python

   html_short_title = html_title = 'Ansys Sphinx Theme |version|'

Customize icons
---------------
The navigation bar shows two icons on the right by default. The first is for
switching between light and dark modes. The second is for going to the library's
GitHub repository.

- For comprehensive information on customizing icons, see
  `Configure icon links <https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/configuring.html?highlight=icons#configure-icon-links>`_
  in the *PyData Theme* documentation.
- For comprehensive information on `Font Awesome <https://fontawesome.com/>`_, an icon
  library and toolkit, see its `documentation <https://fontawesome.com/v6/docs>`_,
  particularly `How To Add Icons <https://fontawesome.com/v6/docs/web/add-icons/how-to#contentHeader>`_.

The following sections explain how you can add icons and hide icons.

Add icons
~~~~~~~~~
In the ``conf.py`` file, the ``html_theme_options`` dictionary has a child ``icon_links``
dictionary. To add icons to the navigation bar, add them to the ``icon_links``
dictionary. For each icon to add, specify its ``name``, the associated ``url``,
the ``icon``, and the ``type``.

This example adds an icon for sending an email:

.. code-block:: python

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

.. code-block:: python

    html_theme_options = {
        "hidden_icons": ["GitHub"],
        ...
    }


If you want to hide all icons, use the ``show_icons`` boolean variable:

.. code-block:: python

    html_theme_options = {
        "show_icons": False,
        ...
    }

