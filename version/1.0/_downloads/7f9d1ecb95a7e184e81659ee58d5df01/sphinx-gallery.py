# Copyright (C) 2021 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# noqa: D205, D400
"""
Sphinx-Gallery
==============

This example shows how to add a new example when using `Sphinx-Gallery
<https://sphinx-gallery.github.io/>`_.

To use Sphinx-Gallery, first install the package with this command:

.. code-block:: bash

        pip install sphinx-gallery

Then, add the package to the ``extensions`` variable in your Sphinx ``conf.py`` file:

.. code-block:: python

        extensions = [
            "sphinx_gallery.gen_gallery",
        ]
"""
###############################################################################
# Plot a simple sphere using PyVista
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This code plots a simple sphere using PyVista.

import pyvista as pv

pv.set_jupyter_backend("html")

sphere = pv.Sphere()
sphere.plot()

###############################################################################
# Plot a simple sphere using PyVista with a plotter

plotter = pv.Plotter(notebook=True)
plotter.add_mesh(sphere, color="white", show_edges=True)
plotter.title = "3D Sphere Visualization"
plotter.show()

###############################################################################
# Render equations using IPython ``math``
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This example shows how to render equations using the IPython ``math`` module.

from IPython.display import Math, display

# LaTeX formatted equation
equation = r"\int\limits_{-\infty}^\infty f(x) \delta(x - x_0) \, dx = f(x_0)"
# Display the equation
display(Math(equation))

###############################################################################
from IPython.display import Latex

Latex(r"This is a \LaTeX{} equation: $a^2 + b^2 = c^2$")

###############################################################################
# Render a table in markdown
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# This is an example to render a table inside the markdown with Sphinx-Gallery.
#
# ====== ====== =======
# A      B      A and B
# ====== ====== =======
# False  False  False
# True   False  False
# False  True   False
# True   True   True
# ====== ====== =======

###############################################################################
# Render a table using pandas

import pandas as pd

# Create a dictionary of data
data = {
    "A": [True, False, True, False],
    "B": [False, True, False, True],
    "C": [True, True, False, False],
}

# Create DataFrame from the dictionary
df = pd.DataFrame(data)

# Display the DataFrame
df.head()

###############################################################################
