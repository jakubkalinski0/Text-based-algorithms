import re
from typing import Optional


def parse_publication(reference: str) -> Optional[dict]:
    """
    Parse academic publication reference and extract structured information.

    Expected reference format:
    Lastname, I., Lastname2, I2. (Year). Title. Journal, Volume(Issue), StartPage-EndPage.

    Example:
    Kowalski, J., Nowak, A. (2023). Analiza algorytmów tekstowych. Journal of Computer Science, 45(2), 123-145.

    Args:
        reference (str): Publication reference string

    Returns:
        Optional[dict]: A dictionary containing parsed publication data or None if the reference doesn't match expected format
    """
    # TODO: Implement regex patterns to match different parts of the reference
    # You need to create patterns for:
    # 1. Authors and year pattern
    # 2. Title and journal pattern
    # 3. Volume, issue, and pages pattern
    authors_year_pattern = r"(?:[A-Za-zśŚźŻżŻłŁąĄęĘóÓćĆńŃ]+,\s[A-Za-zśŚźŻżŻłŁąĄęĘóÓćĆńŃ]\.,?\s?)+)\((\d{4})\)"
    title_journal_pattern = r"\.\s([^.]+)\.\s([^,]+),\s(\d+)"
    volume_issue_pages_pattern = r"(?:\((\d+)\))?,\s(\d+)-(\d+)"

    # TODO: Combine the patterns
    full_pattern = r"^((?:[A-Za-zśŚźŻżŻłŁąĄęĘóÓćĆńŃ]+,\s[A-Za-zśŚźŻżŻłŁąĄęĘóÓćĆńŃ]\.,?\s?)+)\((\d{4})\)\.\s([^.]+)\.\s([^,]+),\s(\d+)(?:\((\d+)\))?,\s(\d+)-(\d+)"

    # TODO: Use re.match to try to match the full pattern against the reference
    # If there's no match, return None

    match = re.search(full_pattern, reference)
    if not match: return None

    # TODO: Extract information using regex
    # Each author should be parsed into a dictionary with 'last_name' and 'initial' keys

    authors_str = match.group(1)

    authors_list = []

    # TODO: Create a pattern to match individual authors
    author_pattern = r"([A-Za-zśŚźŻżŻłŁąĄęĘóÓćĆńŃ]+),\s([A-Za-zśŚźŻżŻłŁąĄęĘóÓćĆńŃ])\."

    # TODO: Use re.finditer to find all authors and add them to authors_list

    authors_list = [{'last_name': author_match.group(1), 'initial': author_match.group(2)} for author_match in
                    re.finditer(author_pattern, authors_str)]

    # TODO: Create and return the final result dictionary with all the parsed information
    # It should include authors, year, title, journal, volume, issue, and pages

    year = int(match.group(2))
    title = match.group(3)
    journal = match.group(4)
    volume = int(match.group(5))
    issue_str = match.group(6)
    issue = int(issue_str) if issue_str else None
    start_page = int(match.group(7))
    end_page = int(match.group(8))

    return {
        'authors': authors_list,
        'year': year,
        'title': title,
        'journal': journal,
        'volume': volume,
        'issue': issue,
        'pages': {
            'start': start_page,
            'end': end_page}
    }