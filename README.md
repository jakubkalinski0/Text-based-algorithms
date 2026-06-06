# Text-based Algorithms

Zbiór implementacji algorytmów i ćwiczeń z przetwarzania tekstu — od podstawowej analizy stringów, przez wyrażenia regularne i wyszukiwanie wzorców, po drzewa sufiksów i odległość edycyjną.

## Struktura projektu

```
├── Lab1/   # Wprowadzenie — analiza tekstu, palindromy, anagramy
├── Lab2/   # Wyrażenia regularne, DFA, parsowanie dokumentów
├── Lab3/   # Wyszukiwanie wzorca w tekście
├── Lab4/   # Zaawansowane wyszukiwanie i dopasowanie przybliżone
├── Lab5/   # Drzewa sufiksów (algorytm Ukkonena)
├── Lab6/   # Odległość edycyjna
└── requirements.txt
```

## Wymagania

- Python 3.10+
- [pytest](https://pytest.org/) (do uruchamiania testów)

## Instalacja

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Uruchamianie testów

Z katalogu głównego repozytorium:

```bash
# wszystkie testy (Lab2–Lab6)
python -m pytest Lab2/tests Lab3/tests Lab4/tests Lab6/tests

# pojedyncze laboratorium
python -m pytest Lab3/tests -v
```

Lab1 i Lab5 nie mają dedykowanych testów automatycznych — Lab5 zawiera skrypty porównawcze (`compare.py`, `suffix.py`).

## Laboratoria

### Lab1 — Wprowadzenie do przetwarzania tekstu

| Plik | Opis |
|------|------|
| `Task1_Word_and_character_counter.py` | Liczenie słów, znaków, samogłosek i spółgłosek |
| `Task2_Palindromes.py` | Sprawdzanie palindromów i budowanie najkrótszego palindromu |
| `Task3_Character_frequency_analysis_and_anagram_checking.py` | Częstość znaków i sprawdzanie anagramów |

### Lab2 — Wyrażenia regularne

| Plik | Opis |
|------|------|
| `parse_publication.py` | Parsowanie referencji bibliograficznych |
| `extract_links.py` | Ekstrakcja linków z kodu HTML |
| `analyze_text_file.py` | Analiza pliku tekstowego (słowa, zdania, e-maile, daty) |
| `build_dfa.py` | Budowa i symulacja automatu skończonego z wyrażeń regularnych |

Szczegółowy opis zadań: [`Lab2/README.md`](Lab2/README.md).

### Lab3 — Wyszukiwanie wzorca

| Algorytm | Plik |
|----------|------|
| Naiwny | `naive_pattern_matching.py` |
| Knuth-Morris-Pratt (KMP) | `kmp_algorithm.py` |
| Boyer-Moore | `boyer_moore_algorithm.py` |
| Rabin-Karp | `rabin_karp_algorithm.py` |
| Z-algorithm | `z_algorithm.py` |

### Lab4 — Zaawansowane wyszukiwanie

| Plik | Opis |
|------|------|
| `shift_or_algorithm.py` | Algorytm Shift-Or (dopasowanie bitowe) |
| `aho_corasick_algorithm.py` | Wyszukiwanie wielu wzorców jednocześnie |
| `levenshtein_distance.py` | Odległość Levenshteina |
| `fuzzy_matching.py` | Dopasowanie rozmyte (Hamming, fuzzy Shift-Or) |
| `two_dimensional_search.py` | Wyszukiwanie wzorca w macierzy 2D |

### Lab5 — Drzewa sufiksów

| Plik | Opis |
|------|------|
| `ukkonen.py` | Budowa drzewa sufiksów algorytmem Ukkonena |
| `suffix.py` | Drzewo sufiksów z pomiarami wydajności |
| `substring.py` | Wyszukiwanie podciągów i LCS na drzewie sufiksów |
| `compare.py` | Porównanie algorytmów wyszukiwania wzorca |

### Lab6 — Odległość edycyjna

| Plik | Opis |
|------|------|
| `naive_edit_distance.py` | Naiwne obliczanie odległości edycyjnej |
| `wagner_fischer.py` | Algorytm Wagnera-Fischera (programowanie dynamiczne) |
| `allison.py` | Algorytm Allisonsa |
| `nilsims.py` | Algorytm Nilsimsa |

## Licencja

Projekt objęty licencją określoną w pliku [LICENSE](LICENSE).
