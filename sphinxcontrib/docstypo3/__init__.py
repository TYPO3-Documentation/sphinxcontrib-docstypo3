"""
    sphinxcontrib.docstypo3
    ~~~~~~~~~~~~~~~~~~~~~~~

    Extend Sphinx behaviour

    :copyright: Copyright 2017 by Martin Bless <martin.bless@mbless.de>
    :license: BSD, see LICENSE for details.
"""

from typing import Any

import pbr.version
from docutils import nodes
from sphinx.transforms import SphinxTransform

if False:
    # For type annotations
    from typing import Any, Dict  # noqa
    from sphinx.application import Sphinx  # noqa
    SphinxTransform
    pbr.version
    TYPE_CHECKING, Any, Dict, Generator, List, Tuple
    nodes


__version__ = pbr.version.VersionInfo("docstypo3").version_string()

substitutions = {}
substitution_keys = {
    "cfg_audience",
    "cfg_author",
    "cfg_copyright",
    "cfg_description",
    "cfg_language",
    "cfg_license",
    "cfg_project",
    "cfg_release",
    "cfg_version",
}

def _config_inited(app, config):
    for k in substitution_keys:
        v = getattr(app.config, k[4:], "")
        substitutions[k] = v


class OurSubstitutions(SphinxTransform):
    """
    Replace some substitutions if they aren't defined in the document.
    """
    # run before the default Substitutions
    default_priority = 212

    def apply(self, **kwargs: Any) -> None:
        # only handle those not otherwise defined in the document
        to_handle = substitution_keys - set(self.document.substitution_defs)
        for ref in self.document.traverse(nodes.substitution_reference):
            refname = ref['refname']
            if refname in to_handle:
                text = substitutions.get(refname, "")
                if not text and refname == 'ctx_author':
                    text = substitutions.get('ctx_t3author', "")
                ref.replace_self(nodes.Text(text, text))

def setup(app):
    app.connect("config-inited", _config_inited)
    app.add_transform(OurSubstitutions)

    # type: (Sphinx) -> Dict[unicode, Any]
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": __version__,
    }
