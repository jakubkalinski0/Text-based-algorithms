def find_pattern_in_column(text_column: str, pattern_columns: list[str]) -> list[tuple[int, int]]:
    """
    Wyszukuje wszystkie kolumny wzorca w kolumnie tekstu.

    Args:
        text_column: Kolumna tekstu
        pattern_columns: Lista kolumn wzorca

    Returns:
        Lista krotek (pozycja, indeks kolumny), gdzie znaleziono kolumnę wzorca
    """
    results = []
    text_len = len(text_column)

    for col_idx, pattern_col in enumerate(pattern_columns):
        pattern_len = len(pattern_col)

        if pattern_len == 0:
            continue
        if pattern_len > text_len:
            continue

        for pos in range(text_len - pattern_len + 1):
            if text_column[pos:pos + pattern_len] == pattern_col:
                results.append((pos, col_idx))

    return results


def find_pattern_2d(text: list[str], pattern: list[str]) -> list[tuple[int, int]]:
    """
    Wyszukuje wzorzec dwuwymiarowy w tekście dwuwymiarowym.

    Args:
        text: Tekst dwuwymiarowy (lista ciągów znaków tej samej długości)
        pattern: Wzorzec dwuwymiarowy (lista ciągów znaków tej samej długości)

    Returns:
        Lista krotek (i, j), gdzie (i, j) to współrzędne lewego górnego rogu wzorca w tekście
    """
    if not text or not pattern:
        return []

    text_height = len(text)
    if text_height == 0:
        return []

    text_width = len(text[0])
    if any(len(row) != text_width for row in text):
        raise ValueError("Wszystkie wiersze tekstu muszą mieć taką samą długość")

    pattern_height = len(pattern)
    if pattern_height == 0:
        return []

    pattern_width = len(pattern[0])
    if any(len(row) != pattern_width for row in pattern):
        raise ValueError("Wszystkie wiersze wzorca muszą mieć taką samą długość")

    if pattern_height > text_height or pattern_width > text_width:
        return []

    results = []

    for i in range(text_height - pattern_height + 1):
        for j in range(text_width - pattern_width + 1):
            match = True
            for pi in range(pattern_height):
                if text[i + pi][j:j + pattern_width] != pattern[pi]:
                    match = False
                    break

            if match:
                results.append((i, j))

    return results