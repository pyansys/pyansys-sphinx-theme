.. _sphinx-design:

Sphinx design
=============
The rendering of sphinx design with ansys sphinx theme.
To access the full documentation for the sphinx design package,
please refer `sphinx design <https://sphinx-design.readthedocs.io/en/latest/index.html>`_.

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
