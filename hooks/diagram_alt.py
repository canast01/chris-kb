"""Give Kroki diagrams real alt text instead of the plugin's fixed alt="Kroki".

on_page_markdown (runs before the kroki plugin) records each diagram fence's
labels; on_page_content replaces alt="Kroki" on the generated <img> tags in
order with "<section> diagram: label, label, ...". If the counts don't match,
it falls back to "<section> diagram" so no wrong label is ever attached.
"""
import html
import re

from mkdocs.plugins import event_priority

LANGS = ("d2", "plantuml", "mermaid", "vegalite", "graphviz", "dot", "blockdiag", "seqdiag", "nwdiag", "c4plantuml")
FENCE = re.compile(r"^(`{3,}|~{3,})[ \t]*(" + "|".join(LANGS) + r")\b[^\n]*\n(.*?)^\1[ \t]*$", re.S | re.M)
HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", re.M)
QUOTED = re.compile(r'"((?:[^"\\]|\\.)+)"')
MERMAID_NODE = re.compile(r"\w[\[\(\{]+\"?(.+?)\"?[\]\)\}]+(?=\s|$|:|;|-|&)", re.M)
PUML_DECL = re.compile(r"^\s*(?:actor|participant|database|entity|boundary|control|collections|queue|node|component|rectangle)\s+\"?([^\"\n]+?)\"?(?:\s+as\s+\w+)?\s*$", re.M)
MAX_LABELS = 8
MAX_ALT = 160
ANY_FENCE = re.compile(r"^(`{3,}|~{3,}).*?^\1[ \t]*$", re.S | re.M)

_pending = {}


def _clean(s):
    s = s.replace("\\n", " ").replace("\\$", "$").replace('\\"', '"')
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"[*_`]", "", s)
    return re.sub(r"\s+", " ", s).strip(" :")


def _labels(lang, body):
    if lang == "vegalite":
        m = re.search(r'"title"\s*:\s*"([^"]+)"', body)
        return [m.group(1)] if m else []
    if lang in ("plantuml", "c4plantuml"):
        found = PUML_DECL.findall(body) or QUOTED.findall(body)
    elif lang == "mermaid":
        found = MERMAID_NODE.findall(body) or QUOTED.findall(body)
    else:
        found = QUOTED.findall(body)
    out, seen = [], set()
    for raw in found:
        lab = _clean(raw)
        lab = lab.strip("[]{} ")
        while lab.startswith("(") and lab.count("(") > lab.count(")"):
            lab = lab[1:].strip()
        while lab.endswith(")") and lab.count(")") > lab.count("("):
            lab = lab[:-1].strip()
        if lab.count("(") > lab.count(")"):
            lab += ")"
        if (not lab or len(lab) < 3 or len(lab) > 60 or lab.lower() in seen
                or re.fullmatch(r"[#\d\s.,;:%/-]+", lab)):
            continue
        seen.add(lab.lower())
        out.append(lab)
        if len(out) == MAX_LABELS:
            break
    return out


@event_priority(100)  # before the kroki plugin replaces the fences
def on_page_markdown(markdown, page, **kwargs):
    # Blank out fenced code so "# comment" lines inside code are not taken as headings
    masked = ANY_FENCE.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), markdown)
    headings = [(m.start(), _clean(m.group(2))) for m in HEADING.finditer(masked)]
    items = []
    for m in FENCE.finditer(markdown):
        section = next((h for pos, h in reversed(headings) if pos < m.start()), page.title or "")
        items.append((section, _labels(m.group(2), m.group(3))))
    _pending[page.file.src_uri] = items
    return markdown


def on_page_content(content, page, **kwargs):
    items = _pending.pop(page.file.src_uri, [])
    imgs = list(re.finditer(r'(<img\b[^>]*?\balt=")Kroki("[^>]*\bsrc="[^"]*kroki-generated[^"]*")', content))
    if not imgs:
        return content
    exact = len(imgs) == len(items)
    out, last = [], 0
    for i, m in enumerate(imgs):
        if exact:
            section, labels = items[i]
            alt = f"{section} diagram"
            for lab in labels:
                nxt = alt + (": " if alt.endswith("diagram") else ", ") + lab
                if len(nxt) > MAX_ALT:
                    break
                alt = nxt
        else:
            alt = f"{page.title} diagram"
        out.append(content[last:m.start()])
        out.append(m.group(1) + html.escape(alt, quote=True) + m.group(2))
        last = m.end()
    out.append(content[last:])
    return "".join(out)
