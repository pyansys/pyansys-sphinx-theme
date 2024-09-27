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

"""Module to fuse search."""

import json
import re

from docutils import nodes


class SearchIndex:
    """Class to get search index."""

    def __init__(self, doc_name, app):
        """Initialize the class.

        Parameters
        ----------
        doc_name : str
            Document name.
        app : Sphinx
            Sphinx application.
        version : str
            Version of the document for prefixing the path.
        """
        self._doc_name = doc_name
        self.doc_path = f"{self._doc_name}.html"
        self.env = app.env
        self.doc_title = app.env.titles[self._doc_name].astext()
        self._doc_tree = app.env.get_doctree(self._doc_name)
        self.sections = []

    def iterate_through_docs(self):
        """Iterate through the document."""
        for node in self._doc_tree.traverse(nodes.section):
            self.section_title = node[0].astext()
            self.section_text = "\n".join(
                n.astext()
                for node_type in [nodes.paragraph, nodes.literal_block]
                for n in node.traverse(node_type)
            )
            self.section_anchor_id = _title_to_anchor(self.section_title)
            self.sections.append(
                {
                    "section_title": self.section_title,
                    "section_text": self.section_text,
                    "section_anchor_id": self.section_anchor_id,
                }
            )

    def construct_title_breadcrumbs(self, section_title: str) -> str:
        """Generate title breadcrumbs from the document name."""
        # removing the last part of the doc_name because it is the file name taken from the nodes
        docs_parts = self._doc_name.split("/")[:-1]

        title_string = [
            self.env.titles[doc_part].astext()
            for doc_part in docs_parts
            if doc_part in self.env.titles
        ]

        self.breadcrumbs_title = " > ".join(title_string)

        if self.breadcrumbs_title:
            if self.section_title == self.doc_title:
                return f"{self.breadcrumbs_title} > {section_title}"
            else:
                return f"{self.breadcrumbs_title} > {self.doc_title} > {section_title}"
        else:
            return (
                section_title
                if self.section_title == self.doc_title
                else f"{self.doc_title} > {section_title}"
            )

    @property
    def indices(self):
        """Get search index."""
        for sections in self.sections:
            title_breadcrumbs = self.construct_title_breadcrumbs(sections["section_title"])

            yield {
                "objectID": self._doc_name,
                "href": f"{self.doc_path}#{sections['section_anchor_id']}",
                "title": title_breadcrumbs,
                "section": sections["section_title"],
                "text": sections["section_text"],
            }


def _title_to_anchor(title: str) -> str:
    """Convert title to anchor."""
    return re.sub(r"[^\w\s-]", "", title.lower().strip().replace(" ", "-"))


def create_search_index(app, exception):
    """Create search index for the document in build finished.

    Parameters
    ----------
    app : Sphinx
        Sphinx application.
    exception : Any
        Exception.
    """
    if exception:
        return

    all_docs = app.env.found_docs
    search_index_list = []

    for document in all_docs:
        search_index = SearchIndex(document, app)
        search_index.iterate_through_docs()
        search_index_list.extend(search_index.indices)

    search_index = app.builder.outdir / "_static" / "search.json"
    with search_index.open("w", encoding="utf-8") as index_file:
        json.dump(search_index_list, index_file, ensure_ascii=False, indent=4)
