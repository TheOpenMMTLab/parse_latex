from typing import Dict, Tuple
from .group import Group
from .macro import Macro

from .parse_util import get_text, get_id, to_list


class Decision:

    def __init__(self, id, reference: str, selected: Tuple[str, str], alternatives: Dict[str, str], state: str):
        self.id = id
        self.reference = reference
        self.selected = selected
        self.alternatives = alternatives
        self.state = state

    def __repr__(self):
        return (f"Decision(id={self.id}, alternatives={self.alternatives}, "
                f"selected={self.selected}, state={self.state})")


def parse_reference(n) -> str:
    if isinstance(n, Macro):
        if n.name == "useid" and len(n.arguments) == 1:
            return get_text(n.arguments[0])
    raise ValueError(f"Expected useid Macro 'useid', got {type(n)}")


def parse_selected(n) -> Tuple[str, str]:
    sel_id = None
    text = ""
    selected = to_list(n)
    for item in selected:
        if isinstance(item, Macro) and item.name == "usealt":
            if sel_id:
                raise ValueError(f"Expected only one usealt Macro in {selected}")
            sel_id = get_id(item)
            continue
        text += get_text(item)

    if sel_id is None:  # no decision
        return None

    return sel_id, text.strip()


def parse_alternatives(n) -> Dict[str, str]:
    altdef = to_list(n)
    alt_id = None
    result = {}
    for item in altdef:
        if isinstance(item, Macro) and item.name == "defalt":
            alt_id = get_id(item)
            if alt_id in result:
                raise ValueError(f"Duplicate defalt Macro id found: {alt_id}")
            result[alt_id] = ""
            continue
        if alt_id is None:
            raise ValueError(f"Expected defalt Macro with an id, got {altdef}")
        result[alt_id] += get_text(item)

    return result


def parse_decision(macro) -> Decision:
    assert len(macro.options) == 0, "Expected no options in Decision"
    if len(macro.arguments) != 5:
        raise ValueError(f"Expected 5 arguments in Decision, got {len(macro.arguments)}: {macro.arguments}")

    return Decision(
        id=get_text(macro.arguments[0]) ,
        reference=parse_reference(macro.arguments[1]),
        selected=parse_selected(macro.arguments[2]),
        alternatives=parse_alternatives(macro.arguments[3]),
        state=get_text(macro.arguments[4])
    )
