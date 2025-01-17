.. _admonitions:

Admonitions
===========

Admonitions are specially formatted blocks that highlight important information in the documentation.
This page shows how the Ansys Sphinx Theme renders admonitions.

The examples shown below are derived from the PyData Sphinx Theme project, copyrighted by pandas, 2018.
Original examples can be found in `Examples <pydata_examples_>`_ in
the PyData Sphinx Theme documentation.
These examples are licensed under the BSD 3-Clause License.

The examples included below in this page were originally copyrighted and licensed as follows:

- Copyright (c) 2021, Pradyun Gedam. Licensed under the Creative Commons Attribution-ShareAlike 4.0 International License
  (SPDX-License-Identifier: CC-BY-SA-4.0), as specified by the PyData Sphinx Theme in their examples.


.. jinja:: admonitions

    {% for filename in inputs_admonitions %}

    .. include:: sphinx_examples/{{ filename }}

    {% endfor %}

