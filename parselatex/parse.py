from pylatexenc.latexwalker import LatexWalker, LatexEnvironmentNode, LatexMacroNode, LatexCharsNode, LatexGroupNode, LatexCommentNode
from .decision import parse_decision
from .requirement import parse_requirement
from .macro import Macro
from .group import Group
from .text import Text


def parse_options(options_text: str) -> dict:
    """
    Parses LaTeX macro options into a dictionary.

    Example:
        Input:  "source=Rail:UC:Tfz, flag,"
        Output: {'source': 'Rail:UC:Tfz', 'flag': None}
    """
    result = {}
    # Remove line breaks and extra spaces
    options_text = options_text.replace('\n', '').strip()

    # Split at commas, ignore empty entries
    pairs = [entry.strip() for entry in options_text.split(',') if entry.strip()]

    for entry in pairs:
        if '=' in entry:
            key, value = entry.split('=', 1)
            result[key.strip()] = value.strip()
        else:
            # Handle flag-like options without a value
            result[entry.strip()] = None

    return result


def parse_nodes(nodes):

    elements = []
    macro = None

    for n in nodes:

        if isinstance(n, LatexCommentNode):
            continue

        if isinstance(n, LatexMacroNode):
            macro = Macro(n.macroname)
            elements.append(macro)
            continue

        if macro:
            if isinstance(n, LatexCharsNode):
                text = n.chars.strip()
                if len(text) == 0:
                    continue

                # if options
                if text.startswith("[") and text.endswith("]"):
                    macro.setOptions(parse_options(text[1:-1]))
                    continue

                # Ende vom MAcro
                macro = None
                elements.append(Text(text))
                continue

            if isinstance(n, LatexGroupNode):
                childs = parse_nodes(n.nodelist)
                if len(childs) == 1:
                    macro.addArgument(childs[0])
                else:
                    macro.addArgument(Group(childs))
                continue

            if not isinstance(n, LatexEnvironmentNode):
                raise ValueError(f"Unknown type {type(n)}")

            # Ende macro
            macro = None

        if isinstance(n, LatexEnvironmentNode):
            childs = parse_nodes(n.nodelist)
            elements.extend(childs)
            continue

        if isinstance(n, LatexCharsNode):
            text = n.chars.strip()
            if len(text) == 0:
                continue
            elements.append(Text(text))

    return elements


def parse_latex(content: str):

    result = []
    walker = LatexWalker(content)
    nodes, _, _ = walker.get_latex_nodes(pos=0)

    for e in parse_nodes(nodes):
        if isinstance(e, Macro):
            if e.name == "entscheidung":
                decision = parse_decision(e)
                result.append(decision)

            elif e.name == "anforderung":
                requirement = parse_requirement(e)
                result.append(requirement)

    return result
