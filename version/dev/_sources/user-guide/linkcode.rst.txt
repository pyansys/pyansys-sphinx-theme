.. _ref_user_guide_extension:

The ``linkcode`` extension
===========================

The ``linkcode`` extension automatically adds *source* links to the documentation for Python, C, C++,
and JavaScript objects. It allows you to link to the source code hosted on GitHub.

To use the ``linkcode`` extension, you must add it to the ``extensions`` variable in your
project's Sphinx ``conf.py`` file:

.. code-block:: python

    extensions = ["ansys_sphinx_theme.extension.linkcode"]

Configuration options
---------------------

The Linkcode extension provides a way to configure its behavior by using certain options within your ``conf.py`` file.
Depending on your preferred approach, you can utilize the direct
configuration options or the ``html_context`` dictionary to streamline your settings.

If both sets of configuration options are given, the direct configuration options (that is, ``link_code_library``,
``link_code_source``, ``link_code_branch``) has
precedence over the corresponding settings in the ``html_context`` dictionary.

Direct configuration options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``link_code_library`` :
  The user/repository name where the source code is hosted. For example, ``ansys/ansys-sphinx-theme``.

- ``link_code_source`` (str, optional, default: ''):
  The relative path of the source code file within the repository. For example, ``src``.

- ``link_code_branch`` (str, optional, default: 'main'):
  The GitHub branch. It can be a specific version like ``main`` or ``dev``.

If the ``link_code_source`` and ``link_code_branch`` options are not provided in the configuration,
the following default values are used:

- ``link_code_source``: An empty string (``''``). This links to the root of the repository.
- ``link_code_branch``: ``main``. This is the default branch name used if no branch is specified.

.. code-block:: python

  # Example of setting direct configuration in example
  link_code_library = "username/repo-name"
  link_code_source = "src"
  link_code_branch = "dev"

Using ``html_context`` dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You also have the option to centralize your GitHub-related configuration by incorporating it
directly into the ``html_context`` dictionary within your ``conf.py`` file. This approach allows you to
minimize redundancy and manage the GitHub-related information more effectively for the extension:

.. code-block:: python

   # Example of setting GitHub-related configuration in conf.py
   html_context = {
       "github_user": "<your-github-org>",
       "github_repo": "<your-github-repo>",
       "github_version": "<your-branch>",
       "source_path": "<path-from-root-to-your-source_file>",
   }

With this setup, you can fine-tune your configuration according to your preferences and requirements,
enhancing the integration of the ``linkcode`` extension into your documentation.