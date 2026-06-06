from Lab3.boyer_moore_algorithm import (
    compute_bad_character_table,
    compute_good_suffix_table,
    boyer_moore_pattern_match
)


class TestBoyerMooreAlgorithm:
    def test_compute_bad_character_table(self):
        pattern = "ABCABC"
        expected = {'A': 3, 'B': 4, 'C': 5}
        bad_char = compute_bad_character_table(pattern)
        assert bad_char == expected, f"Expected {expected}, got {bad_char}"

        pattern = "ABCDEF"
        expected = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}
        bad_char = compute_bad_character_table(pattern)
        assert bad_char == expected, f"Expected {expected}, got {bad_char}"

        pattern = "AAAA"
        expected = {'A': 3}
        bad_char = compute_bad_character_table(pattern)
        assert bad_char == expected, f"Expected {expected}, got {bad_char}"

        pattern = ""
        expected = {}
        bad_char = compute_bad_character_table(pattern)
        assert bad_char == expected, f"Expected {expected}, got {bad_char}"

    def test_compute_good_suffix_table(self):
        pattern = "AABA"
        good_suffix = compute_good_suffix_table(pattern)
        assert len(good_suffix) == len(pattern) + 1, f"Expected length {len(pattern) + 1}, got {len(good_suffix)}"

        pattern = "AAAA"
        expected = [1, 1, 2, 3, 4]
        good_suffix = compute_good_suffix_table(pattern)
        assert good_suffix == expected, f"Expected {expected}, got {good_suffix}"

        pattern = "ABCD"
        good_suffix = compute_good_suffix_table(pattern)
        assert len(good_suffix) == len(pattern) + 1, f"Expected length {len(pattern) + 1}, got {len(good_suffix)}"

        pattern = "ABCABC"
        good_suffix = compute_good_suffix_table(pattern)
        assert len(good_suffix) == len(pattern) + 1, f"Expected length {len(pattern) + 1}, got {len(good_suffix)}"

    def test_basic_pattern_matching(self):
        text = "ABABDABACDABABCABAB"
        pattern = "ABABC"
        expected = [10]
        result = boyer_moore_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_multiple_matches(self):
        text = "ABABABABABA"
        pattern = "ABA"
        expected = [0, 2, 4, 6, 8]
        result = boyer_moore_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_no_match(self):
        text = "ABCDEFGHIJKLMN"
        pattern = "XYZ"
        expected = []
        result = boyer_moore_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_empty_pattern(self):
        text = "ABCDEFG"
        pattern = ""
        expected = []
        result = boyer_moore_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_empty_text(self):
        text = ""
        pattern = "ABC"
        expected = []
        result = boyer_moore_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_pattern_at_beginning_and_end(self):
        text = "ABCABCABC"
        pattern = "ABC"
        expected = [0, 3, 6]
        result = boyer_moore_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_long_pattern(self):
        text = "THISISATEST"
        pattern = "ISATEST"
        expected = [4]
        result = boyer_moore_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_worst_case_scenario(self):
        text = "AAAAAAAAAAAA"
        pattern = "AAAA"
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        result = boyer_moore_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"