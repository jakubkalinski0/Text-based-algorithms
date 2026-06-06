from Lab3.rabin_karp_algorithm import rabin_karp_pattern_match


class TestRabinKarpAlgorithm:
    def test_basic_pattern_matching(self):
        text = "ABABDABACDABABCABAB"
        pattern = "ABABC"
        expected = [10]
        result = rabin_karp_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_multiple_matches(self):
        text = "ABABABABABA"
        pattern = "ABA"
        expected = [0, 2, 4, 6, 8]
        result = rabin_karp_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_no_match(self):
        text = "ABCDEFGHIJKLMN"
        pattern = "XYZ"
        expected = []
        result = rabin_karp_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_empty_pattern(self):
        text = "ABCDEFG"
        pattern = ""
        expected = []
        result = rabin_karp_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_empty_text(self):
        text = ""
        pattern = "ABC"
        expected = []
        result = rabin_karp_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_pattern_at_beginning_and_end(self):
        text = "ABCABCABC"
        pattern = "ABC"
        expected = [0, 3, 6]
        result = rabin_karp_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_pattern_with_hash_collisions(self):
        text = "AAAABAAABA"
        pattern = "AAAA"
        expected = [0]
        result = rabin_karp_pattern_match(text, pattern, prime=3)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_long_text_short_pattern(self):
        text = "A" * 1000 + "B" + "A" * 1000
        pattern = "AB"
        expected = [999]
        result = rabin_karp_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"