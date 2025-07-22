import re


def parse_options(options_text):
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


def parse_anforderung(latex_code):
    """
    Parses the LaTeX code for the \anforderung macro and extracts its components.
    
    Returns a list of dictionaries with the parsed components.
    """
    pattern = r"""
    \\anforderung      # The macro itself
    \s*
    \[
    (.*?)              # Optional parameters (non-greedy)
    \]
    \s*
    \{
    (.*?)              # 1st mandatory parameter
    \}
    \s*
    \{
    (.*?)              # 2nd mandatory parameter
    \}
    \s*
    \{
    (.*?)              # 3rd mandatory parameter
    \}
    \s*
    \{
    (.*?)              # 4th mandatory parameter
    \}
    \s*
    \{
    (.*?)              # 5th mandatory parameter
    \}
    """

    regex = re.compile(pattern, re.DOTALL | re.VERBOSE)

    for match in regex.finditer(latex_code):
        options = match.group(1).strip()
        options_dict = parse_options(options)
        params = [match.group(i).strip() for i in range(2, 7)]

        yield {
            'options': options_dict,
            'id': params[0],
            'modality': params[2],
            'text': ' '.join(params[1:])+'.'
        }
