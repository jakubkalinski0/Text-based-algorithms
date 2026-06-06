def allison_global_alignment(s1: str, s2: str,
                             match_score: int = 2,
                             mismatch_score: int = -1,
                             gap_penalty: int = -1) -> tuple[int, str, str]:
    """
    Znajduje optymalne globalne wyrównanie używając algorytmu Allisona.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków
        match_score: Punkty za dopasowanie
        mismatch_score: Punkty za niedopasowanie
        gap_penalty: Kara za lukę

    Returns:
        Krotka zawierająca wynik wyrównania i dwa wyrównane ciągi
    """
    m, n = len(s1), len(s2)

    # Obsługa pustych ciągów
    if m == 0 and n == 0:
        return 0, "", ""
    if m == 0:
        return n * gap_penalty, "-" * n, s2
    if n == 0:
        return m * gap_penalty, s1, "-" * m

    # Inicjalizacja macierzy wyników
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Inicjalizacja pierwszego wiersza i kolumny (kary za luki)
    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] + gap_penalty
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] + gap_penalty

    # Wypełnienie macierzy
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Sprawdzenie czy znaki się dopasowują
            if s1[i - 1] == s2[j - 1]:
                match = dp[i - 1][j - 1] + match_score
            else:
                match = dp[i - 1][j - 1] + mismatch_score

            # Opcje z lukami
            delete = dp[i - 1][j] + gap_penalty  # Luka w s2
            insert = dp[i][j - 1] + gap_penalty  # Luka w s1

            # Wybór najlepszej opcji
            dp[i][j] = max(match, delete, insert)

    # Traceback - odtworzenie wyrównania
    aligned_s1, aligned_s2 = "", ""
    i, j = m, n

    while i > 0 or j > 0:
        if i > 0 and j > 0:
            # Sprawdzenie czy przyszliśmy z przekątnej
            if s1[i - 1] == s2[j - 1]:
                score_match = dp[i - 1][j - 1] + match_score
            else:
                score_match = dp[i - 1][j - 1] + mismatch_score

            if dp[i][j] == score_match:
                aligned_s1 = s1[i - 1] + aligned_s1
                aligned_s2 = s2[j - 1] + aligned_s2
                i -= 1
                j -= 1
            elif i > 0 and dp[i][j] == dp[i - 1][j] + gap_penalty:
                aligned_s1 = s1[i - 1] + aligned_s1
                aligned_s2 = "-" + aligned_s2
                i -= 1
            else:
                aligned_s1 = "-" + aligned_s1
                aligned_s2 = s2[j - 1] + aligned_s2
                j -= 1
        elif i > 0:
            aligned_s1 = s1[i - 1] + aligned_s1
            aligned_s2 = "-" + aligned_s2
            i -= 1
        else:
            aligned_s1 = "-" + aligned_s1
            aligned_s2 = s2[j - 1] + aligned_s2
            j -= 1

    return dp[m][n], aligned_s1, aligned_s2


def allison_local_alignment(s1: str, s2: str,
                            match_score: int = 2,
                            mismatch_score: int = -1,
                            gap_penalty: int = -1) -> tuple[int, str, str, int, int]:
    """
    Znajduje optymalne lokalne wyrównanie (podobnie do algorytmu Smith-Waterman).

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków
        match_score: Punkty za dopasowanie
        mismatch_score: Punkty za niedopasowanie
        gap_penalty: Kara za lukę

    Returns:
        Krotka zawierająca wynik wyrównania, dwa wyrównane ciągi oraz pozycje początku
    """
    m, n = len(s1), len(s2)

    # Obsługa pustych ciągów
    if m == 0 or n == 0:
        return 0, "", "", 0, 0

    # Inicjalizacja macierzy wyników (wszystkie zera dla lokalnego wyrównania)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Śledzenie maksymalnego wyniku i jego pozycji
    max_score = 0
    max_i, max_j = 0, 0

    # Wypełnienie macierzy
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Sprawdzenie czy znaki się dopasowują
            if s1[i - 1] == s2[j - 1]:
                match = dp[i - 1][j - 1] + match_score
            else:
                match = dp[i - 1][j - 1] + mismatch_score

            # Opcje z lukami
            delete = dp[i - 1][j] + gap_penalty  # Luka w s2
            insert = dp[i][j - 1] + gap_penalty  # Luka w s1

            # Wybór najlepszej opcji (minimum 0 dla lokalnego wyrównania)
            dp[i][j] = max(0, match, delete, insert)

            # Aktualizacja maksymalnego wyniku
            if dp[i][j] > max_score:
                max_score = dp[i][j]
                max_i, max_j = i, j

    # Jeśli maksymalny wynik to 0, nie ma dobrego lokalnego wyrównania
    if max_score == 0:
        return 0, "", "", 0, 0

    # Traceback od pozycji z maksymalnym wynikiem
    aligned_s1, aligned_s2 = "", ""
    i, j = max_i, max_j

    # Pozycje końca wyrównania (1-based indexing)
    end_i, end_j = i, j

    while i > 0 and j > 0 and dp[i][j] > 0:
        if s1[i - 1] == s2[j - 1]:
            score_match = dp[i - 1][j - 1] + match_score
        else:
            score_match = dp[i - 1][j - 1] + mismatch_score

        if dp[i][j] == score_match:
            aligned_s1 = s1[i - 1] + aligned_s1
            aligned_s2 = s2[j - 1] + aligned_s2
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + gap_penalty:
            aligned_s1 = s1[i - 1] + aligned_s1
            aligned_s2 = "-" + aligned_s2
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + gap_penalty:
            aligned_s1 = "-" + aligned_s1
            aligned_s2 = s2[j - 1] + aligned_s2
            j -= 1
        else:
            break

    # Pozycje początku wyrównania (0-based indexing)
    start_i, start_j = i, j

    return max_score, aligned_s1, aligned_s2, start_i, start_j


def print_alignment_matrix(s1: str, s2: str, dp: list[list[int]]):
    """Pomocnicza funkcja do wyświetlania macierzy wyrównania"""
    print("Macierz wyrównania:")
    print("    ", end="")
    print("    ".join(["-"] + list(s2)))
    for i, row in enumerate(dp):
        char = "-" if i == 0 else s1[i - 1]
        print(f"{char:2} ", end="")
        print("  ".join(f"{val:2}" for val in row))
    print()