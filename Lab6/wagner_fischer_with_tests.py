def wagner_fischer(s1: str, s2: str,
                   insert_cost: int = 1,
                   delete_cost: int = 1,
                   substitute_cost: int = 1) -> int:
    """
    Oblicza odległość edycyjną używając algorytmu Wagnera-Fischera (programowanie dynamiczne).

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków
        insert_cost: Koszt operacji wstawienia
        delete_cost: Koszt operacji usunięcia
        substitute_cost: Koszt operacji zamiany

    Returns:
        Odległość edycyjna z uwzględnieniem kosztów operacji
    """
    # Obsługa przypadków brzegowych
    if not s1:
        return len(s2) * insert_cost
    if not s2:
        return len(s1) * delete_cost

    m, n = len(s1), len(s2)

    # Inicjalizacja macierzy DP
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Inicjalizacja pierwszego wiersza i kolumny
    for i in range(1, m + 1):
        dp[i][0] = i * delete_cost

    for j in range(1, n + 1):
        dp[0][j] = j * insert_cost

    # Wypełnianie macierzy DP
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # Znaki są identyczne - brak kosztu
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Wybieramy minimum z trzech operacji
                dp[i][j] = min(
                    dp[i - 1][j] + delete_cost,  # Usunięcie
                    dp[i][j - 1] + insert_cost,  # Wstawienie
                    dp[i - 1][j - 1] + substitute_cost  # Zamiana
                )

    return dp[m][n]


