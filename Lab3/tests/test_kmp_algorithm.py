from Lab3.kmp_algorithm import compute_lps_array, kmp_pattern_match


class TestKMPAlgorithm:
    def test_compute_lps_array(self):
        pattern = "ABABACA"
        expected = [0, 0, 1, 2, 3, 0, 1]
        lps = compute_lps_array(pattern)
        assert lps == expected, f"Expected {expected}, got {lps}"

        pattern = "AAAA"
        expected = [0, 1, 2, 3]
        lps = compute_lps_array(pattern)
        assert lps == expected, f"Expected {expected}, got {lps}"

        pattern = "ABCDEABC"
        expected = [0, 0, 0, 0, 0, 1, 2, 3]
        lps = compute_lps_array(pattern)
        assert lps == expected, f"Expected {expected}, got {lps}"

    def test_basic_pattern_matching(self):
        text = "ABABDABACDABABCABAB"
        pattern = "ABABC"
        expected = [10]
        result = kmp_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_multiple_matches(self):
        text = "ABABABABABA"
        pattern = "ABA"
        expected = [0, 2, 4, 6, 8]
        result = kmp_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_no_match(self):
        text = "ABCDEFGHIJKLMN"
        pattern = "XYZ"
        expected = []
        result = kmp_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_empty_pattern(self):
        text = "ABCDEFG"
        pattern = ""
        expected = []
        result = kmp_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_empty_text(self):
        text = ""
        pattern = "ABC"
        expected = []
        result = kmp_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_pattern_with_repeated_prefix(self):
        text = "AAAABAAAAABAAAA"
        pattern = "AAAAAB"
        expected = [5]
        result = kmp_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_long_text_and_pattern(self):
        text = "AABAABAACAADAABAAABAA"
        pattern = "AABAA"
        expected = [0, 3, 12, 16]
        result = kmp_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"