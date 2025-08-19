from .text import Text
from .macro import Macro
from .group import Group


def to_list(n) -> list:
    if isinstance(n, Group):
        return n.content
    return [n]


def get_id(n) -> str:
    if isinstance(n, Macro) and len(n.arguments) == 1:
        return get_text(n.arguments[0])
    raise ValueError(f"Expected Macro with 1 argument, got {n}")


def get_si_unit(n) -> str:
    unit = None
    prefix = ""
    for e in to_list(n):
        if isinstance(e, Macro) and e.name == "kilo":
            prefix = "k"
            continue
        if isinstance(e, Macro) and e.name == "meter":
            unit = "m"
            continue
        raise ValueError(f"Expected Macro with unit, got {n}")

    if not unit:
        raise ValueError(f"Expected Macro with unit, got {n}")
    return prefix + unit


def get_text(n) -> str:
    if isinstance(n, Group):
        return " ".join(get_text(arg) for arg in n.content)
    
    if isinstance(n, Macro) and len(n.arguments) == 0 and n.name == " ":
        return " "
    if isinstance(n, Macro) and len(n.arguments) == 0 and n.name == "zb":
        return "z.B."

    if isinstance(n, Macro) and len(n.arguments) == 1 and n.name in ["gls", "glsentrytext"]:
        return get_text(n.arguments[0])
    if isinstance(n, Macro) and len(n.arguments) == 2 and n.name == "SI":
        return get_text(n.arguments[0]) + " " + get_si_unit(n.arguments[1])
    
    if isinstance(n, Text):
        return n.content
    raise ValueError(f"Expected Text, got {n}")
