from Lab4.shift_or_algorithm import set_nth_bit, nth_bit, make_mask, shift_or


class TestShiftOrAlgorithm:
    def test_set_nth_bit(self):
        assert set_nth_bit(0) == 1, "Błąd przy ustawianiu bitu na pozycji 0"
        assert set_nth_bit(1) == 2, "Błąd przy ustawianiu bitu na pozycji 1"
        assert set_nth_bit(2) == 4, "Błąd przy ustawianiu bitu na pozycji 2"
        assert set_nth_bit(7) == 128, "Błąd przy ustawianiu bitu na pozycji 7"

    def test_nth_bit(self):
        assert nth_bit(0, 0) == 0, "Błąd przy odczytywaniu bitu 0 z 0"
        assert nth_bit(1, 0) == 1, "Błąd przy odczytywaniu bitu 0 z 1"
        assert nth_bit(2, 1) == 1, "Błąd przy odczytywaniu bitu 1 z 2"
        assert nth_bit(7, 0) == 1, "Błąd przy odczytywaniu bitu 0 z 7"
        assert nth_bit(7, 1) == 1, "Błąd przy odczytywaniu bitu 1 z 7"
        assert nth_bit(7, 2) == 1, "Błąd przy odczytywaniu bitu 2 z 7"
        assert nth_bit(7, 3) == 0, "Błąd przy odczytywaniu bitu 3 z 7"

    def test_make_mask(self):
        pattern = "ABC"
        masks = make_mask(pattern)

        assert nth_bit(masks[ord('A')], 0) == 0, "Błąd w masce dla znaku 'A'"
        assert nth_bit(masks[ord('B')], 1) == 0, "Błąd w masce dla znaku 'B'"
        assert nth_bit(masks[ord('C')], 2) == 0, "Błąd w masce dla znaku 'C'"

        assert nth_bit(masks[ord('X')], 0) == 1, "Błąd w masce dla znaku 'X'"
        assert nth_bit(masks[ord('X')], 1) == 1, "Błąd w masce dla znaku 'X'"
        assert nth_bit(masks[ord('X')], 2) == 1, "Błąd w masce dla znaku 'X'"

        empty_masks = make_mask("")
        assert all(m == 0xff for m in empty_masks), "Błąd w maskach dla pustego wzorca"

    def test_shift_or_basic(self):
        text = "ABABCABCABC"
        pattern = "ABC"
        result = shift_or(text, pattern)
        expected = [2, 5, 8]
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_shift_or_multiple_matches(self):
        text = "ABABABABABA"
        pattern = "ABA"
        result = shift_or(text, pattern)
        expected = [0, 2, 4, 6, 8]
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_shift_or_no_match(self):
        text = "ABCDEF"
        pattern = "XYZ"
        result = shift_or(text, pattern)
        expected = []
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_shift_or_empty_pattern(self):
        text = "ABCDEF"
        pattern = ""
        result = shift_or(text, pattern)
        expected = []
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_shift_or_empty_text(self):
        text = ""
        pattern = "ABC"
        result = shift_or(text, pattern)
        expected = []
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_shift_or_pattern_equals_text(self):
        text = "ABC"
        pattern = "ABC"
        result = shift_or(text, pattern)
        expected = [0]
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_shift_or_pattern_longer_than_text(self):
        text = "ABC"
        pattern = "ABCDEF"
        result = shift_or(text, pattern)
        expected = []
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"