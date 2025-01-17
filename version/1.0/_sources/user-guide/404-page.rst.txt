:orphan:

.. _ref_user_guide_404_page:

********
404 page
********
Because Sphinx does not create a 404 page by default, you can use the
`sphinx-notfound-page
<https://sphinx-notfound-page.readthedocs.io/en/latest/index.html>`_ extension
for 404 pages. While originally developed to be used with `Read the Docs <https://readthedocs.org/>`_,
this extension can be used in other hosting services. For more
information, see the extension's `documentation <https://sphinx-notfound-page.readthedocs.io/en/latest/how-it-works.html>`_.

Install the extension
---------------------
Install and enable the ``sphinx-notfound-page`` extension with:

.. code-block:: text

    python -m pip install sphinx-notfound-page

Consider adding this extension to your ``requirements_doc.txt`` file.

Add the extension to the ``conf.py`` file
-----------------------------------------
After installing the ``sphinx-notfound-page`` extension, add it to
your ``conf.py`` file:

.. code-block:: python

    # Add the extension
    extensions = [
        ...,
        "notfound.extension",
    ]

Configure your 404 page
-----------------------
You can use the default 404 page that the ``ansys-sphinx-theme`` package supplies
or create and use a custom 404 page.

Use the default 404 page
~~~~~~~~~~~~~~~~~~~~~~~~
To use the default 404 page, you can use the ``generate_404`` function in the
``ansys_sphinx_theme`` module to create and use a custom cover page:

.. code-block:: pycon

    from ansys_sphinx_theme import generate_404


    # Configure sphinx-notfound-page
    notfound_context = {
    'body': generate_404(<organisation_which_the_project_belongs_to>,
            <name_of_the_project>,
            <mail_id_for_the_project>,
            <name_of_team_managing_the_project>
            )
    }

.. _sphinx-notfound-page: https://sphinx-notfound-page.readthedocs.io/en/latest/index.html

Create and use a custom 404 page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To create and use a custom 404 page, do the following:

#. Create a ``404.rst`` file next to the ``conf.py`` file.
#. To suppress the spurious ``document isn't included in any toctree`` Sphinx
   warning, include the ``:orphan:`` attribute at the top of this ``404.rst`` file:

   .. code-block:: rst

        :orphan:

        Error 404 Not Found
        ===================
        The page you are requesting does not exist.

#. Update the ``notfound_template`` variable in the ``conf.py`` to the location of
   your ``404.rst`` file:

   .. code-block:: rst

        # Configure sphinx-notfound-page
        notfound_template = "path/to/404.rst"
