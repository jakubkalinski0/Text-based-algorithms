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


# Klasa testów z pliku prowadzącego
class TestAllisonAlgorithm:
    def test_allison_global_alignment_identical(self):
        s1 = "ACGT"
        s2 = "ACGT"
        score, align1, align2 = allison_global_alignment(s1, s2)
        expected_score = 8  # 4 matches * 2 points each
        assert score == expected_score, f"Oczekiwano wyniku {expected_score}, otrzymano: {score}"
        assert align1 == "ACGT", f"Oczekiwano 'ACGT', otrzymano: {align1}"
        assert align2 == "ACGT", f"Oczekiwano 'ACGT', otrzymano: {align2}"

    def test_allison_global_alignment_with_mismatch(self):
        s1 = "ACGT"
        s2 = "ATGT"
        score, align1, align2 = allison_global_alignment(s1, s2)
        expected_score = 5  # 3 matches (2*3=6) + 1 mismatch (-1) = 5
        assert score == expected_score, f"Oczekiwano wyniku {expected_score}, otrzymano: {score}"
        assert len(align1) == len(align2), "Wyrównania powinny mieć tę samą długość"

    def test_allison_global_alignment_with_gap(self):
        s1 = "ACGT"
        s2 = "ACT"
        score, align1, align2 = allison_global_alignment(s1, s2)
        assert len(align1) == len(align2), "Wyrównania powinny mieć tę samą długość"
        assert "-" in align1 or "-" in align2, "Wyrównanie powinno zawierać lukę"

    def test_allison_global_alignment_empty_strings(self):
        s1 = ""
        s2 = ""
        score, align1, align2 = allison_global_alignment(s1, s2)
        assert score == 0, f"Oczekiwano wyniku 0, otrzymano: {score}"
        assert align1 == "", f"Oczekiwano pustego ciągu, otrzymano: {align1}"
        assert align2 == "", f"Oczekiwano pustego ciągu, otrzymano: {align2}"

    def test_allison_global_alignment_one_empty(self):
        s1 = "ACGT"
        s2 = ""
        score, align1, align2 = allison_global_alignment(s1, s2)
        expected_score = -4  # 4 gaps * -1 each
        assert score == expected_score, f"Oczekiwano wyniku {expected_score}, otrzymano: {score}"
        assert align1 == "ACGT", f"Oczekiwano 'ACGT', otrzymano: {align1}"
        assert align2 == "----", f"Oczekiwano '----', otrzymano: {align2}"

    def test_allison_global_alignment_custom_scores(self):
        s1 = "AC"
        s2 = "AT"
        score, align1, align2 = allison_global_alignment(s1, s2, match_score=3, mismatch_score=-2, gap_penalty=-3)
        expected_score = 1  # 1 match (3) + 1 mismatch (-2) = 1
        assert score == expected_score, f"Oczekiwano wyniku {expected_score}, otrzymano: {score}"

    def test_allison_local_alignment_identical(self):
        s1 = "ACGT"
        s2 = "ACGT"
        score, align1, align2, start1, start2 = allison_local_alignment(s1, s2)
        expected_score = 8  # 4 matches * 2 points each
        assert score == expected_score, f"Oczekiwano wyniku {expected_score}, otrzymano: {score}"
        assert align1 == "ACGT", f"Oczekiwano 'ACGT', otrzymano: {align1}"
        assert align2 == "ACGT", f"Oczekiwano 'ACGT', otrzymano: {align2}"

    def test_allison_local_alignment_with_mismatch(self):
        s1 = "AAACGTAAA"
        s2 = "TTTACGTTTT"
        score, align1, align2, start1, start2 = allison_local_alignment(s1, s2)
        # Powinno znaleźć lokalne dopasowanie dla "ACGT"
        assert score > 0, f"Lokalny wynik powinien być dodatni, otrzymano: {score}"
        assert "ACGT" in align1 or "ACG" in align1, "Wyrównanie powinno zawierać część wspólną"

    def test_allison_local_alignment_no_match(self):
        s1 = "AAAA"
        s2 = "TTTT"
        score, align1, align2, start1, start2 = allison_local_alignment(s1, s2)
        assert score == 0, f"Oczekiwano wyniku 0 dla braku dopasowania, otrzymano: {score}"

    def test_allison_local_alignment_empty_strings(self):
        s1 = ""
        s2 = ""
        score, align1, align2, start1, start2 = allison_local_alignment(s1, s2)
        assert score == 0, f"Oczekiwano wyniku 0, otrzymano: {score}"

    def test_allison_local_alignment_substring_match(self):
        s1 = "GGGACGTGGG"
        s2 = "ACGT"
        score, align1, align2, start1, start2 = allison_local_alignment(s1, s2)
        expected_score = 8  # Perfect match of "ACGT"
        assert score == expected_score, f"Oczekiwano wyniku {expected_score}, otrzymano: {score}"
        assert align1 == "ACGT", f"Oczekiwano 'ACGT', otrzymano: {align1}"
        assert align2 == "ACGT", f"Oczekiwano 'ACGT', otrzymano: {align2}"

    def test_allison_local_alignment_overlapping_sequences(self):
        s1 = "ACGTACGT"
        s2 = "CGTACG"
        score, align1, align2, start1, start2 = allison_local_alignment(s1, s2)
        assert score > 0, f"Lokalny wynik powinien być dodatni, otrzymano: {score}"
        assert len(align1) == len(align2), "Wyrównania powinny mieć tę samą długość"

    def test_allison_local_vs_global_comparison(self):
        s1 = "AAACGTAAA"
        s2 = "TTTACGTTTT"

        global_score, _, _, = allison_global_alignment(s1, s2)
        local_score, _, _, _, _ = allison_local_alignment(s1, s2)

        # Lokalny wynik powinien być lepszy lub równy globalnemu dla tego przypadku
        assert local_score >= global_score, f"Lokalny wynik ({local_score}) powinien być >= globalnego ({global_score})"


