"""Sphinx documentation configuration file."""

from datetime import datetime
import os
from pathlib import Path
from typing import List

from github import Github
import pyvista
import requests
from sphinx.builders.latex import LaTeXBuilder

from ansys_sphinx_theme import (
    ALL_NODES,
    PARAGRAPHS,
    TITLES,
    __version__,
    ansys_favicon,
    ansys_logo_white,
    ansys_logo_white_cropped,
    generate_404,
    get_version_match,
    latex,
    watermark,
)

THIS_PATH = Path(__file__).parent.resolve()
EXAMPLE_PATH = (THIS_PATH / "examples" / "sphinx_examples").resolve()

# Project information
project = "ansys_sphinx_theme"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS, Inc."
release = version = __version__
cname = os.getenv("DOCUMENTATION_CNAME", "sphinxdocs.ansys.com")
switcher_version = get_version_match(__version__)

# HTML configuration
html_favicon = ansys_favicon
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "Ansys Sphinx Theme"
html_static_path = ["_static"]
templates_path = ["_templates"]

html_context = {
    "github_user": "ansys",
    "github_repo": "ansys-sphinx-theme",
    "github_version": "main",
    "doc_path": "doc/source",
    "page_assets": {
        "examples/table": {
            "needs_datatables": True,
        },
    },
}

html_theme_options = {
    "github_url": "https://github.com/ansys/ansys-sphinx-theme",
    "contact_mail": "pyansys.support@ansys.com",
    "use_edit_page_button": True,
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": get_version_match(__version__),
    },
    "logo": "ansys",
    "static_search": {
        "threshold": 0.2,
        "limit": 7,
        "minMatchCharLength": 3,
    },
    "whatsnew": {
        "no_of_headers": 2,
        "no_of_contents": 3,
        "whatsnew_file": "whatsnew",
        "changelog_file": "changelog",
        "pages": ["changelog"],  # "index"
    },
}

index_patterns = {
    "examples/api/": ALL_NODES,
    "examples/sphinx_examples/": TITLES + PARAGRAPHS,
}


# Sphinx extensions
extensions = [
    "numpydoc",
    "sphinx_design",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx_copybutton",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "notfound.extension",
    "sphinx_jinja",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}

# numpydoc configuration
numpydoc_show_class_members = False
numpydoc_xref_param_type = True
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    "SS04",  # Summary contains heading whitespaces
    "RT02",  # The first line of the Returns section should contain only the type
}

suppress_warnings = ["config.cache"]

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# additional logos for the latex coverpage
LaTeXBuilder.supported_image_types = ["image/png", "image/pdf", "image/svg+xml"]
latex_additional_files = [watermark, ansys_logo_white, ansys_logo_white_cropped]
latex_elements = {"preamble": latex.generate_preamble(html_title)}

# Not found page
notfound_context = {
    "body": generate_404(),
}
notfound_no_urls_prefix = True

# ONLY FOR ANSYS-SPHINX-THEME
exclude_patterns = [
    "links.rst",
    "examples/sphinx-gallery/README.rst",
    "examples/gallery-examples/*.ipynb",
    "sg_execution_times.rst",
]
rst_epilog = ""
with Path.open(THIS_PATH / "links.rst", "r") as f:
    rst_epilog += f.read()


linkcheck_ignore = [
    r"https://sphinxdocs.ansys.com/version/*",
]
if switcher_version != "dev":
    linkcheck_ignore.append(
        f"https://github.com/ansys/ansys-sphinx-theme/releases/tag/v{__version__}"
    )


# Configure the Jinja contexts

jinja_contexts = {
    "install_guide": {
        "version": f"v{version}" if not version.endswith("dev0") else "main",
    },
    "pdf_guide": {"version": get_version_match(__version__)},  # noqa: E501
}


