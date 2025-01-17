Installation
############

There are multiple sources for installing the latest stable version of the Ansys Sphinx Theme. These
include public PyPI, Ansys PyPI, and GitHub.

.. jinja:: install_guide

    .. tab-set::

        .. tab-item:: Public PyPI

            .. code-block::

                python -m pip install ansys-sphinx-theme

        .. tab-item:: Ansys PyPI

            .. code-block::

                PIP_EXTRA_INDEX_URL="https://${PYANSYS_PYPI_PRIVATE_PAT}@pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/simple/"
                python -m pip install ansys-sphinx-theme

        .. tab-item:: GitHub

            .. code-block::

                python -m pip install git+https://github.com/ansys/ansys-sphinx-theme.git@{{ version }}
