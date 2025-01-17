# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Module for the Ansys Sphinx theme."""

from itertools import islice, tee
import logging
import os
import pathlib
import re
import subprocess
from typing import Any, Dict, Iterable
import warnings

from docutils import nodes
from sphinx import addnodes
from sphinx.application import Sphinx
import yaml

from ansys_sphinx_theme.extension.linkcode import DOMAIN_KEYS, sphinx_linkcode_resolve
from ansys_sphinx_theme.latex import generate_404
from ansys_sphinx_theme.search import (
    ALL_NODES,
    PARAGRAPHS,
    TITLES,
    create_search_index,
    update_search_config,
)

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    import importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))


# Declare the fundamental paths of the theme
THIS_PATH = pathlib.Path(__file__).parent.resolve()
THEME_PATH = THIS_PATH / "theme" / "ansys_sphinx_theme"
STATIC_PATH = THEME_PATH / "static"
STYLE_PATH = STATIC_PATH / "css"
JS_PATH = STATIC_PATH / "js"
CSS_PATH = STYLE_PATH / "ansys_sphinx_theme.css"
TEMPLATES_PATH = THEME_PATH / "_templates"
AUTOAPI_TEMPLATES_PATH = TEMPLATES_PATH / "autoapi"
LOGOS_PATH = STATIC_PATH / "logos"

ANSYS_LOGO_LINK = "https://www.ansys.com/"
PYANSYS_LOGO_LINK = "https://docs.pyansys.com/"

