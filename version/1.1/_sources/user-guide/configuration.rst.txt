.. _ref_user_guide_configuration:

Basic configuration
===================

To use the Ansys Sphinx Theme, add the following line to your project's Sphinx ``conf.py`` file:

.. code-block:: python

   html_theme = "ansys_sphinx_theme"

The Ansys Sphinx Theme provides these features:

- `PyAnsys and Ansys logos`_
- `Version switcher`_
- `PDF cover page`_
- `Custom CSS`_

PyAnsys and Ansys logos
~~~~~~~~~~~~~~~~~~~~~~~

The Ansys Sphinx Theme includes the PyAnsys and Ansys logos. All the logos
are available in the
`ansys_sphinx_theme/static/ <static_files_>`_
directory.

To use the logo in both dark and light modes, add the following code to the``html_theme_options`` dictionary in your project's Sphinx ``conf.py`` file:


.. tab-set::

   .. tab-item:: Ansys logo

      .. code-block:: python

         html_theme_options = {
             "logo": "ansys",
         }


   .. tab-item:: PyAnsys logo

      .. code-block:: python

         html_theme_options = {
             "logo": "pyansys",
         }

   .. tab-item:: No logo

      .. code-block:: python

         html_theme_options = {
             "logo": "no_logo",
         }

.. note::

    By default, if ``ansys`` logo is displayed, the logo links to the Ansys website. If the PyAnsys logo is displayed, the logo links to the PyAnsys website.
    If you want to change the link, you can set the ``logo_link`` option in the ``conf.py`` file.

    For example:

    .. code-block:: python

       html_theme_options = {
           "logo": "ansys",
           "logo_link": "https://www.example.com",
       }

.. note::

    If you use the ``logo`` option, make sure to remove the ``html_logo`` option from the ``conf.py`` file.
    ``logo`` option overrides the ``html_logo`` option and display the specified logo.

You can also add a custom logo by specifying the path to the logo file as specified in `pydata-sphinx-theme <pydata_logo_>`_.

For example:

.. code-block:: python

   html_theme_options = {
       "logo": {
           "image_light": "_static/logo-light.png",
           "image_dark": "_static/logo-dark.png",
       }
   }


``favicon``
~~~~~~~~~~~

The ``favicon`` setting specifies the icon that appears in the browser tab. To use the Ansys favicon, add the following code to your project's Sphinx ``conf.py`` file:

.. code-block:: python

    html_favicon = ansys_favicon


Version switcher
~~~~~~~~~~~~~~~~

The Ansys Sphinx Theme includes a version switcher for switching between different versions of the documentation.
To show the version switcher in your documentation, add the following code to your project's Sphinx ``conf.py`` file:

.. code-block:: python

   from ansys_sphinx_theme import get_version_match

   version = "0.1.0"
   switcher_versions = get_version_match(version)
   cname = "your_name"
   html_theme_options = {
       "switcher": {
           "json_url": f"https://{cname}/versions.json",
           "version_match": switcher_version,
       },
   }

The switcher requires a ``versions.json`` file that contains the versions of the documentation and their URLs in the given ``json_url``.
For more information, see `PyAnsys multi-version documentation <dev_guide_multi_version_>`_ in the
*PyAnsys developer's guide*.

PDF cover page
~~~~~~~~~~~~~~

The Ansys Sphinx Theme includes a PDF cover page that you can customize.
To customize the PDF cover page, see :ref:`ref_user_guide_pdf_cover`.

Custom CSS
~~~~~~~~~~

You can add custom CSS to the Ansys Sphinx Theme by creating a directory named ``_static/css`` in
your documentation and adding the following code to your project's Sphinx ``conf.py`` file:

.. code-block:: python

   html_static_path = ["_static"]
   html_css_files = ["css/custom.css"]

Here is an example of a custom CSS file that changes the background color
of the body to black and the text color to white:

.. code-block:: css

   .body {
       background-color: black;
      color: white;
   }

