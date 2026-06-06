from Lab3.z_algorithm import compute_z_array, z_pattern_match


class TestZAlgorithm:
    def test_compute_z_array(self):
        s = "aabcaabxaaz"
        expected = [0, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]
        z = compute_z_array(s)
        assert z == expected, f"Expected {expected}, got {z}"

        s = "abababab"
        expected = [0, 0, 6, 0, 4, 0, 2, 0]
        z = compute_z_array(s)
        assert z == expected, f"Expected {expected}, got {z}"

        s = "aaaaaa"
        expected = [0, 5, 4, 3, 2, 1]
        z = compute_z_array(s)
        assert z == expected, f"Expected {expected}, got {z}"

    def test_basic_pattern_matching(self):
        text = "ABABDABACDABABCABAB"
        pattern = "ABABC"
        expected = [10]
        result = z_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_multiple_matches(self):
        text = "ABABABABABA"
        pattern = "ABA"
        expected = [0, 2, 4, 6, 8]
        result = z_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_no_match(self):
        text = "ABCDEFGHIJKLMN"
        pattern = "XYZ"
        expected = []
        result = z_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_empty_pattern(self):
        text = "ABCDEFG"
        pattern = ""
        expected = []
        result = z_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_empty_text(self):
        text = ""
        pattern = "ABC"
        expected = []
        result = z_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_pattern_at_beginning_and_end(self):
        text = "ABCABCABC"
        pattern = "ABC"
        expected = [0, 3, 6]
        result = z_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_overlapping_patterns(self):
        text = "AAAAA"
        pattern = "AA"
        expected = [0, 1, 2, 3]
        result = z_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_special_characters(self):
        text = "ab$cd$ef"
        pattern = "ab$"
        expected = [0]
        result = z_pattern_match(text, pattern)
        assert result == expected, f"Expected {expected}, got {result}"