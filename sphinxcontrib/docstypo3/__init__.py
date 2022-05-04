"""
    sphinxcontrib.docstypo3
    ~~~~~~~~~~~~~~~~~~~~~~~

    Extend Sphinx behaviour

    :copyright: Copyright 2021 by Martin Bless <martin.bless@mbless.de>
    :license: BSD, see LICENSE for details.
"""

import json
import logging
from typing import Any

import pbr.version
from docutils import nodes
from sphinx.transforms import SphinxTransform

from .utils import get_replacements_from_parsed_string

if False:
    # For type annotations
    from typing import Any, Dict  # noqa
    from sphinx.application import Sphinx  # noqa

__version__ = pbr.version.VersionInfo("sphinxcontrib-docstypo3").version_string()

logger = logging.getLogger(__name__)

substitutions = {}

substitution_keys = {
    #
    # Standard Sphinx settings, [general], (prefix: std_)
    "std_author",
    "std_copyright",
    "std_language",  # "en", two-letter-code
    "std_project",
    "std_release",
    "std_version",
    #
    # sphinxcontrib-docstypo3, [docstypo3-meta], (prefix: dt3m_)
    "dt3m_audience",
    "dt3m_description",
    "dt3m_doctype",   # Demo, Tutorial, Reference, Book
    "dt3m_language",  # "English" readable phrase
    "dt3m_license",
    "dt3m_maintainer",
    "dt3m_website",
    #
    # Sphinx html_theme_options, [html_theme_options], (prefix: hto_)
    "hto_edit_button_type",
    "hto_repo_file_edit_url",
    "hto_project_contact",
    "hto_project_discussions",
    "hto_project_home",
    "hto_project_issues",
    "hto_project_repository",
}


def _config_inited(app, config):
    for k in substitution_keys:
        prefix, name = k.split("_", 1)
        if prefix == "std":
            substitutions[k] = str(getattr(app.config, name, ""))
        elif prefix == "hto":
            substitutions[k] = str(
                getattr(app.config, "html_theme_options", {}).get(name, "")
            )
        elif prefix == "dt3m":
            substitutions[k] = str(
                getattr(app.config, "docstypo3", {}).get("meta", {}).get(name, "")
            )
    logger.debug(f"[{__name__}] substitutions: {substitutions!r}")


class OurSubstitutions(SphinxTransform):
    """
    Replace some substitutions if they aren't defined in the document.
    """

    # non-standard, very early

    default_priority = 190

    def apply(self, **kwargs: Any) -> None:
        # only handle those not otherwise defined in the document
        to_handle = substitution_keys - set(self.document.substitution_defs)
        for ref in self.document.traverse(nodes.substitution_reference):
            refname = ref["refname"]
            parts = refname.rsplit("_", 1)
            # provide: refname, postfix
            # refname: key to substitutions
            # postfix: "" | "_r" | "_json" | "_linked"
            if len(parts) == 1:
                postfix = ""
                fn = str
            else:
                postfix = parts[-1]
                if postfix == "r":
                    refname = parts[0]
                    fn = repr
                elif postfix == "json":
                    refname = parts[0]
                    fn = json.dumps
                elif postfix == "linked":
                    refname = parts[0]
                    fn = str
                else:
                    postfix = ""
                    fm = str

            replacement = None
            if refname in to_handle:
                text = substitutions.get(refname)
                if text is not None:
                    if postfix in ["", "r", "json"]:
                        text = fn(text)
                        replacement = nodes.Text(text, text)
                    elif postfix == "linked":
                        replacement = get_replacements_from_parsed_string(text)
            if replacement:
                ref.replace_self(replacement)


def setup(app):
    app.add_config_value("docstypo3", {}, "env")
    app.add_config_value("docstypo3_composer", {}, "")
    app.add_transform(OurSubstitutions)
    app.connect("config-inited", _config_inited)

    # type: (Sphinx) -> Dict[unicode, Any]
    return {
        "parallel_read_safe": True,
        "version": __version__,
    }