def extract_example_links(
    repo_fullname: str, path_relative_to_root: str, exclude_files: List[str] = []
) -> List[str]:
    """
    Extract example links from a specific GitHub repository.

    Parameters
    ----------
    repo_fullname : str
        Fullname of the repository to extract example links from.
    path_relative_to_root : str
        Path relative to the root of the repository to extract example links from.
    exclude_files : list of str
        A list of files to exclude from the returned example links.

    Returns
    -------
    list
        List of example links.
    """
    g = Github()
    repo = g.get_repo(repo_fullname)
    contents = repo.get_contents(path_relative_to_root)
    if not isinstance(contents, list):
        contents = [contents]
    example_links = []
    for content in contents:
        if content.type == "dir":
            example_links.extend(extract_example_links(repo_fullname, content.path, exclude_files))
        elif content.type == "file":
            if content.name not in exclude_files:
                example_links.append(content.download_url)

    return example_links


def download_and_process_files(example_links: List[str]) -> List[str]:
    """Download and process a series of example files.

    This function downloads a series of example files using a
    list of links and processes each file.

    Parameters
    ----------
    example_links : List[str]
        List of links to the example files to be downloaded.

    Returns
    -------
    list
        List of the names of the processed files.
    """
    file_names = []
    for link in example_links:
        file_name = link.split("/")[-1]
        file_path = str((EXAMPLE_PATH / file_name).absolute())
        with open(file_path, "wb") as f:  # noqa: PTH123
            response = requests.get(link)
            content = response.content.decode()
            lines = content.splitlines()
            # Replace the "target" string with the file name in the example files
            f.write("\n".join([line.replace("target", file_name) for line in lines]).encode())
        file_names.append(file_name)

    return file_names


# Skip building examples if desired
BUILD_EXAMPLES = True if os.environ.get("BUILD_EXAMPLES", "true") == "true" else False
jinja_contexts["main_toctree"] = {"build_examples": BUILD_EXAMPLES}

if not BUILD_EXAMPLES:
    exclude_patterns.extend(["examples.rst", "examples/**", "examples/api/**"])


else:
    # Autoapi examples
    extensions.append("ansys_sphinx_theme.extension.autoapi")
    html_theme_options["ansys_sphinx_theme_autoapi"] = {
        "project": project,
        "directory": "src/ansys_sphinx_theme/examples",
        "output": "examples/api",
        "own_page_level": "function",
        "package_depth": 1,
    }

    # Gallery of examples
    extensions.extend(["nbsphinx", "sphinx_gallery.gen_gallery"])
    sphinx_gallery_conf = {
        # path to your examples scripts
        "examples_dirs": ["examples/sphinx-gallery"],
        # path where to save gallery generated examples
        "gallery_dirs": ["examples/gallery-examples"],
        # Pattern to search for example files
        "filename_pattern": r"sphinx_gallery\.py",
        # Remove the "Download all examples" button from the top level gallery
        "download_all_examples": False,
        # Modules for which function level galleries are created.  In
        "image_scrapers": ("pyvista", "matplotlib"),
        "default_thumb_file": "source/_static/pyansys_light_square.png",
    }

    nbsphinx_prolog = """
Download this example as a :download:`Jupyter notebook </{{ env.docname }}.ipynb>`.

----
"""
    nbsphinx_execute = "always"
    nbsphinx_thumbnails = {
        "examples/nbsphinx/jupyter-notebook": "_static/pyansys_light_square.png",
    }

    pyvista.BUILDING_GALLERY = True

    # Third party examples
    example_links = extract_example_links(
        "executablebooks/sphinx-design",
        "docs/snippets/rst",
        exclude_files=["article-info.txt"],
    )
    file_names = download_and_process_files(example_links)

    admonitions_links = extract_example_links(
        "pydata/pydata-sphinx-theme",
        "docs/examples/kitchen-sink/admonitions.rst",
    )

    admonitions_links = download_and_process_files(admonitions_links)
    todo_include_todos = True  # admonition todo needs this to be True

    jinja_contexts["examples"] = {"inputs_examples": file_names}
    jinja_contexts["admonitions"] = {"inputs_admonitions": admonitions_links}
