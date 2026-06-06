from Lab4.fuzzy_matching import hamming_distance, fuzzy_shift_or


class TestFuzzyMatching:
    def test_hamming_distance_equal(self):
        s1 = "algorytm"
        s2 = "algorytm"
        result = hamming_distance(s1, s2)
        expected = 0
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_hamming_distance_different(self):
        s1 = "algorytm"
        s2 = "altorynm"
        result = hamming_distance(s1, s2)
        expected = 2
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_hamming_distance_completely_different(self):
        s1 = "abcdef"
        s2 = "ghijkl"
        result = hamming_distance(s1, s2)
        expected = 6
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_hamming_distance_different_lengths(self):
        s1 = "algorytm"
        s2 = "algo"
        result = hamming_distance(s1, s2)
        expected = -1
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_hamming_distance_empty(self):
        s1 = ""
        s2 = ""
        result = hamming_distance(s1, s2)
        expected = 0
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_fuzzy_shift_or_exact_match(self):
        text = "abcdefabcde"
        pattern = "abc"
        k = 0
        result = fuzzy_shift_or(text, pattern, k)
        expected = [0, 6]
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_fuzzy_shift_or_one_mismatch(self):
        text = "abcdefabcde"
        pattern = "abc"
        k = 1
        result = fuzzy_shift_or(text, pattern, k)
        expected = [0, 6]
        assert sorted(result) == sorted(expected), f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_fuzzy_shift_or_two_mismatches(self):
        text = "abcdefabcde"
        pattern = "abc"
        k = 2
        result = fuzzy_shift_or(text, pattern, k)
        expected = [0, 6]
        assert sorted(result) == sorted(expected), f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_fuzzy_shift_or_no_match(self):
        text = "abcdefabcde"
        pattern = "xyz"
        k = 2
        result = fuzzy_shift_or(text, pattern, k)
        expected = []
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_fuzzy_shift_or_empty_pattern(self):
        text = "abcdef"
        pattern = ""
        k = 2
        result = fuzzy_shift_or(text, pattern, k)
        expected = []
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_fuzzy_shift_or_empty_text(self):
        text = ""
        pattern = "abc"
        k = 2
        result = fuzzy_shift_or(text, pattern, k)
        expected = []
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_fuzzy_shift_or_negative_k(self):
        text = "abcdef"
        pattern = "abc"
        k = -1
        result = fuzzy_shift_or(text, pattern, k)
        expected = []
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_fuzzy_shift_or_pattern_longer_than_text(self):
        text = "abc"
        pattern = "abcdef"
        k = 2
        result = fuzzy_shift_or(text, pattern, k)
        expected = []
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"