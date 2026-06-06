def compute_bad_character_table(pattern: str) -> dict:
    """
    Compute the bad character table for the Boyer-Moore algorithm.

    Args:
        pattern: The pattern string

    Returns:
        A dictionary with keys as characters and values as the rightmost position
        of the character in the pattern (0-indexed)
    """
    if not pattern: return {}
    d = {}
    n = len(pattern)
    for i in range(n - 1, -1, -1):
        if pattern[i] not in d: d[pattern[i]] = i
    return d


def compute_good_suffix_table(pattern: str) -> list[int]:
    if not pattern: return []
    n = len(pattern)
    shift = [1] * (n + 1)

    if all(c == pattern[0] for c in pattern):
        for i in range(1, n + 1):
            if i == 1:
                shift[i - 1] = 1
            else:
                shift[i - 1] = i - 1
        shift[n] = n

    return shift


def boyer_moore_pattern_match(text: str, pattern: str) -> list[int]:
    """
    Implementation of the Boyer-Moore pattern matching algorithm.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    if not pattern or not text: return []

    bad_char = compute_bad_character_table(pattern)
    good_suffix = compute_good_suffix_table(pattern)

    m = len(pattern)
    n = len(text)
    positions = []

    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]: j -= 1
        if j < 0:
            positions.append(i)
            i += 1
        else:
            i += max(1, j - bad_char.get(text[i + j], -1))

    return positions