def run_all_tests():
    """Uruchamia wszystkie testy z klasy TestAllisonAlgorithm"""
    test_instance = TestAllisonAlgorithm()

    test_methods = [method for method in dir(test_instance) if method.startswith('test_')]

    print("=== URUCHAMIANIE TESTÓW PROWADZĄCEGO ===\n")

    passed = 0
    failed = 0

    for test_method in test_methods:
        try:
            print(f"Uruchamianie: {test_method}")
            getattr(test_instance, test_method)()
            print(f"✓ PASSED: {test_method}")
            passed += 1
        except AssertionError as e:
            print(f"✗ FAILED: {test_method}")
            print(f"  Błąd: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ ERROR: {test_method}")
            print(f"  Nieoczekiwany błąd: {e}")
            failed += 1
        print()

    print(f"=== PODSUMOWANIE ===")
    print(f"Przeszło: {passed}")
    print(f"Nie przeszło: {failed}")
    print(f"Łącznie testów: {passed + failed}")

    if failed == 0:
        print("🎉 WSZYSTKIE TESTY PRZESZŁY!")
    else:
        print(f"⚠️  {failed} testów nie przeszło")


# Przykłady użycia i testy
if __name__ == "__main__":
    # Najpierw uruchom testy prowadzącego
    run_all_tests()

    print("\n" + "=" * 50)
    print("DODATKOWE PRZYKŁADY DEMONSTRACYJNE")
    print("=" * 50 + "\n")

    # Test 1: Przykład z zadania
    print("=== TEST 1: Przykład z zadania ===")
    s1 = "ACGTACGT"
    s2 = "ACGTGCGT"

    score, align1, align2 = allison_global_alignment(s1, s2)
    print(f"Sekwencje: '{s1}' i '{s2}'")
    print(f"Globalne wyrównanie:")
    print(f"Wynik: {score}")
    print(f"S1: {align1}")
    print(f"S2: {align2}")
    print()

    # Test 2: Lokalne wyrównanie dla tego samego przykładu
    print("=== TEST 2: Lokalne wyrównanie ===")
    score, align1, align2, start1, start2 = allison_local_alignment(s1, s2)
    print(f"Lokalne wyrównanie:")
    print(f"Wynik: {score}")
    print(f"S1: {align1} (start: {start1})")
    print(f"S2: {align2} (start: {start2})")
    print()

    # Test 3: Różne systemy punktacji
    print("=== TEST 3: Różne systemy punktacji ===")
    s3 = "GAATTC"
    s4 = "GGATCC"

    # System 1: Standardowy
    score1, align1_1, align2_1 = allison_global_alignment(s3, s4, 2, -1, -1)
    print(f"System 1 (match=2, mismatch=-1, gap=-1):")
    print(f"Wynik: {score1}, S1: {align1_1}, S2: {align2_1}")

    # System 2: Wyższa kara za luki
    score2, align1_2, align2_2 = allison_global_alignment(s3, s4, 2, -1, -2)
    print(f"System 2 (match=2, mismatch=-1, gap=-2):")
    print(f"Wynik: {score2}, S1: {align1_2}, S2: {align2_2}")

    # System 3: Niższa kara za niedopasowanie
    score3, align1_3, align2_3 = allison_global_alignment(s3, s4, 3, -0.5, -1)
    print(f"System 3 (match=3, mismatch=-0.5, gap=-1):")
    print(f"Wynik: {score3}, S1: {align1_3}, S2: {align2_3}")
    print()

    # Test 4: Porównanie globalnego vs lokalnego
    print("=== TEST 4: Globalne vs Lokalne ===")
    s5 = "AAACGTAAA"
    s6 = "TTTCGTTTT"

    global_score, global_align1, global_align2 = allison_global_alignment(s5, s6)
    local_score, local_align1, local_align2, local_start1, local_start2 = allison_local_alignment(s5, s6)

    print(f"Sekwencje: '{s5}' i '{s6}'")
    print(f"Globalne - Wynik: {global_score}")
    print(f"  S1: {global_align1}")
    print(f"  S2: {global_align2}")
    print(f"Lokalne - Wynik: {local_score}")
    print(f"  S1: {local_align1} (start: {local_start1})")
    print(f"  S2: {local_align2} (start: {local_start2})")
    print()

    # Test 5: Przypadek z wieloma lukami
    print("=== TEST 5: Przypadek z lukami ===")
    s7 = "ATCG"
    s8 = "AATTCCGG"

    score, align1, align2 = allison_global_alignment(s7, s8)
    print(f"Sekwencje: '{s7}' i '{s8}'")
    print(f"Globalne wyrównanie:")
    print(f"Wynik: {score}")
    print(f"S1: {align1}")
    print(f"S2: {align2}")
    print()

    local_score, local_align1, local_align2, local_start1, local_start2 = allison_local_alignment(s7, s8)
    print(f"Lokalne wyrównanie:")
    print(f"Wynik: {local_score}")
    print(f"S1: {local_align1} (start: {local_start1})")
    print(f"S2: {local_align2} (start: {local_start2})")