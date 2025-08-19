from parselatex.parse import parse_latex


def test_parse_requirement_simple():
    content = r"""
        \anforderung[
    ursprung=Rail:UC:Tfz,
]
    {Rail:Komm:Integr:Tfz}
    {Kommunikationsinfrastruktur}
    {muss}
    {Integrität der Datenverbindung zwischen Stellwerk und Triebfahrzeug}
    {sicherstellen}
    """

    parts = list(parse_latex(content))
    assert len(parts) == 1
    assert parts[0].id == "Rail:Komm:Integr:Tfz"
    assert parts[0].options == {"ursprung": "Rail:UC:Tfz"}
    assert parts[0].modality == "muss"
    assert parts[0].text == "Kommunikationsinfrastruktur muss Integrität der Datenverbindung zwischen Stellwerk und Triebfahrzeug sicherstellen"


def test_parse_requirement_complex():
    content = r"""
        \begin{itemize}

    \item \anforderung
      {Rail:Req:Schlüsselsynchronisierung}
      {Das System}
      {muss}
      {für die Kommunikation zwischen Triebfahrzeugen und Stellwerk}
      {einen synchron via \gls{qkd} verteilten Schlüssel nutzen}%
      \todo{lp: verstehe \enquote{synchron} hier nicht}


    \end{itemize}
    """

    parts = list(parse_latex(content))
    assert len(parts) == 1
    assert parts[0].id == "Rail:Req:Schlüsselsynchronisierung"
    assert parts[0].options == {}
    assert parts[0].modality == "muss"
    assert parts[0].text == "Das System muss für die Kommunikation zwischen Triebfahrzeugen und Stellwerk einen synchron via qkd verteilten Schlüssel nutzen"


def test_parse_requirement_macros():
    content = r"""
    \anforderung
      {Rail:Req:QKDDistanz}
      {Das System}
      {muss}
      {den Schlüsselaustausch via \gls{qkd}}
      {über Strecken von mehreren \SI{100}{\kilo\meter} ermöglichen}
    """

    parts = list(parse_latex(content))
    assert len(parts) == 1
    assert parts[0].id == "Rail:Req:QKDDistanz"
    assert parts[0].options == {}
    assert parts[0].modality == "muss"
    assert parts[0].text == "Das System muss den Schlüsselaustausch via qkd über Strecken von mehreren 100 km ermöglichen"


