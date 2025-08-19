from parselatex.parse import parse_latex


def test_parse_decision_entschieden():
    content = r"""
        \entscheidung
        {Ent:Beispiel} % Kennung
        {\useid{Rail:Req:DistanzUnlimitiert}} % Problem
        {\usealt{1} Es wird der SuperLaser3000 der Fa.\ ThüriLicht verwendet} % Lösung
        {
            \defalt{1} Der SuperLaser3000 der Fa.\ ThüriLicht
            \defalt{2} Handelsüblicher Laserpointer als Photonenquelle: Günstig aber technisch ungenügend.
        } % Alternativen
        { entschieden } % Status
    """

    parts = list(parse_latex(content))
    assert len(parts) == 1
    assert parts[0].id == "Ent:Beispiel"
    assert parts[0].reference == "Rail:Req:DistanzUnlimitiert"
    assert parts[0].selected == ("1", "Es wird der SuperLaser3000 der Fa. ThüriLicht verwendet")
    assert parts[0].alternatives == {
        "1": "Der SuperLaser3000 der Fa. ThüriLicht",
        "2": "Handelsüblicher Laserpointer als Photonenquelle: Günstig aber technisch ungenügend."
    }
    assert parts[0].state == "entschieden"


def test_parse_decision_vorgeschlagen():
    content = r"""
        \entscheidung
        {Ent:Beispiel} % Kennung
        {\useid{Rail:Req:DistanzUnlimitiert}} % Problem
        {} % Lösung
        {
            \defalt{1} Der SuperLaser3000 der Fa.\ ThüriLicht
            \defalt{2} Handelsüblicher Laserpointer als Photonenquelle: Günstig aber technisch ungenügend.
        } % Alternativen
        {vorgeschlagen} % Status
    """

    parts = list(parse_latex(content))
    assert len(parts) == 1
    assert parts[0].id == "Ent:Beispiel"
    assert parts[0].reference == "Rail:Req:DistanzUnlimitiert"
    assert parts[0].selected is None
    assert parts[0].alternatives == {
        "1": "Der SuperLaser3000 der Fa. ThüriLicht",
        "2": "Handelsüblicher Laserpointer als Photonenquelle: Günstig aber technisch ungenügend."
    }
    assert parts[0].state == "vorgeschlagen"