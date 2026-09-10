from parselatex.parse import parse_latex


def test_parse_decision_key_bandwidth_insufficient():
    """Test with real decision from new_requirements.tex"""
    content = r"""
        \entscheidung
          {Arch:Rail:KeyBandwithInsufficient}
          {vorgeschlagen}
          {\useid{Rail:Req:Laden:Dauer:Tfz},
           \useid{Rail:Req:Laden:Dauer:Smartphone}}
          {Die synchrone Generierung von Schlüsselmaterial auf den mobilen Endstellen würde zu langes Gebundensein an Verbindungen erfordern}
          {%
            Schlüsselverbrauch dem Schlüsselangebot unterordnen.
            Vorteil ist die Einfachheit der Umsetzung.
            Inakzeptabler Nachteil ist die Verringerung der IT-Sicherheit.%
          }{%
            Schlüsselgenerierungsrate erhöhen.
            Außerhalb der Möglichkeiten.%
          }{%
            Mehrere Verbindungen parallel für Beladung nutzen.
            Vorteil ist die Nähe zur standardisierten Architektur.
            Nachteil sind die höheren Hardwarekosten.%
          }{%
            Freifeld-Verbindung mittels Laser durch Luft.
            Vorteil ist die Entbehrung der Verbindung mittels Lichtwellenleiter.
            Nachteil ist die Unverfügbarkeit der Technologie.%
          }{}
    """

    parts = list(parse_latex(content))
    assert len(parts) == 1
    decision = parts[0]
    assert decision.id == "Arch:Rail:KeyBandwithInsufficient"
    assert decision.state == "vorgeschlagen"
    # References should be a list with 2 items
    assert len(decision.references) == 2
    assert decision.references == ["Rail:Req:Laden:Dauer:Tfz", "Rail:Req:Laden:Dauer:Smartphone"]
    # Problem description
    assert "Schlüsselmaterial" in decision.problem
    # Alternatives should be a list with 4 items (5th is empty)
    assert len(decision.alternatives) == 4
    assert "Schlüsselverbrauch" in decision.alternatives[0]
    assert "Schlüsselgenerierungsrate" in decision.alternatives[1]
    assert "parallel" in decision.alternatives[2]
    assert "Freifeld" in decision.alternatives[3]


def test_parse_decision_indirect_qkd():
    """Test with simpler decision from new_requirements.tex"""
    content = r"""
        \entscheidung
          {Arch:Rail:IndirectQKD}
          {vorgeschlagen}
          {\useid{Arch:Rail:KeyBandwithInsufficient}}
          {Die mobilen Endstellen sollen ihr Schlüsselmaterial nicht direkt selbst erzeugen, also indirekt erhalten}
          {%
            Gebundensein an Verbindungen erzwingen.
            Vorteil ist die Einfachheit der Lösung.
            Nachteil sind erzwungene stationäre Verweildauern.%
          }{}{}{}{}
    """

    parts = list(parse_latex(content))
    assert len(parts) == 1
    decision = parts[0]
    assert decision.id == "Arch:Rail:IndirectQKD"
    assert decision.state == "vorgeschlagen"
    # Single reference
    assert len(decision.references) == 1
    assert decision.references == ["Arch:Rail:KeyBandwithInsufficient"]
    # Problem description
    assert "Schlüsselmaterial" in decision.problem
    # Only 1 non-empty alternative
    assert len(decision.alternatives) == 1
    assert "Gebundensein" in decision.alternatives[0]
    assert parts[0].state == "vorgeschlagen"