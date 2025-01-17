.. _sphinx-design:

Sphinx design
=============
This example shows how the Ansys Sphinx Theme renders documentation components
using the ``sphinx-design`` extension. For comprehensive information, see its
`documentation <sphinx_design_docs_>`_.

Credits and acknowledgments
---------------------------

The examples presented below are sourced from the Sphinx Design project
Copyright (c) by Chris Sewell (2023),
available at `sphinx design examples <sphinx_design_examples_>`_.
This project is licensed under the MIT License.

.. jinja:: examples

    {% for filename in inputs_examples %}
    {% set title = filename.split('.')[0] %}

    {{ title[0].upper() }}{{ title[1:] }}
    {{ '~' * (title | length) }}

    .. literalinclude:: sphinx_examples/{{ filename }}
       :language: rst

    This directive renders as follows:

    .. include:: sphinx_examples/{{ filename }}

    {% endfor %}
