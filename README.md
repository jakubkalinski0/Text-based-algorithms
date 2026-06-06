# Text-based Algorithms

A collection of text processing algorithms and exercises, from basic string analysis and regular expressions to pattern matching, suffix trees, and edit distance.

## Project structure

```
├── Lab1/   # Introduction: text analysis, palindromes, anagrams
├── Lab2/   # Regular expressions, DFA, document parsing
├── Lab3/   # Pattern matching in text
├── Lab4/   # Advanced search and approximate matching
├── Lab5/   # Suffix trees (Ukkonen's algorithm)
├── Lab6/   # Edit distance
└── requirements.txt
```

## Requirements

- Python 3.10+
- [pytest](https://pytest.org/) (for running tests)

## Installation

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Running tests

From the repository root:

```bash
# all tests (Lab2 to Lab6)
python -m pytest Lab2/tests Lab3/tests Lab4/tests Lab6/tests

# single lab
python -m pytest Lab3/tests -v
```

Lab1 and Lab5 do not have dedicated automated tests. Lab5 includes comparison scripts (`compare.py`, `suffix.py`).

## Labs

### Lab1: Introduction to text processing

| File | Description |
|------|-------------|
| `Task1_Word_and_character_counter.py` | Word, character, vowel, and consonant counting |
| `Task2_Palindromes.py` | Palindrome checking and shortest palindrome construction |
| `Task3_Character_frequency_analysis_and_anagram_checking.py` | Character frequency and anagram checking |

### Lab2: Regular expressions

| File | Description |
|------|-------------|
| `parse_publication.py` | Bibliographic reference parsing |
| `extract_links.py` | Link extraction from HTML |
| `analyze_text_file.py` | Text file analysis (words, sentences, emails, dates) |
| `build_dfa.py` | DFA construction and simulation from regular expressions |

Detailed task descriptions: [`Lab2/README.md`](Lab2/README.md).

### Lab3: Pattern matching

| Algorithm | File |
|-----------|------|
| Naive | `naive_pattern_matching.py` |
| Knuth-Morris-Pratt (KMP) | `kmp_algorithm.py` |
| Boyer-Moore | `boyer_moore_algorithm.py` |
| Rabin-Karp | `rabin_karp_algorithm.py` |
| Z-algorithm | `z_algorithm.py` |

### Lab4: Advanced search

| File | Description |
|------|-------------|
| `shift_or_algorithm.py` | Shift-Or algorithm (bit-parallel matching) |
| `aho_corasick_algorithm.py` | Multi-pattern search |
| `levenshtein_distance.py` | Levenshtein distance |
| `fuzzy_matching.py` | Fuzzy matching (Hamming, fuzzy Shift-Or) |
| `two_dimensional_search.py` | 2D pattern search in a matrix |

### Lab5: Suffix trees

| File | Description |
|------|-------------|
| `ukkonen.py` | Suffix tree construction with Ukkonen's algorithm |
| `suffix.py` | Suffix tree with performance benchmarks |
| `substring.py` | Substring search and LCS on a suffix tree |
| `compare.py` | Pattern matching algorithm comparison |

### Lab6: Edit distance

| File | Description |
|------|-------------|
| `naive_edit_distance.py` | Naive edit distance computation |
| `wagner_fischer.py` | Wagner-Fischer algorithm (dynamic programming) |
| `allison.py` | Allison's algorithm |
| `nilsims.py` | Nilsims algorithm |

## License

This project is licensed under the terms specified in [LICENSE](LICENSE).
