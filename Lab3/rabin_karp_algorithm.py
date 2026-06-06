def rabin_karp_pattern_match(text: str, pattern: str, prime: int = 101) -> list[int]:
    """
    Implementation of the Rabin-Karp pattern matching algorithm.
    Args:
        text: The text to search in
        pattern: The pattern to search for
        prime: A prime number used for the hash function
    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """

    if not pattern or not text or len(pattern) > len(text): return []

    m = len(pattern)
    n = len(text)
    matches = []

    h = 1  # hash dla sliding window
    for _ in range(m - 1):
        h = (h * 100) % prime

    p_hash = 0  # pattern
    t_hash = 0  # obecne okno textu

    for i in range(m):
        p_hash = (100 * p_hash + ord(pattern[i])) % prime
        t_hash = (100 * t_hash + ord(text[i])) % prime

    for i in range(n - m + 1):  # m dlugosciowe odcinki
        if p_hash == t_hash:
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match: matches.append(i)

        if i < n - m:
            t_hash = (100 * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % prime  # rehaszujemy suuwamy i dodajemy

    return matches