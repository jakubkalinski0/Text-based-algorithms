from Lab6.wagner_fischer import (
    wagner_fischer,
    wagner_fischer_with_alignment,
    wagner_fischer_space_optimized
)


class TestWagnerFischer:
    def test_wagner_fischer_equal_strings(self):
        s1 = "algorytm"
        s2 = "algorytm"
        result = wagner_fischer(s1, s2)
        expected = 0
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_one_substitution(self):
        s1 = "cat"
        s2 = "bat"
        result = wagner_fischer(s1, s2)
        expected = 1
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_one_insertion(self):
        s1 = "cat"
        s2 = "cart"
        result = wagner_fischer(s1, s2)
        expected = 1
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_one_deletion(self):
        s1 = "cart"
        s2 = "cat"
        result = wagner_fischer(s1, s2)
        expected = 1
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_multiple_operations(self):
        s1 = "kitten"
        s2 = "sitting"
        result = wagner_fischer(s1, s2)
        expected = 3
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_empty_strings(self):
        s1 = ""
        s2 = ""
        result = wagner_fischer(s1, s2)
        expected = 0
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_one_empty_string(self):
        s1 = "abc"
        s2 = ""
        result = wagner_fischer(s1, s2)
        expected = 3
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_custom_costs(self):
        s1 = "cat"
        s2 = "bat"
        result = wagner_fischer(s1, s2, insert_cost=2, delete_cost=2, substitute_cost=3)
        expected = 3
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_with_alignment_no_gaps(self):
        s1 = "abc"
        s2 = "abc"
        distance, align1, align2 = wagner_fischer_with_alignment(s1, s2)
        assert distance == 0, f"Oczekiwano odległość 0, otrzymano: {distance}"
        assert align1 == "abc", f"Oczekiwano 'abc', otrzymano: {align1}"
        assert align2 == "abc", f"Oczekiwano 'abc', otrzymano: {align2}"

    def test_wagner_fischer_with_alignment_only_insertions(self):
        s1 = ""
        s2 = "abc"
        distance, align1, align2 = wagner_fischer_with_alignment(s1, s2)
        assert distance == 3, f"Oczekiwano odległość 3, otrzymano: {distance}"
        assert align1 == "---", f"Oczekiwano '---', otrzymano: {align1}"
        assert align2 == "abc", f"Oczekiwano 'abc', otrzymano: {align2}"

    def test_wagner_fischer_with_alignment_only_deletions(self):
        s1 = "abc"
        s2 = ""
        distance, align1, align2 = wagner_fischer_with_alignment(s1, s2)
        assert distance == 3, f"Oczekiwano odległość 3, otrzymano: {distance}"
        assert align1 == "abc", f"Oczekiwano 'abc', otrzymano: {align1}"
        assert align2 == "---", f"Oczekiwano '---', otrzymano: {align2}"

    def test_wagner_fischer_space_optimized(self):
        s1 = "kitten"
        s2 = "sitting"
        result = wagner_fischer_space_optimized(s1, s2)
        expected = 3
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_space_optimized_empty(self):
        s1 = ""
        s2 = "abc"
        result = wagner_fischer_space_optimized(s1, s2)
        expected = 3
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_space_optimized_equal(self):
        s1 = "test"
        s2 = "test"
        result = wagner_fischer_space_optimized(s1, s2)
        expected = 0
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_wagner_fischer_long_strings(self):
        s1 = "a" * 100
        s2 = "b" * 100
        result = wagner_fischer(s1, s2)
        expected = 100
        assert result == expected, f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_consistency_between_versions(self):
        s1 = "intention"
        s2 = "execution"
        result1 = wagner_fischer(s1, s2)
        result2 = wagner_fischer_space_optimized(s1, s2)
        distance, _, _ = wagner_fischer_with_alignment(s1, s2)

        assert result1 == result2 == distance, f"Wszystkie wersje powinny zwracać tę samą odległość: {result1}, {result2}, {distance}"