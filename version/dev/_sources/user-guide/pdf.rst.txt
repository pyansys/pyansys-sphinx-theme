.. _ref_user_guide_pdf_cover:

PDF cover page
==============
For generating a PDF of your documentation, Sphinx uses a default cover
page. However, you can use the ``generate_preamble`` function in the
``ansys_sphinx_theme.latex`` module to create and use a custom cover page:

.. autofunction:: ansys_sphinx_theme.latex.generate_preamble

You use this function to generate the value for the ``preamble`` key in the
``latex_elements`` variable declared in the ``conf.py`` file:

.. code-block:: pycon

    latex_elements = {
        "preamble": ansys_sphinx_theme.latex.generate_preamble(
            <title_of_coverpage>,
            <watermark_for_titlepage>,
            <date_to_be_printed>,
        )
    }

To use the logo and watermark provided by Ansys on the cover page, you must
import them and then add them to the ``latex_additional_files`` dictionary:

.. code-block:: python

    from ansys_sphinx_theme import (
        ansys_logo_white,
        ansys_logo_white_cropped,
        watermark,
    )

.. code-block:: python

    latex_additional_files = [watermark, ansys_logo_white, ansys_logo_white_cropped]

.. jinja:: pdf_guide

    For an example of a rendered PDF cover page, see the
    `PDF documentation <https://sphinxdocs.ansys.com/version/{{ version }}/_static/assets/download/ansys_sphinx_theme.pdf>`_.
