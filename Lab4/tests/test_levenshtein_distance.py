from Lab4.levenshtein_distance import levenshtein_distance


class TestLevenshteinDistance:
    def test_levenshtein_equal_strings(self):
        s1 = "algorytm"
        s2 = "algorytm"
        result = levenshtein_distance(s1, s2)
        expected = 0
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_levenshtein_one_substitution(self):
        s1 = "sobota"
        s2 = "robota"
        result = levenshtein_distance(s1, s2)
        expected = 1
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_levenshtein_one_insertion(self):
        s1 = "szala"
        s2 = "szpala"
        result = levenshtein_distance(s1, s2)
        expected = 1
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_levenshtein_one_deletion(self):
        s1 = "pralka"
        s2 = "praka"
        result = levenshtein_distance(s1, s2)
        expected = 1
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_levenshtein_multiple_operations(self):
        s1 = "kitten"
        s2 = "sitting"
        result = levenshtein_distance(s1, s2)
        expected = 3
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_levenshtein_empty_strings(self):
        s1 = ""
        s2 = ""
        result = levenshtein_distance(s1, s2)
        expected = 0
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_levenshtein_one_empty_string(self):
        s1 = "algorytm"
        s2 = ""
        result = levenshtein_distance(s1, s2)
        expected = 8
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

        s1 = ""
        s2 = "algorytm"
        result = levenshtein_distance(s1, s2)
        expected = 8
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_levenshtein_completely_different(self):
        s1 = "abcdef"
        s2 = "ghijkl"
        result = levenshtein_distance(s1, s2)
        expected = 6
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"