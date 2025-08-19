from parselatex.parse import parse_latex


def test_parse_latex(data_dir):
    input_file = data_dir / "text.tex"

    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    parts = list(parse_latex(content))
    assert len(parts) == 4
    for part in parts:
        print(part)
