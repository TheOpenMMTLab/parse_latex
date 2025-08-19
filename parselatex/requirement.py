from .macro import Macro
from .parse_util import get_text, get_id


class Requirement:

    def __init__(self, id, options, modality, text):
        self.id = id
        self.options = options
        self.modality = modality
        self.text = text

    def __repr__(self):
        return (f"Requirement(id={self.id}, options={self.options}, "
                f"modality={self.modality}, text={self.text})")


def parse_requirement(macro: Macro) -> Requirement:
    """
    Parses the \\anforderung command and extracts its components.
    """

    if len(macro.arguments) != 5:
        raise ValueError(f"Expected 5 arguments in Requirement, got {len(macro.arguments)}: {macro.arguments}")

    lines = [get_text(n) for n in macro.arguments[1:5]]

    return Requirement(
        id=get_text(macro.arguments[0]),
        options=macro.options,
        modality=get_text(macro.arguments[2]),
        text=' '.join(lines)
    )
