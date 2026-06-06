from Lab4.two_dimensional_search import find_pattern_2d


class TestTwoDimensionalSearch:
    def test_multiple_matches(self):
        text = [
            "abcabc",
            "defdef",
            "abcabc"
        ]
        pattern = [
            "abc",
            "def"
        ]
        result = find_pattern_2d(text, pattern)
        expected = [(0, 0), (0, 3)]
        assert sorted(result) == sorted(expected), f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_no_match(self):
        text = [
            "abcdef",
            "ghijkl",
            "mnopqr"
        ]
        pattern = [
            "xyz",
            "123"
        ]
        result = find_pattern_2d(text, pattern)
        expected = []
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_pattern_at_edge(self):
        text = [
            "abcdef",
            "ghijkl",
            "mnopqr"
        ]
        pattern = [
            "ab",
            "gh"
        ]
        result = find_pattern_2d(text, pattern)
        expected = [(0, 0)]
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_pattern_equals_text(self):
        text = [
            "abc",
            "def"
        ]
        pattern = [
            "abc",
            "def"
        ]
        result = find_pattern_2d(text, pattern)
        expected = [(0, 0)]
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_empty_pattern(self):
        text = [
            "abcdef",
            "ghijkl"
        ]
        pattern = []
        result = find_pattern_2d(text, pattern)
        expected = []
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_empty_text(self):
        text = []
        pattern = [
            "abc",
            "def"
        ]
        result = find_pattern_2d(text, pattern)
        expected = []
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_pattern_larger_than_text(self):
        text = [
            "abc",
            "def"
        ]
        pattern = [
            "abcd",
            "efgh",
            "ijkl"
        ]
        result = find_pattern_2d(text, pattern)
        expected = []
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_one_dimensional_pattern(self):
        text = [
            "abcdef",
            "ghijkl",
            "mnopqr"
        ]
        pattern = [
            "abc"
        ]
        result = find_pattern_2d(text, pattern)
        expected = [(0, 0)]
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_one_dimensional_text(self):
        text = [
            "abcdefghi"
        ]
        pattern = [
            "def"
        ]
        result = find_pattern_2d(text, pattern)
        expected = [(0, 3)]
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_overlapping_matches(self):
        text = [
            "aaaaaa",
            "aaaaaa",
            "aaaaaa"
        ]
        pattern = [
            "aaa",
            "aaa"
        ]
        result = find_pattern_2d(text, pattern)
        expected = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3)]
        assert sorted(result) == sorted(expected), f"Oczekiwano: {expected}, otrzymano: {result}"