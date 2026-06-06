def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Oblicza odległość Levenshteina między dwoma ciągami znaków.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość Levenshteina (minimalna liczba operacji wstawienia, usunięcia
        lub zamiany znaku potrzebnych do przekształcenia s1 w s2)
    """
    if not s1: return len(s2)  # edge case
    if not s2: return len(s1)

    n1 = len(s1)
    n2 = len(s2)

    dp = [[0 for _ in range(n2 + 1)] for _ in range(n1 + 1)]

    for i in range(n1 + 1): dp[i][0] = i  # usuwanie i znakow

    for i in range(1, n2 + 1): dp[0][i] = i  # wstawianie j znakow
    # dp[i][j] to minimalna liczba operacji wstaw,suun,zmien potrzebna do zmiany pierwszych i znakow z s1 w pierwsze j znakow z s2.
    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)  # usunięcie, wstaw, zmien

    return dp[n1][n2]