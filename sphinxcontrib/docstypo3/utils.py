import json

import docutils
import docutils.core
import docutils.frontend
from docutils import nodes
from docutils.parsers.rst import states


def json_safe_dict(d):
    """Deep copy a dict and stringify JSON incompatible values."""
    result = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = json_safe_dict(v)
        else:
            try:
                json.dumps(v)
            except TypeError:
                v = f"{STRINGIFIED:}{v}"
        result[k] = v
    return result


class SettingsFaker:
    """Simulate a settings object for docutils."""

    def __init__(self):
        self._stats = {}
        self.__dict__.update({
            # Docutils' RST parser references - at least - these settings
            # attributes.
            "character_level_inline_markup": False,
            "debug": 0,
            "error_encoding": "utf-8",
            "error_encoding_error_handler": "backslashreplace",
            "halt_level": 4,
            "input_encoding": "unicode",
            "language_code": "en",
            "output_encoding": "unicode",
            "pep_references": None,
            "raw_enabled": 1,
            "report_level": 2,
            "rfc_references": None,
            "tab_width": 3,
            "warning_stream": None,
        })

    def __getattr__(self, item):
        self._stats[item] = self._stats.get(item, 0) + 1
        return None


def parse_rst_string(input):
    settings = SettingsFaker()
    parser = docutils.parsers.rst.Parser()
    document = docutils.utils.new_document("string", settings)
    parser.parse(input, document)
    return document


def char_at(s, p):
    if p < 0 or p >= len(s):
        return None
    else:
        return s[p]


def iter_chunks(s, hrefs):
    """Split the string into chunks according to list of hrefs.

    Behavior:
    https://example.org                   →  <a href="https://example.org">https://example.org</a>
    (https://example.org)                 →  <a href="https://example.org">https://example.org</a>
    [  ](https://example.org)             →  <a href="https://example.org">https://example.org</a>
    <https://example.org>                 →  &lt;<a href="https://example.org">https://example.org</a>&gt;
    Home (https://example.org)            →  <a href="https://example.org">Home</a>
    Text [linktext](https://example.org)  →  Text <a href="https://example.org">linktext</a>

    """

    # yield linktext, href, healthy

    healthy = True

    if not s.strip():
        yield s, None, healthy
        return

    for e, href in enumerate(hrefs):
        if not s.strip():
            # href but empty s encountered
            healthy = False
            yield s, None, healthy
            return
        # be cautious
        href = href.strip()
        if href.strip():
            p = s.find(href)
            if p == -1:
                # href does not occur
                healthy = False
            elif p == 0:
                # no linktext, so link to itself
                yield href, href, healthy
                s = s[len(href):]
            else:
                p_before = p - 1
                p_next = p + len(href)
                p_right_bracket = p - 2
                char_right_bracket = char_at(s, p_right_bracket)
                char_before = char_at(s, p_before)
                char_next = char_at(s, p_next)
                if char_before == "(" and char_next == ")":
                    p_left_bracket = None
                    if char_right_bracket == "]":
                        for i in range(p_right_bracket - 1, -1, -1):
                            if char_at(s, i) == "[":
                                p_left_bracket = i
                                break

                    if p_left_bracket is not None:
                        # abc (bcd)[url]
                        text = s[0:p_left_bracket]
                        if len(text):
                            yield text, None, healthy
                        linktext = s[p_left_bracket + 1: p_right_bracket]
                        if not linktext.strip():
                            linktext = href
                        yield linktext, href, healthy
                    else:
                        # create link, drop brackets
                        linktext = s[0:p_before]
                        linktext_rstripped = linktext.rstrip()
                        linktext_ws = linktext[len(linktext_rstripped):]
                        if linktext_rstripped:
                            yield linktext_rstripped, href, healthy
                        else:
                            if linktext_ws:
                                yield linktext_ws, None, healthy
                            yield href, href, healthy
                    s = s[p_next + 1:]

                elif char_before == "<" and char_next == ">":
                    yield s[:p], None, healthy
                    yield href, href, healthy
                    yield s[p_next:p_next + 1], None, healthy
                    s = s[p_next + 1:]
                else:
                    yield s[:p], None, healthy
                    yield href, href, healthy
                    s = s[p + len(href):]
        else:
            # empty href.strip() encountered
            healthy = False
    if s:
        yield s, None, healthy


def get_replacement_from_string_and_document(text, document):
    replacement = []
    hrefs = [elm.rawsource for elm in document.traverse() if isinstance(elm, docutils.nodes.reference)]
    for linktext, href, healthy in iter_chunks(text, hrefs):
        if href:
            replacement.append(
                nodes.reference(
                    linktext,
                    linktext,
                    refuri=href,
                    internal=False,
                )
            )
        elif linktext:
            replacement.append(nodes.Text(linktext, linktext))
    return replacement


def get_replacements_from_parsed_string(text):
    document = parse_rst_string(text)
    replacement = get_replacement_from_string_and_document(text, document)
    return replacement



if __name__ == "__main__":

    examples = [
        "https://docs.typo3.org/ is waiting for you.",
        "(https://docs.typo3.org/) is waiting for you.",
        "  (https://docs.typo3.org/)       is waiting for you.",
        "T3Docs (https://docs.typo3.org/) is waiting for you.",
        "T3Docs    (https://docs.typo3.org/)       is waiting for you.",
        "Martin Bless <martin.bless@mbless.de> TYPO3 (https://typo3.org/).",
        "Martin Bless    <martin.bless@mbless.de>  See also: [TYPO3](https://typo3.org/).",
        ]
    for e, text in enumerate(examples):
        print(f"\n==========\n{text}\n----------\n")
        get_replacements_from_parsed_string(text)
