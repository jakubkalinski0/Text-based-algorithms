from Lab6.naive_edit_distance import naive_edit_distance, naive_edit_distance_with_operations


class TestNaiveEditDistance:
    def test_naive_edit_distance_equal_strings(self):
        s1 = "algorytm"
        s2 = "algorytm"
        result = naive_edit_distance(s1, s2)
        expected = 0
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_naive_edit_distance_one_substitution(self):
        s1 = "cat"
        s2 = "bat"
        result = naive_edit_distance(s1, s2)
        expected = 1
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_naive_edit_distance_one_insertion(self):
        s1 = "cat"
        s2 = "cart"
        result = naive_edit_distance(s1, s2)
        expected = 1
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_naive_edit_distance_one_deletion(self):
        s1 = "cart"
        s2 = "cat"
        result = naive_edit_distance(s1, s2)
        expected = 1
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_naive_edit_distance_multiple_operations(self):
        s1 = "kitten"
        s2 = "sitting"
        result = naive_edit_distance(s1, s2)
        expected = 3
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_naive_edit_distance_empty_strings(self):
        s1 = ""
        s2 = ""
        result = naive_edit_distance(s1, s2)
        expected = 0
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_naive_edit_distance_one_empty_string(self):
        s1 = "abc"
        s2 = ""
        result = naive_edit_distance(s1, s2)
        expected = 3
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

        s1 = ""
        s2 = "abc"
        result = naive_edit_distance(s1, s2)
        expected = 3
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_naive_edit_distance_completely_different(self):
        s1 = "abc"
        s2 = "xyz"
        result = naive_edit_distance(s1, s2)
        expected = 3
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_naive_edit_distance_with_operations_basic(self):
        s1 = "cat"
        s2 = "bat"
        distance, operations = naive_edit_distance_with_operations(s1, s2)
        assert distance == 1, f"Oczekiwano odległość 1, otrzymano: {distance}"
        assert len(operations) == 3, f"Oczekiwano 3 operacje, otrzymano: {len(operations)}"

    def test_naive_edit_distance_with_operations_empty(self):
        s1 = ""
        s2 = "abc"
        distance, operations = naive_edit_distance_with_operations(s1, s2)
        assert distance == 3, f"Oczekiwano odległość 3, otrzymano: {distance}"
        insert_count = sum(1 for op in operations if op.startswith("INSERT"))
        assert insert_count == 3, f"Oczekiwano 3 operacje INSERT, otrzymano: {insert_count}"

    def test_naive_edit_distance_with_operations_same_strings(self):
        s1 = "abc"
        s2 = "abc"
        distance, operations = naive_edit_distance_with_operations(s1, s2)
        assert distance == 0, f"Oczekiwano odległość 0, otrzymano: {distance}"
        match_count = sum(1 for op in operations if op.startswith("MATCH"))
        assert match_count == 3, f"Oczekiwano 3 operacje MATCH, otrzymano: {match_count}"

    def test_naive_edit_distance_longer_strings(self):
        s1 = "intention"
        s2 = "execution"
        result = naive_edit_distance(s1, s2)
        expected = 5
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"