Ansys Sphinx Theme documentation |version|
##########################################

The Ansys Sphinx Theme is a custom Ansys-branded theme for use with Sphinx, a documentation
generator for creating project documentation from reStructuredText source files.

This theme is specifically tailored for documentation related to Ansys projects
helping to ensure consistency in its look and feel. Various useful extensions
are included in the theme to make documentation more appealing and user-friendly.

.. jinja:: main_toctree

    .. grid:: 1 2 3 3
        :gutter: 1 2 3 3
        :padding: 1 2 3 3

        .. grid-item-card:: :material-regular:`power_settings_new;1.25em` Getting started
            :link: getting-started
            :link-type: doc

            Learn how to install the Ansys Sphinx Theme.

        .. grid-item-card:: :material-regular:`description;1.25em` User guide
            :link: user-guide
            :link-type: doc

            Learn how to use the capabilities and features of this theme.

        {% if build_examples %}

        .. grid-item-card:: :material-regular:`file_copy;1.25em` Examples
            :link: examples
            :link-type: doc

            Explore examples that show how to integrate third-party extensions with this theme.

        {% endif %}

        .. grid-item-card:: :material-regular:`update;1.25em` Changelog
            :link: changelog
            :link-type: doc

            View the changelog for this project.

.. jinja:: main_toctree

    .. toctree::
       :hidden:
       :maxdepth: 3

       getting-started.rst
       user-guide.rst
       {% if build_examples %}
       examples.rst
       {% endif %}
       changelog