def wagner_fischer_with_alignment(s1: str, s2: str) -> tuple[int, str, str]:
    """
    Oblicza odległość edycyjną i zwraca wyrównanie sekwencji.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Krotka zawierająca odległość edycyjną i dwa wyrównane ciągi
        (w wyrównanych ciągach '-' oznacza lukę)
    """
    # Obsługa przypadków brzegowych
    if not s1:
        return len(s2), '-' * len(s2), s2
    if not s2:
        return len(s1), s1, '-' * len(s1)

    m, n = len(s1), len(s2)

    # Inicjalizacja macierzy DP
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Inicjalizacja pierwszego wiersza i kolumny
    for i in range(1, m + 1):
        dp[i][0] = i

    for j in range(1, n + 1):
        dp[0][j] = j

    # Wypełnianie macierzy DP
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # Usunięcie
                    dp[i][j - 1] + 1,  # Wstawienie
                    dp[i - 1][j - 1] + 1  # Zamiana
                )

    # Backtracking do znalezienia wyrównania
    aligned_s1, aligned_s2 = [], []
    i, j = m, n

    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            # Znaki są identyczne
            aligned_s1.append(s1[i - 1])
            aligned_s2.append(s2[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            # Zamiana
            aligned_s1.append(s1[i - 1])
            aligned_s2.append(s2[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            # Usunięcie z s1
            aligned_s1.append(s1[i - 1])
            aligned_s2.append('-')
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            # Wstawienie do s1
            aligned_s1.append('-')
            aligned_s2.append(s2[j - 1])
            j -= 1
        else:
            # Sytuacja awaryjna - nie powinna się zdarzyć
            break

    # Odwrócenie sekwencji (były budowane od końca)
    aligned_s1.reverse()
    aligned_s2.reverse()

    return dp[m][n], ''.join(aligned_s1), ''.join(aligned_s2)


def wagner_fischer_space_optimized(s1: str, s2: str) -> int:
    """
    Oblicza odległość edycyjną używając zoptymalizowanej pamięciowo wersji algorytmu.
    Złożoność pamięciowa: O(min(m,n)) zamiast O(m*n)

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość edycyjna
    """
    # Obsługa przypadków brzegowych
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)

    # Zapewniamy, że s1 jest krótszym ciągiem dla optymalizacji pamięci
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    m, n = len(s1), len(s2)

    # Używamy tylko dwóch wierszy zamiast całej macierzy
    prev_row = list(range(m + 1))
    curr_row = [0] * (m + 1)

    for j in range(1, n + 1):
        curr_row[0] = j

        for i in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                curr_row[i] = prev_row[i - 1]
            else:
                curr_row[i] = min(
                    prev_row[i] + 1,  # Usunięcie
                    curr_row[i - 1] + 1,  # Wstawienie
                    prev_row[i - 1] + 1  # Zamiana
                )

        # Zamiana wierszy
        prev_row, curr_row = curr_row, prev_row

    return prev_row[m]


# Klasa testowa zgodna z testami prowadzącego
class TestWagnerFischer:
    def test_wagner_fischer_equal_strings(self):
        s1 = "algorytm"
        s2 = "algorytm"
        result = wagner_fischer(s1, s2)
        expected = 0
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_one_substitution(self):
        s1 = "cat"
        s2 = "bat"
        result = wagner_fischer(s1, s2)
        expected = 1
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_one_insertion(self):
        s1 = "cat"
        s2 = "cart"
        result = wagner_fischer(s1, s2)
        expected = 1
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_one_deletion(self):
        s1 = "cart"
        s2 = "cat"
        result = wagner_fischer(s1, s2)
        expected = 1
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_multiple_operations(self):
        s1 = "kitten"
        s2 = "sitting"
        result = wagner_fischer(s1, s2)
        expected = 3
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_empty_strings(self):
        s1 = ""
        s2 = ""
        result = wagner_fischer(s1, s2)
        expected = 0
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_one_empty_string(self):
        s1 = "abc"
        s2 = ""
        result = wagner_fischer(s1, s2)
        expected = 3
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_custom_costs(self):
        s1 = "cat"
        s2 = "bat"
        result = wagner_fischer(s1, s2, insert_cost=2, delete_cost=2, substitute_cost=3)
        expected = 3
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_with_alignment_no_gaps(self):
        s1 = "abc"
        s2 = "abc"
        distance, align1, align2 = wagner_fischer_with_alignment(s1, s2)
        assert distance == 0, f"Oczekiwano odległość 0, otrzymano: {distance}"
        assert align1 == "abc", f"Oczekiwano 'abc', otrzymano: {align1}"
        assert align2 == "abc", f"Oczekiwano 'abc', otrzymano: {align2}"

    def test_wagner_fischer_with_alignment_only_insertions(self):
        s1 = ""
        s2 = "abc"
        distance, align1, align2 = wagner_fischer_with_alignment(s1, s2)
        assert distance == 3, f"Oczekiwano odległość 3, otrzymano: {distance}"
        assert align1 == "---", f"Oczekiwano '---', otrzymano: {align1}"
        assert align2 == "abc", f"Oczekiwano 'abc', otrzymano: {align2}"

    def test_wagner_fischer_with_alignment_only_deletions(self):
        s1 = "abc"
        s2 = ""
        distance, align1, align2 = wagner_fischer_with_alignment(s1, s2)
        assert distance == 3, f"Oczekiwano odległość 3, otrzymano: {distance}"
        assert align1 == "abc", f"Oczekiwano 'abc', otrzymano: {align1}"
        assert align2 == "---", f"Oczekiwano '---', otrzymano: {align2}"

    def test_wagner_fischer_space_optimized(self):
        s1 = "kitten"
        s2 = "sitting"
        result = wagner_fischer_space_optimized(s1, s2)
        expected = 3
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_space_optimized_empty(self):
        s1 = ""
        s2 = "abc"
        result = wagner_fischer_space_optimized(s1, s2)
        expected = 3
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_space_optimized_equal(self):
        s1 = "test"
        s2 = "test"
        result = wagner_fischer_space_optimized(s1, s2)
        expected = 0
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_long_strings(self):
        s1 = "a" * 100
        s2 = "b" * 100
        result = wagner_fischer(s1, s2)
        expected = 100
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_consistency_between_versions(self):
        s1 = "intention"
        s2 = "execution"
        result1 = wagner_fischer(s1, s2)
        result2 = wagner_fischer_space_optimized(s1, s2)
        distance, _, _ = wagner_fischer_with_alignment(s1, s2)

        assert result1 == result2 == distance, f"Wszystkie wersje powinny zwracać tę samą odległość: {result1}, {result2}, {distance}"


def run_all_tests():
    """Uruchamia wszystkie testy"""
    test_instance = TestWagnerFischer()

    test_methods = [method for method in dir(test_instance) if method.startswith('test_')]

    passed = 0
    failed = 0

    print("=== Uruchamianie testów prowadzącego ===\n")

    for test_method in test_methods:
        try:
            getattr(test_instance, test_method)()
            print(f"✅ {test_method} - PASSED")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test_method} - FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"💥 {test_method} - ERROR: {e}")
            failed += 1

    print(f"\n=== Podsumowanie ===")
    print(f"Testy zaliczone: {passed}")
    print(f"Testy niezaliczone: {failed}")
    print(f"Łącznie: {passed + failed}")

    if failed == 0:
        print("\n🎉 Wszystkie testy przeszły pomyślnie!")
    else:
        print(f"\n⚠️  {failed} testów wymaga poprawki")


# Dodatkowe testy i przykłady
def demo_examples():
    """Demonstracja działania algorytmu"""
    print("\n=== Przykłady działania algorytmu ===\n")

    # Przykład z zadania
    s1, s2 = "GCATGCU", "GATTACA"
    distance = wagner_fischer(s1, s2)
    distance_align, align1, align2 = wagner_fischer_with_alignment(s1, s2)

    print(f"Przykład z zadania:")
    print(f"s1 = '{s1}'")
    print(f"s2 = '{s2}'")
    print(f"Odległość edycyjna: {distance}")
    print(f"Wyrównanie: '{align1}' -> '{align2}'")
    print()

    # Inne przykłady
    examples = [
        ("kitten", "sitting"),
        ("intention", "execution"),
        ("saturday", "sunday")
    ]

    for s1, s2 in examples:
        distance = wagner_fischer(s1, s2)
        _, align1, align2 = wagner_fischer_with_alignment(s1, s2)
        print(f"'{s1}' -> '{s2}': odległość = {distance}")
        print(f"Wyrównanie: '{align1}' -> '{align2}'")
        print()


if __name__ == "__main__":
    run_all_tests()
    demo_examples()