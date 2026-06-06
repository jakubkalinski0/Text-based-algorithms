from Lab3.naive_pattern_matching import naive_pattern_match


class TestNaivePatternMatching:
    def test_basic_matching(self):
        text = "ABABDABACDABABCABAB"
        pattern = "ABABC"
        expected = [10]
        result = naive_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_multiple_matches(self):
        text = "ABABABABABA"
        pattern = "ABA"
        expected = [0, 2, 4, 6, 8]
        result = naive_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_no_match(self):
        text = "ABCDEFGHIJKLMN"
        pattern = "XYZ"
        expected = []
        result = naive_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_pattern_at_beginning(self):
        text = "ABCDEFGHIJK"
        pattern = "ABC"
        expected = [0]
        result = naive_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_pattern_at_end(self):
        text = "ABCDEFGHIJK"
        pattern = "IJK"
        expected = [8]
        result = naive_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_empty_pattern(self):
        text = "ABCDEFG"
        pattern = ""
        expected = []
        result = naive_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_empty_text(self):
        text = ""
        pattern = "ABC"
        expected = []
        result = naive_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_pattern_equals_text(self):
        text = "ABCDEF"
        pattern = "ABCDEF"
        expected = [0]
        result = naive_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_overlapping_matches(self):
        text = "AAAAAA"
        pattern = "AAA"
        expected = [0, 1, 2, 3]
        result = naive_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"