"""Semantic version regex as found on semver.org:
https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string"""
SEMVER_REGEX = (
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+(>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?"
)

# make logo paths available
ansys_favicon = str((LOGOS_PATH / "ansys-favicon.png").absolute())
ansys_logo_black = str((LOGOS_PATH / "ansys_logo_black_cropped.jpg").absolute())
ansys_logo_white = str((LOGOS_PATH / "ansys_logo_white.pdf").absolute())
ansys_logo_white_cropped = str((LOGOS_PATH / "ansys_logo_white_cropped.pdf").absolute())
page_404 = str((STATIC_PATH / "404.rst").absolute())
pyansys_logo_black = str((LOGOS_PATH / "pyansys-logo-black-cropped.png").absolute())
pyansys_logo_white = str((LOGOS_PATH / "pyansys-logo-white-cropped.png").absolute())
watermark = str((LOGOS_PATH / "watermark.pdf").absolute())
pyansys_logo_dark_mode = str((LOGOS_PATH / "pyansys_logo_transparent_white.png").absolute())
pyansys_logo_light_mode = str((LOGOS_PATH / "pyansys_logo_transparent_black.png").absolute())
ansys_logo_light_mode = str((LOGOS_PATH / "ansys_logo_transparent_black.png").absolute())
ansys_logo_dark_mode = str((LOGOS_PATH / "ansys_logo_transparent_white.png").absolute())

# Cheat sheet extension version
CHEAT_SHEET_QUARTO_EXTENTION_VERSION = "v1"


def get_html_theme_path() -> pathlib.Path:
    """Return list of HTML theme paths.

    Returns
    -------
    pathlib.Path
        Path pointing to the installation directory of the theme.

    """
    return THEME_PATH.resolve()


def get_autoapi_templates_dir_relative_path(path: pathlib.Path) -> str:
    """Return a string representing the relative path for autoapi templates.

    Parameters
    ----------
    path : pathlib.Path
        Path to the desired file.

    Returns
    -------
    str
        A string rerpesenting the relative path to the autoapi templates.

    """
    return os.path.relpath(str(AUTOAPI_TEMPLATES_PATH.absolute()), start=str(path.absolute()))


def get_version_match(semver: str) -> str:
    """Evaluate the version match for the multi-documentation.

    Parameters
    ----------
    semver : str
        Semantic version number in the form of a string.

    Returns
    -------
    str
        Matching version number in the form of a string.

    """
    if "dev" in semver:
        return "dev"
    major, minor, *_ = semver.split(".")
    return ".".join([major, minor])


def setup_default_html_theme_options(app):
    """Set up the default configuration for the HTML options.

    Parameters
    ----------
    app : ~sphinx.application.Sphinx
        Application instance for rendering the documentation.

    Notes
    -----
    This function is the only way to overwrite ``pydata-sphinx-theme``
    configuration. Variables declared in the ``theme.conf`` do not include
    inherited ones.

    """
    # Place all switchers and icons at the end of the navigation bar
    theme_options = app.config.html_theme_options
    # Place all switchers and icons at the end of the navigation bar
    if theme_options.get("switcher"):
        theme_options.setdefault(
            "navbar_end", ["version-switcher", "theme-switcher", "navbar-icon-links"]
        )
    theme_options.setdefault("collapse_navigation", True)
    theme_options.setdefault("navigation_with_keys", True)

    # Update the icon links. If not given, add a default GitHub icon.
    if not theme_options.get("icon_links") and theme_options.get("github_url"):
        theme_options["icon_links"] = [
            {
                "name": "GitHub",
                "url": theme_options["github_url"],
                "icon": "fa-brands fa-github",
            }
        ]
        theme_options["github_url"] = None

    # Add default pygments style options
    if not theme_options.get("pygments_light_style"):
        theme_options["pygments_light_style"] = "friendly"
    if not theme_options.get("pygments_dark_style"):
        theme_options["pygments_dark_style"] = "monokai"


def fix_edit_html_page_context(
    app: Sphinx, pagename: str, templatename: str, context: dict, doctree: nodes.document
) -> None:
    """Add a function that Jinja can access for returning an "edit this page" link .

    This function creates an "edit this page" link for any library.
    The link points to the corresponding file on the main branch.

    Parameters
    ----------
    app : Sphinx
        Sphinx application instance for rendering the documentation.
    pagename : str
        Name of the current page.
    templatename : str
        Name of the template being used.
    context : dict
        Context dictionary for the page.
    doctree : document
        Document tree for the page.

    Notes
    -----
    [1] Originally implemented by `Alex Kaszynski <https://github.com/akaszynski>`_ in
    `PyVista <https://github.com/pyvista/pyvista>`_ ,
    see https://github.com/pyvista/pyvista/pull/4113
    """

    def fix_edit_link_page(link: str) -> str:
        """Transform "edit on GitHub" links to the correct URL.

        This function fixes the URL for the "edit this page" link.

        Parameters
        ----------
        link : str
            Link to the GitHub edit interface.

        Returns
        -------
        str
            Link to the corresponding file on the main branch.
        """
        github_user = context.get("github_user", "")
        github_repo = context.get("github_repo", "")
        github_source = context.get("source_path", "")
        kind = context.get("github_version", "")

        if "_autosummary" in pagename:
            for obj_node in list(doctree.findall(addnodes.desc)):
                try:
                    domain = obj_node.get("domain")
                    for signode in obj_node:
                        if not isinstance(signode, addnodes.desc_signature):
                            continue
                        # Convert signode to a specified format
                        info = {}
                        for key in DOMAIN_KEYS.get(domain, []):
                            value = signode.get(key)
                            if not value:
                                value = ""
                            info[key] = value
                        if not info:
                            continue
                        # This is an API example
                        return sphinx_linkcode_resolve(
                            domain=domain,
                            info=info,
                            library=f"{github_user}/{github_repo}",
                            source_path=github_source,
                            github_version=kind,
                            edit=True,
                        )
                except ValueError as e:
                    logging.debug(f"An error occurred: {e}")  # Log the exception as debug info
                    return link

        elif "api" in pagename:
            for obj_node in list(doctree.findall(addnodes.desc)):
                domain = obj_node.get("domain")
                if domain != "py":
                    return link

                for signode in obj_node:
                    if not isinstance(signode, addnodes.desc_signature):
                        continue

                    fullname = signode["fullname"]
                    modname = fullname.replace(".", "/")

                    if github_source:
                        return f"http://github.com/{github_user}/{github_repo}/edit/{kind}/{github_source}/{modname}.{domain}"  # noqa: E501
                    else:
                        return f"http://github.com/{github_user}/{github_repo}/edit/{kind}/{modname}.{domain}"  # noqa: E501

        else:
            return link

    context["fix_edit_link_page"] = fix_edit_link_page


def update_footer_theme(
    app: Sphinx, pagename: str, templatename: str, context: Dict[str, Any], doctree: nodes.document
) -> None:
    """Update the version number of the Ansys Sphinx theme in the footer.

    Connect to the Sphinx application instance for rendering the documentation,
    and add the current version number of the Ansys Sphinx theme to the page context.
    This allows the theme to update the footer with the current version number.

    Parameters
    ----------
    app : ~sphinx.application.Sphinx
        Application instance for rendering the documentation.
    pagename : str
        The name of the current page.
    templatename : str
        The name of the template being used.
    context : dict
        The context dictionary for the page.
    doctree : ~docutils.nodes.document
        The document tree for the page.
    """
    context["ansys_sphinx_theme_version"] = __version__


def replace_html_tag(app, exception):
    """Replace HTML tags in the generated HTML files.

    Parameters
    ----------
    app : ~sphinx.application.Sphinx
        Application instance for rendering the documentation.
    exception : Exception
        Exception that occurred during the build process.
    """
    if exception is not None:
        return

    build_dir = pathlib.Path(app.builder.outdir).resolve()
    defined_extensions = app.config["extensions"]
    if not any(
        extension in defined_extensions
        for extension in ["autoapi.extension", "ansys_sphinx_theme.extension.autoapi"]
    ):
        return
    api_dir = app.config["autoapi_root"]
    api_path = build_dir / api_dir
    if not api_path.exists():
        return

    file_names = list(api_path.rglob("*.html"))
    for file_name in file_names:
        with pathlib.Path.open(api_dir / file_name, "r", encoding="utf-8") as file:
            content = file.read()
        with pathlib.Path.open(api_dir / file_name, "w", encoding="utf-8") as file:
            modified_content = content.replace("&lt;", "<").replace("&gt;", ">")
            file.write(modified_content)


def configure_theme_logo(app: Sphinx):
    """
    Configure the theme logo based on the theme options.

    Parameters
    ----------
    app : sphinx.application.Sphinx
        Application instance for rendering the documentation.
    """
    # Define logo configurations
    pyansys_logo = {
        "image_dark": pyansys_logo_dark_mode,
        "image_light": pyansys_logo_light_mode,
    }

    ansys_logo = {
        "image_dark": ansys_logo_dark_mode,
        "image_light": ansys_logo_light_mode,
    }
    theme_options = app.config.html_theme_options
    logo_option = theme_options.get("logo")

    if not logo_option:
        theme_options["logo"] = pyansys_logo

    if isinstance(logo_option, str) and logo_option not in {"ansys", "pyansys", "no_logo"}:
        raise ValueError(
            f"Invalid logo option: '{logo_option}'. The logo option must be either 'ansys', 'pyansys', or 'no_logo'"  # noqa: E501
        )

    if logo_option == "ansys":
        theme_options["logo"] = ansys_logo
        theme_options["logo_link"] = theme_options.get("logo_link", ANSYS_LOGO_LINK)
    elif logo_option == "pyansys":
        theme_options["logo"] = pyansys_logo
        theme_options["logo_link"] = theme_options.get("logo_link", PYANSYS_LOGO_LINK)
    elif logo_option == "no_logo":
        theme_options["logo"] = None

    elif isinstance(logo_option, dict):
        theme_options["logo"] = logo_option


def convert_pdf_to_png(pdf_path: pathlib.Path, output_dir: pathlib.Path, output_png: str):
    """
    Convert PDF to PNG images.

    Parameters
    ----------
    pdf_path : pathlib.Path
        Path to the PDF file.
    output_dir : pathlib.Path
        Path to the output directory.
    output_png : str
        Name of the output PNG file.
    """
    try:
        from pdf2image import convert_from_path
    except ImportError as e:
        raise ImportError(
            f"Failed to import `pdf2image`: {e}. Install the package using `pip install pdf2image`"  # noqa: E501
        )
    try:
        images = convert_from_path(pdf_path, 500)
        images[0].save(output_dir / output_png, "PNG")
    except Exception as e:
        raise RuntimeError(
            f"Failed to convert PDF to PNG: {e}, ensure `poppler` is installed. See https://pypi.org/project/pdf2image/"  # noqa: E501
        )


def add_cheat_sheet(
    app: Sphinx, pagename: str, templatename: str, context: Dict[str, Any], doctree: nodes.document
) -> None:
    """Add a cheat sheet to the left navigation sidebar.

    Parameters
    ----------
    app : ~sphinx.application.Sphinx
        Application instance for rendering the documentation.
    pagename : str
        Name of the current page.
    templatename : str
        Name of the template being used.
    context : dict
        Context dictionary for the page.
    doctree : ~docutils.nodes.document
        The doctree.
    """
    cheatsheet_options = app.config.html_theme_options.get("cheatsheet", {})
    pages = cheatsheet_options.get("pages", ["index"])
    pages = [pages] if isinstance(pages, str) else pages
    if cheatsheet_options and any(pagename == page for page in pages):
        sidebar = context.get("sidebars", [])
        sidebar.append("cheatsheet_sidebar.html")
        context["sidebars"] = sidebar


def build_quarto_cheatsheet(app: Sphinx):
    """
    Build the Quarto cheatsheet.

    Parameters
    ----------
    app : sphinx.application.Sphinx
        Application instance for rendering the documentation.
    """
    cheatsheet_options = app.config.html_theme_options.get("cheatsheet", {})

    if not cheatsheet_options:
        return

    cheatsheet_file = cheatsheet_options.get("file", "")
    output_dir = "_static"
    version = cheatsheet_options.get("version", "main")

    if not cheatsheet_file:
        return

    cheatsheet_file = pathlib.Path(app.srcdir) / cheatsheet_file
    file_name = str(cheatsheet_file.name)
    file_path = cheatsheet_file.parent
    output_dir_path = pathlib.Path(app.outdir) / output_dir
    try:
        # Add the cheatsheet to the Quarto project
        subprocess.run(
            [
                "quarto",
                "add",
                f"ansys/pyansys-quarto-cheatsheet@{CHEAT_SHEET_QUARTO_EXTENTION_VERSION}",
                "--no-prompt",
            ],
            cwd=file_path,
            capture_output=True,
            text=True,
        )

        # Render the cheatsheet
        subprocess.run(
            [
                "quarto",
                "render",
                file_name,
                "--to",
                "cheat_sheet-pdf",
                "--output-dir",
                output_dir_path,
                "-V",
                f"version={version}",
            ],
            cwd=file_path,
            capture_output=True,
            text=True,
        )

        # Remove the cheatsheet from the Quarto project
        subprocess.run(
            ["quarto", "remove", "ansys/cheat_sheet", "--no-prompt"],
            cwd=file_path,
            capture_output=True,
            text=True,
        )

        # Remove all supplementary files
        supplementary_files = [
            "_static/slash.png",
            "_static/bground.png",
            "_static/ansys.png",
        ]
        for file in supplementary_files:
            file_path = cheatsheet_file.parent / file
            if file_path.exists():
                file_path.unlink()

        # If static folder is clean, delete it
        if not list(cheatsheet_file.parent.glob("_static/*")):
            cheatsheet_file.parent.joinpath("_static").rmdir()

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to build Quarto cheatsheet: {e}. Ensure Quarto is installed.")

    output_file = output_dir_path / file_name.replace(".qmd", ".pdf")
    app.config.html_theme_options["cheatsheet"]["output_dir"] = f"{output_dir}/{output_file.name}"
    output_png = file_name.replace(".qmd", ".png")
    convert_pdf_to_png(output_file, output_dir_path, output_png)
    app.config.html_theme_options["cheatsheet"]["thumbnail"] = f"{output_dir}/{output_png}"


def check_for_depreciated_theme_options(app: Sphinx):
    """Check for depreciated theme options.

    Parameters
    ----------
    app : sphinx.application.Sphinx
        Application instance for rendering the documentation.
    """
    theme_options = app.config.html_theme_options
    if "use_meilisearch" in theme_options:
        warnings.warn(
            "The 'use_meilisearch' option is deprecated. Remove the option "
            "from your configuration file.",
            DeprecationWarning,
        )


def retrieve_whatsnew_input(app: Sphinx) -> tuple:
    # Get the html_theme_options from conf.py
    config_options = app.config.html_theme_options

    # Get the whatsnew key from the html_theme_options
    whatsnew_options = config_options.get("whatsnew")
    if not whatsnew_options:
        return

    # The source directory of the documentation: {repository_root}/doc/source
    doc_src_dir = app.env.srcdir

    # Get the number of headers to display in the what's new section in the sidebar
    # By default, it's 3
    no_of_headers = whatsnew_options.get("no_of_headers", 3)
    # Get the number of what's new content to display under each minor version in the sidebar.
    # By default, it's 3
    no_of_contents = whatsnew_options.get("no_of_contents", 3)

    # Get the name of the whatsnew.yml file in doc/source. By default, it's "whatsnew"
    whatsnew_file = whatsnew_options.get("whatsnew_file", "whatsnew")
    whatsnew_file = pathlib.Path(doc_src_dir) / f"{whatsnew_file}.yml"

    # Get the name of the changelog file in doc/source. By default, it's "changelog"
    changelog_file = whatsnew_options.get("changelog_file", "changelog")
    changelog_file = pathlib.Path(doc_src_dir) / f"{changelog_file}.rst"

    # Get the pages the whatsnew section should be displayed on. By default, it's changelog
    pages = whatsnew_options.get("pages", ["changelog"])

    whatsnew_config = {
        "no_of_headers": no_of_headers,
        "no_of_contents": no_of_contents,
        "whatsnew_file": whatsnew_file,
        "changelog_file": changelog_file,
        "pages": pages,
    }

    return whatsnew_config


def add_whatsnew_changelog(app, doctree):
    """Create doctree with minor version and what's new content."""
    whatsnew_config = retrieve_whatsnew_input(app)
    # Read the file and get the sections from the file as a list. For example,
    # sections = [<document: <target...><section "getting started; ref-getting-starte ...>]
    sections = doctree.traverse(nodes.document)
    if not sections:
        return

    # Get the file name of the section using section.get("source") and return the section
    # if section.get("source") is equal to the changelog_file
    changelog_doctree_sections = [
        section
        for section in sections
        if section.get("source") == str(whatsnew_config["changelog_file"])
    ]

    # Return if the changelog file sections are not found
    if not changelog_doctree_sections:
        return

    whatsnew_file = whatsnew_config["whatsnew_file"]
    whatsnew_data = get_whatsnew_data(whatsnew_file)

    existing_minor_versions = []
    docs_content = doctree.traverse(nodes.section)

    # Get each section that contains a semantic version number
    version_sections = [node for node in docs_content if re.search(SEMVER_REGEX, node[0].astext())]

    for node in version_sections:
        # Get the semantic version number from the section title link
        next_node = node.next_node(nodes.reference)
        # Get the name of the section title link
        version = next_node.get("name", None)

        if version:
            # Create the minor version from the patch version
            minor_version = ".".join(version.split(".")[:-1])

            if minor_version not in existing_minor_versions:
                # Add minor version to list of existing minor versions
                existing_minor_versions.append(minor_version)

                # Create a section for the minor version
                minor_version_section = nodes.section(
                    ids=[f"version-{minor_version}"], names=[f"Version {minor_version}"]
                )
                # Add the title to the section for the minor version
                minor_version_section += nodes.title("", f"Version {minor_version}")

                # Add "What's New" section under the minor version if the minor version is in
                # the what's new data
                if whatsnew_file.exists() and (minor_version in list(whatsnew_data.keys())):
                    minor_version_whatsnew = add_whatsnew_section(minor_version, whatsnew_data)
                    minor_version_section.append(minor_version_whatsnew)

                # Add the title at the beginning of a section with a patch version
                node.insert(0, minor_version_section)


def get_whatsnew_data(whatsnew_file):
    if whatsnew_file.exists():
        with pathlib.Path.open(whatsnew_file, "r", encoding="utf-8") as file:
            whatsnew_data = yaml.safe_load(file)

        minor_version_whatsnew_data = {}
        for fragment in whatsnew_data["fragments"]:
            # Get the minor version from the fragment version
            whatsnew_minor_version = ".".join(fragment["version"].split(".")[:2])

            # Create an empty list for the minor version if it does not exist
            if whatsnew_minor_version not in minor_version_whatsnew_data:
                minor_version_whatsnew_data[whatsnew_minor_version] = []
            # Append the fragment to the minor version in the whatsnew_data
            minor_version_whatsnew_data[whatsnew_minor_version].append(fragment)

        return minor_version_whatsnew_data


def add_whatsnew_section(minor_version, whatsnew_data):
    """Add the what's new title and content under the minor version."""
    # Add the what's new section and title
    minor_version_whatsnew = nodes.section(ids=[f"version-{minor_version}-whatsnew"])
    minor_version_whatsnew += nodes.title("", "What's New")

    # Add a dropdown under the "What's New" section for each fragment in the whatsnew.yml file
    for fragment in whatsnew_data[minor_version]:
        # Create a dropdown for the fragment
        whatsnew_dropdown = nodes.container(
            body_classes=[""],
            chevron=True,
            container_classes=["sd-mb-3 sd-fade-in-slide-down"],
            design_component="dropdown",
            has_title=True,
            icon="",
            is_div=True,
            opened=False,
            title_classes=[""],
            type="dropdown",
        )

        # Set the title_id for the dropdown
        title_id = fragment["title"].replace(" ", "-").lower()

        # Add the title of the fragment to the dropdown
        whatsnew_dropdown += nodes.rubric(ids=[title_id], text=fragment["title"])

        # Add a line specifying which version the fragment is available in
        version_paragraph = nodes.paragraph("sd-card-text")
        version_paragraph.append(
            nodes.emphasis("", f"Available in v{fragment['version']} and later")
        )
        whatsnew_dropdown += version_paragraph

        # Split content from YAML file into list
        content_lines = fragment["content"].split("\n")

        # Create iterator for the content_lines
        content_iterator = iter(content_lines)

        # Navigate to first line in the iterator
        line = next(content_iterator, None)

        while line is not None:
            if ".. code" in line or ".. sourcecode" in line:
                # Get language after "code::"
                language = line.split("::")[1].strip()
                # Create the code block container node with the language if it exists
                code_block = (
                    nodes.container(classes=[f"highlight-{language} notranslate"])
                    if language
                    else nodes.container()
                )

                # Fill the code block with the following lines until it reaches the end or an
                # unindented line
                code_block, line = fill_code_block(content_iterator, code_block)
                whatsnew_dropdown += code_block
            else:
                # Create the paragraph node
                paragraph = nodes.paragraph("sd-card-text")

                # Fill the paragraph node with the following lines until it reaches
                # the end or a code block
                paragraph, line = fill_paragraph(content_iterator, paragraph, line)
                whatsnew_dropdown += paragraph

        # Append the fragment dropdown to the minor_version_whatsnew section
        minor_version_whatsnew.append(whatsnew_dropdown)

    return minor_version_whatsnew


def fill_code_block(content_iterator: Iterable, code_block: nodes.container) -> nodes.container:
    """Fill the code block.

    Parameters
    ----------
    content_iterator : Iterable
        Iterator for the content lines from the fragments in the whatsnew.yml file.
    code_block : nodes.container
        Container node for the code block.

    Returns
    -------
    nodes.container, str
        Container node for the code block and the next line in the content iterator.
    """
    # classes=["highlight"] is required for the copy button to show up in the literal_block
    highlight_container = nodes.container(classes=["highlight"])

    # Create literal block with copy button
    literal_block = nodes.literal_block(
        classes=["sd-button sd-button--icon sd-button--icon-only sd-button--icon-small"],
        icon="copy",
        label="Copy",
        title="Copy",
    )

    # Move to the first line in the code block (the line after ".. code::")
    next_line = next(content_iterator, None)

    # While the next_line is indented or blank, add it to the code block
    while next_line is not None and (next_line.startswith(" ") or (next_line == "")):
        formatted_line = next_line.lstrip() + "\n"
        # Add the formatted line to the literal block
        literal_block += nodes.inline(text=formatted_line)

        # Break the loop if the end of the content is reached
        if next_line is not None:
            # Move to the next line in the content
            next_line = next(content_iterator, None)
        else:
            break

    # Add the literal block to the highlight container
    highlight_container += literal_block

    # Add the highlight container to the code block
    code_block += highlight_container

    return code_block, next_line


def fill_paragraph(
    content_iterator: Iterable, paragraph: nodes.paragraph, next_line: str
) -> nodes.paragraph:
    """Fill the paragraph node.

    Parameters
    ----------
    content_iterator : Iterable
        Iterator for the content lines from the fragments in the whatsnew.yml file.
    paragraph : nodes.paragraph
        Paragraph node.
    next_line : str
        Next line in the content iterator.

    Returns
    -------
    nodes.paragraph, str
        Paragraph node and the next line in the content iterator.
    """
    # While the next_line is not None and is not a code block, add it to the paragraph
    while next_line is not None and not next_line.startswith(".. "):
        # Regular expressions to find rst links, and single & double backticks/asterisks
        rst_link_regex = r"(`[^<`]+? <[^>`]+?>`_)"
        single_backtick_regex = r"(`[^`]+?`)"
        double_backtick_regex = r"(``.*?``)"
        bold_text_regex = r"(\*\*.*?\*\*)"
        italic_text_regex = r"(\*[^\*]+?\*)"

        # Check if there are rst links, single & double backticks/asterisks in the line
        link_backtick_regex = (
            rf"{rst_link_regex}|"
            rf"{single_backtick_regex}|{double_backtick_regex}|"
            rf"{bold_text_regex}|{italic_text_regex}"
        )

        # Get all matches for rst links, single & double backticks/asterisks in the line
        # Sample: next_line = "The files are **deleted** when the ``GUI`` is closed. For more info"
        # For example, matches = [('', '', '', '**deleted**', ''), ('', '', '``GUI``', '', '')]
        matches = re.findall(link_backtick_regex, next_line)

        if matches:
            # Get all of the matches from the matches list
            # For example, regex_matches = ['**deleted**', '``GUI``']
            regex_matches = [
                element for match in matches for i, element in enumerate(match) if element
            ]

            # Create a regular expression pattern that matches any URL
            # For example, pattern = r"\*\*deleted\*\*|``GUI``"
            pattern = "|".join(map(re.escape, regex_matches))

            # Split the line using the pattern
            # For example, split_lines = ['The files are ', '**deleted**', ' when the ', '``GUI``',
            # ' is closed. For more info']
            split_lines = re.split(f"({pattern})", next_line)

            for line in split_lines:
                if line in regex_matches:
                    # If it matches RST link regex, append a reference node
                    if re.search(rst_link_regex, line):
                        text, url = re.findall(r"`([^<`]+?) <([^>`]+?)>`_", line)[0]
                        if url.startswith("http") or url.startswith("www"):
                            ref_type = "external"
                        else:
                            ref_type = "internal"
                        paragraph.append(
                            nodes.reference(
                                classes=[f"reference-{ref_type}"],
                                refuri=url,
                                href=url,
                                text=text,
                            )
                        )
                    # If it matches single or double backticks, append a literal node
                    elif re.search(single_backtick_regex, line):
                        text = re.findall(r"`([^`]+?)`", line)[0]
                        paragraph.append(nodes.literal(text=text))
                    elif re.search(double_backtick_regex, line):
                        text = re.findall(r"``(.*?)``", line)[0]
                        paragraph.append(nodes.literal(text=text))
                    # If it matches bold text, append a strong node
                    elif re.search(bold_text_regex, line):
                        text = re.findall(r"\*\*(.*?)\*\*", line)[0]
                        paragraph.append(nodes.strong(text=text))
                    # If it matches italic text, append an emphasis node
                    elif re.search(italic_text_regex, line):
                        text = re.findall(r"\*([^\*]+?)\*", line)[0]
                        paragraph.append(nodes.emphasis(text=text))
                else:
                    paragraph.append(nodes.inline(text=line))
        else:
            # Append the next_line as an inline element, unless it is an empty string. If it's an
            # empty string, append a line break
            paragraph.append(nodes.inline(text=next_line)) if next_line != "" else paragraph.append(
                nodes.line(text="\n")
            )

        # Add a space at the end of each line
        paragraph.append(nodes.inline(text=" "))

        # Break the loop if the end of the content is reached
        if next_line is not None:
            # Move to the next line in the content
            next_line = next(content_iterator, None)
        else:
            break

    return paragraph, next_line


def extract_whatsnew(app, doctree, docname):
    """Extract the what's new content from the document."""
    whatsnew_config = retrieve_whatsnew_input(app)

    if docname not in whatsnew_config["pages"]:
        return

    # Get the doctree for the file
    changelog_file = whatsnew_config["changelog_file"].stem
    doctree = app.env.get_doctree(changelog_file)
    docs_content = doctree.traverse(nodes.section)
    html_title = app.config.html_title or app.config.html_short_title or app.config.project

    if not docs_content:
        return

    whatsnew = []
    app.env.whatsnew = []

    # Get a list of nodes whose ids start with "version" that contain "What's new" sections
    versions_nodes = []

    # Find nodes that contain the minor versions and a "What's New" section
    for node in docs_content:
        node_id = node.get("ids")[0]
        # Get the nodes that contain the minor versions: "Version x.y"
        if node_id.startswith("version") and "whatsnew" not in node_id:
            sections = list(node.traverse(nodes.section))
            # If the section contains a "What's New" section, add it to the list of versions
            whatsnew_nodes = [
                section_node
                for section_node in sections
                if section_node.get("ids")[0] == f"{node_id}-whatsnew"
            ]
            if whatsnew_nodes:
                versions_nodes.append(node)

    # Get the version nodes up to the specified number of headers
    versions_nodes = versions_nodes[: whatsnew_config["no_of_headers"]]

    for version_node in versions_nodes:
        # Get the version title (e.g., "Version 0.1")
        version_title = version_node[0].astext()
        # Get the sections under the version node
        sections = list(version_node.traverse(nodes.section))

        # Sections with text that contains "what's new"
        whatsnew_nodes = [node for node in sections if node[0].astext().lower() == "what's new"]

        if not whatsnew_nodes:
            continue

        # Get the children of the "What's New" section
        children = [node for node in whatsnew_nodes[0].traverse(nodes.rubric)]

        # List of ids for each dropdown -> figure out how to match each child in children
        # with its corresponding url
        # ids = [child.get("ids")[0] for child in children]
        # print("ids: ", ids)

        # Filter the displayed children based on the number of content specified in the config
        if len(children) > whatsnew_config["no_of_contents"]:
            children = children[: whatsnew_config["no_of_contents"]]

        contents = {
            "title": f"{html_title} {version_title}",
            "title_url": f"{changelog_file}.html#{version_node.get('ids')[0]}",
            "children": children,
            "url": f"{changelog_file}.html#{whatsnew_nodes[0]['ids'][0]}",
        }

        whatsnew.append(contents)

    app.env.whatsnew = whatsnew


def add_whatsnew_sidebar(app, pagename, templatename, context, doctree):
    """Add what's new section to the context."""
    config_options = app.config.html_theme_options
    whats_new_options = config_options.get("whatsnew")
    if not whats_new_options:
        return

    pages = whats_new_options.get("pages", ["index"])
    if pagename not in pages:
        return

    whatsnew = context.get("whatsnew", [])
    whatsnew.extend(app.env.whatsnew)
    context["whatsnew"] = whatsnew
    sidebar = context.get("sidebars", [])
    sidebar.append("whatsnew_sidebar.html")
    context["sidebars"] = sidebar


def setup(app: Sphinx) -> Dict:
    """Connect to the Sphinx theme app.

    Parameters
    ----------
    app : ~sphinx.application.Sphinx
        Application instance for rendering the documentation.

    Returns
    -------
    Dict
        Dictionary containing application status.

    """
    # Add the theme configuration
    theme_path = get_html_theme_path()
    app.add_html_theme("ansys_sphinx_theme", theme_path)
    app.config.templates_path.append(str(THEME_PATH / "components"))

    # Add default HTML configuration
    setup_default_html_theme_options(app)

    use_ansys_search = app.config.html_theme_options.get("use_ansys_search", True)
    if use_ansys_search:
        update_search_config(app)

    # Verify that the main CSS file exists
    if not CSS_PATH.exists():
        raise FileNotFoundError(f"Unable to locate ansys-sphinx theme at {CSS_PATH.absolute()}")
    app.add_css_file(str(CSS_PATH.relative_to(STATIC_PATH)))
    app.config.templates_path.append(str(TEMPLATES_PATH))
    app.add_js_file("https://cdn.datatables.net/1.10.23/js/jquery.dataTables.min.js")
    app.add_css_file("https://cdn.datatables.net/1.10.23/css/jquery.dataTables.min.css")
    app.add_css_file("https://www.nerdfonts.com/assets/css/webfont.css")
    app.connect("builder-inited", configure_theme_logo)
    app.connect("builder-inited", build_quarto_cheatsheet)
    app.connect("builder-inited", check_for_depreciated_theme_options)
    app.connect("doctree-read", add_whatsnew_changelog)
    app.connect("doctree-resolved", extract_whatsnew)
    app.connect("html-page-context", add_whatsnew_sidebar)
    app.connect("html-page-context", update_footer_theme)
    app.connect("html-page-context", fix_edit_html_page_context)
    # app.connect("html-page-context", fix_toctree)
    app.connect("html-page-context", add_cheat_sheet)
    app.connect("build-finished", replace_html_tag)
    if use_ansys_search:
        app.connect("build-finished", create_search_index)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


__all__ = ["__version__", "generate_404", "get_version_match", "TITLES", "PARAGRAPHS", "ALL_NODES"]
