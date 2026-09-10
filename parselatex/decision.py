from typing import List
from .macro import Macro

from .parse_util import get_text, get_id, to_list


class Decision:

    def __init__(self, id: str, state: str, references: List[str], problem: str, alternatives: List[str]):
        self.id = id
        self.state = state
        self.references = references  # List of reference IDs
        self.problem = problem        # Problem description text
        self.alternatives = alternatives  # List of alternative descriptions (non-empty only)

    def __repr__(self):
        return (f"Decision(id={self.id}, state={self.state}, "
                f"references={self.references}, alternatives={self.alternatives})")


def parse_decision(macro) -> Decision:
    assert len(macro.options) == 0, "Expected no options in Decision"
    if len(macro.arguments) != 9:
        raise ValueError(f"Expected 9 arguments in Decision, got {len(macro.arguments)}: {macro.arguments}")

    return parse_decision_format(macro)


def parse_decision_format(macro) -> Decision:
    """Parse the decision format with nine arguments."""
    # Argument 0: ID
    decision_id = get_text(macro.arguments[0])

    # Argument 1: State
    state = get_text(macro.arguments[1])

    # Argument 2: References (can have multiple \useid macros)
    references = parse_references(macro.arguments[2])

    # Argument 3: Problem description
    problem = get_text(macro.arguments[3])

    # Arguments 4-8: Alternatives (collect only non-empty ones)
    alternatives = []
    for i in range(4, 9):
        alt_text = get_text(macro.arguments[i]).strip()
        if alt_text:  # Only add non-empty alternatives
            alternatives.append(alt_text)

    return Decision(
        id=decision_id,
        state=state,
        references=references,
        problem=problem,
        alternatives=alternatives
    )


def parse_references(n) -> List[str]:
    """Parse references from the references argument (can contain multiple \\useid macros)"""
    references = []
    items = to_list(n)

    for item in items:
        if isinstance(item, Macro) and item.name == "useid":
            ref_id = get_id(item)
            references.append(ref_id)

    return references
