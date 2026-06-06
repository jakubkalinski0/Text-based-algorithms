import re


def extract_links(html: str) -> list[dict[str, str]]:
    """
    Extract all links from the given HTML string.

    Args:
        html (str): HTML content to analyze

    Returns:
        list[dict]: A list of dictionaries where each dictionary contains:
            - 'url': the href attribute value
            - 'title': the title attribute value (or None if not present)
            - 'text': the text between <a> and </a> tags
    """

    # Wzorzec wyrażenia regularnego dla tagów <a>
    # Obsługuje opcjonalny atrybut title i różne rodzaje cudzysłowów
    link_pattern = r'<a\s+href=(["\'])(.*?)\1(\s+title=(["\'])(.*?)\4)?.*?>(.*?)</a>'

    # Lista do przechowywania wyodrębnionych linków
    links = []

    # Znajdź wszystkie wystąpienia linków
    for match in re.finditer(link_pattern, html, re.DOTALL):
        # Wyodrębnij URL, tytuł (opcjonalny) i tekst
        url = match.group(2)
        title = match.group(5) if match.group(5) else None
        text = match.group(6)

        # Dodaj do listy linków
        links.append({
            'url': url,
            'text': text,
            'title': title
        })

    return links

    # # TODO: Implement a regular expression pattern to extract links from HTML.
    # # The pattern should capture three groups:
    # # 1. The URL (href attribute value)
    # # 2. The title attribute (which might not exist)
    # # 3. The link text (content between <a> and </a> tags)
    # pattern = r""
    #
    # links = []
    #
    # # TODO: Use re.finditer to find all matches of the pattern in the HTML
    # # For each match, extract the necessary information and create a dictionary
    # # Then append that dictionary to the 'links' list
    #
    # return links
