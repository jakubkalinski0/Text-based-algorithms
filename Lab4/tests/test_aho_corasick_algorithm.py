import pytest

from Lab4.aho_corasick_algorithm import AhoCorasick


class TestAhoCorasick:
    def test_basic(self):
        patterns = ["he", "she", "his", "hers"]
        text = "ushers"
        ac = AhoCorasick(patterns)
        result = ac.search(text)
        result.sort(key=lambda x: (x[0], len(x[1])))
        expected = [(1, "she"), (2, "he"), (2, "hers")]
        assert result == expected

    def test_multiple_patterns(self):
        patterns = ["a", "ab", "bc", "bca", "c", "caa"]
        text = "abccab"
        ac = AhoCorasick(patterns)
        result = ac.search(text)
        result.sort(key=lambda x: (x[0], len(x[1])))
        expected = [(0, "a"), (0, "ab"), (1, "bc"), (2, "c"), (3, "c"), (4, "a"), (4, "ab")]
        assert result == expected

    def test_overlapping_patterns(self):
        patterns = ["abcd", "bcde", "cdef"]
        text = "abcdefg"
        ac = AhoCorasick(patterns)
        result = ac.search(text)
        result.sort(key=lambda x: (x[0], len(x[1])))
        expected = [(0, "abcd"), (1, "bcde"), (2, "cdef")]
        assert result == expected

    def test_no_match(self):
        patterns = ["xyz", "abc"]
        text = "defghi"
        ac = AhoCorasick(patterns)
        result = ac.search(text)
        assert result == []

    def test_empty_pattern(self):
        patterns = ["", "abc"]
        text = "abcdef"
        ac = AhoCorasick(patterns)
        result = ac.search(text)
        expected = [(0, "abc")]
        assert result == expected

    def test_empty_text(self):
        patterns = ["abc", "def"]
        text = ""
        ac = AhoCorasick(patterns)
        result = ac.search(text)
        assert result == []

    def test_pattern_equals_text(self):
        patterns = ["abc"]
        text = "abc"
        ac = AhoCorasick(patterns)
        result = ac.search(text)
        expected = [(0, "abc")]
        assert result == expected

    def test_prefix_patterns(self):
        patterns = ["a", "ab", "abc", "abcd"]
        text = "abcde"
        ac = AhoCorasick(patterns)
        result = ac.search(text)
        result.sort(key=lambda x: (x[0], len(x[1])))
        expected = [(0, "a"), (0, "ab"), (0, "abc"), (0, "abcd")]
        assert result == expected

    def test_suffix_patterns(self):
        patterns = ["d", "cd", "bcd", "abcd"]
        text = "abcde"
        ac = AhoCorasick(patterns)
        result = ac.search(text)
        result.sort(key=lambda x: (x[0], len(x[1])))
        expected = [(0, "abcd"), (1, "bcd"), (2, "cd"), (3, "d")]
        assert result == expected

    def test_multiple_occurrences(self):
        patterns = ["ab", "bc"]
        text = "abcabcabc"
        ac = AhoCorasick(patterns)
        result = ac.search(text)
        result.sort(key=lambda x: (x[0], len(x[1])))
        expected = [(0, "ab"), (1, "bc"), (3, "ab"), (4, "bc"), (6, "ab"), (7, "bc")]
        assert result == expected

    def test_case_sensitivity(self):
        patterns = ["a", "A"]
        text = "aAbB"
        ac = AhoCorasick(patterns)
        result = ac.search(text)
        result.sort(key=lambda x: (x[0], x[1]))
        expected = [(0, "a"), (1, "A")]
        assert result == expected

    def test_only_output_links(self):
        patterns = ["abc", "bc", "c"]
        text = "abc"
        ac = AhoCorasick(patterns)
        result = ac.search(text)
        result.sort(key=lambda x: (x[0], len(x[1])))
        expected = [(0, "abc"), (1, "bc"), (2, "c")]
        assert result == expected

    def test_long_text(self):
        patterns = ["abc", "def"]
        text = "x" * 1000 + "abc" + "y" * 1000 + "def" + "z" * 1000
        ac = AhoCorasick(patterns)
        result = ac.search(text)
        result.sort(key=lambda x: x[0])
        expected = [(1000, "abc"), (2003, "def")]
        assert result == expected

    def test_repeated_patterns(self):
        patterns = ["abc", "abc"]
        text = "abcabc"
        ac = AhoCorasick(patterns)
        result = ac.search(text)
        unique_results = list(set(result))
        unique_results.sort()
        expected = [(0, "abc"), (3, "abc")]
        assert unique_results == expected

    def test_failure_function(self):
        patterns = ["abcaby", "aby"]
        text = "abcaby"
        ac = AhoCorasick(patterns)
        result = ac.search(text)
        expected = [(0, 'abcaby'), (3, 'aby')]
        assert result == expected
