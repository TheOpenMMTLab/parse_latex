from parselatex.parse import parse_latex
from parselatex.decision import Decision
from parselatex.requirement import Requirement


def test_parse_latex(data_dir):
    input_file = data_dir / "text.tex"

    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    parts = list(parse_latex(content))
    assert len(parts) == 4
    
    # Check first part is a requirement
    assert isinstance(parts[0], Requirement)
    assert parts[0].id == "Rail:Komm:Integr:Tfz"
    
    # Check second part is a decision
    assert isinstance(parts[1], Decision)
    assert parts[1].id == "Ent:Beispiel"
    assert parts[1].state == "vorgeschlagen"
    assert len(parts[1].references) == 1
    assert parts[1].references[0] == "Rail:Req:DistanzUnlimitiert"
    assert len(parts[1].alternatives) == 2
    
    # Check remaining are requirements
    assert isinstance(parts[2], Requirement)
    assert parts[2].id == "All:Req:quantensicher"
    assert isinstance(parts[3], Requirement)
    assert parts[3].id == "Rail:Req:Schlüsselrate"


def test_parse_latex_special_nodes():

    content = r"""\glsentrytext{stw} --- \glsentrytext{stw}"""
    # This test verifies that LatexSpecialsNode (like ---) is handled without errors
    # The function only returns 'entscheidung' and 'anforderung' macros,
    # so we expect 0 results from this input
    parts = list(parse_latex(content))
    for part in parts:
        print(part)
    assert len(parts) == 0
