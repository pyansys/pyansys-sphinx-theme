.. _ref_user_guide_css:

CSS
---
If you need to edit or append to the CSS for the Ansys Sphinx theme,
create a directory named ``_static/css`` next to your ``conf.py`` file and
then create a ``custom.css`` file in this directory.

In this file, place the code for editing or appending to the CSS.
CSS styles in the ``custom.css`` file override the CSS styles in the
Ansys Sphinx theme.

Here is an example that edits the ``body`` element:

.. code::

   body {
    font-family: 'Source Sans Pro', sans-serif;
    color: black;
    padding-top:calc(var(--pst-header-height))
   }
   footer{display:none}
   main{
     overflow: auto;
     height: calc(100vh - 3.8rem);
     overflow-y: scroll;
   }  
   .prev-next-bottom{margin-bottom: 6rem}


Next, in your ``conf.py`` file, add the following:

.. code:: python

    html_static_path = ["_static"]
    html_css_files = ["css/custom.css"]

