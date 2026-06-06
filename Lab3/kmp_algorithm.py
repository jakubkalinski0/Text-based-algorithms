def compute_lps_array(pattern: str) -> list[int]:
    """
    Compute the Longest Proper Prefix which is also Suffix array for KMP algorithm.

    Args:
        pattern: The pattern string

    Returns:
        The LPS array
    """
    # TODO: Implement the Longest Prefix Suffix (LPS) array computation
    # The LPS array helps in determining how many characters to skip when a mismatch occurs
    # For each position i, compute the length of the longest proper prefix of pattern[0...i]
    # that is also a suffix of pattern[0...i]
    # Hint: Use the information from previously computed values to avoid redundant comparisons
    n = len(pattern)
    lps = [0] * n

    length = 0  # naj pref
    i = 1

    while i < n:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            # jesli nie machuja
            if length != 0:
                length = lps[length - 1]
            else:  # jesli nie ma gdzie wrocic
                lps[i] = 0
                i += 1
    return lps


def kmp_pattern_match(text: str, pattern: str) -> list[int]:
    """
    Implementation of the Knuth-Morris-Pratt pattern matching algorithm.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # TODO: Implement the KMP string matching algorithm
    # 1. Preprocess the pattern to compute the LPS array
    # 2. Use the LPS array to determine how much to shift the pattern when a mismatch occurs
    # 3. This avoids redundant comparisons by using information about previous matches
    # 4. Return all positions where the pattern is found in the text
    if not pattern or not text: return []

    lps = compute_lps_array(pattern)

    n = len(text)
    m = len(pattern)
    i = 0  # text
    j = 0  # pattern
    positions = []  # miejsca matchów

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == m:  # caly pattern sie pokrywa
            positions.append(i - j)
            j = lps[j - 1]  # wracamy lps tablem

        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]  # wracamy lps tablem
            else:
                i += 1

    return positions