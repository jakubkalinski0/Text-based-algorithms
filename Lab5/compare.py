import sys
import time
import random
import string
import gc
import matplotlib.pyplot as plt
from collections import defaultdict  # Dla Aho-Corasick

# Globalny licznik porównań znaków (resetowany przed każdym algorytmem)
CHAR_COMPARISONS = 0


def reset_char_comparisons():
    global CHAR_COMPARISONS
    CHAR_COMPARISONS = 0


def increment_char_comparisons(count=1):
    global CHAR_COMPARISONS
    CHAR_COMPARISONS += count


# --- Naiwny Algorytm ---
def naive_search(text, pattern):
    reset_char_comparisons()
    n = len(text)
    m = len(pattern)
    occurrences = []
    if m == 0: return occurrences
    if m > n: return occurrences

    for i in range(n - m + 1):
        match = True
        for j in range(m):
            increment_char_comparisons()
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            occurrences.append(i)
    return occurrences


# --- Algorytm KMP (Knuth-Morris-Pratt) ---
def kmp_compute_lps_array(pattern):  # LPS: Longest Proper Prefix which is also Suffix
    m = len(pattern)
    lps = [0] * m
    length = 0  # Długość poprzedniego najdłuższego prefiksu-sufiksu
    i = 1
    while i < m:
        increment_char_comparisons()  # Porównanie wewnątrz logiki LPS
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern):
    reset_char_comparisons()
    n = len(text)
    m = len(pattern)
    occurrences = []
    if m == 0: return occurrences
    if m > n: return occurrences

    lps = kmp_compute_lps_array(pattern)

    i = 0  # Indeks dla text[]
    j = 0  # Indeks dla pattern[]
    while i < n:
        increment_char_comparisons()
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            occurrences.append(i - j)
            j = lps[j - 1]  # Przesuń pattern zgodnie z LPS
        elif i < n and pattern[j] != text[i]:  # Niedopasowanie po j dopasowaniach
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1  # Przesuń pattern o jeden w tekście
    return occurrences


# --- Algorytm Boyer-Moore ---
# Prosta wersja z regułą złego znaku (Bad Character Rule)
# i uproszczoną regułą dobrego sufiksu (Good Suffix Rule - pominięta dla prostoty,
# ale pełny BM ją zawiera i jest bardziej efektywny)
NO_OF_CHARS = 256  # Rozszerzone ASCII


def bm_bad_char_heuristic(pattern, m):
    bad_char = [-1] * NO_OF_CHARS
    for i in range(m):
        bad_char[ord(pattern[i])] = i
    return bad_char


def boyer_moore_search(text, pattern):
    reset_char_comparisons()
    n = len(text)
    m = len(pattern)
    occurrences = []
    if m == 0: return occurrences
    if m > n: return occurrences

    bad_char = bm_bad_char_heuristic(pattern, m)

    s = 0  # Przesunięcie wzorca względem tekstu
    while s <= (n - m):
        j = m - 1  # Zaczynamy porównywać od końca wzorca

        while j >= 0:
            increment_char_comparisons()
            if pattern[j] != text[s + j]:
                break
            j -= 1

        if j < 0:  # Wzorzec znaleziony
            occurrences.append(s)
            # Przesuń wzorzec tak, aby następny znak w tekście
            # pasował do ostatniego wystąpienia tego znaku we wzorcu.
            # Jeśli wzorzec całkowicie się przesunął, lub jeśli s+m < n,
            # to przesuwamy o bad_char[text[s+m]], w przeciwnym razie o 1.
            s += (m - bad_char[ord(text[s + m])] if s + m < n else 1)
        else:  # Niedopasowanie
            # Przesuń wzorzec tak, aby zły znak w tekście
            # (text[s+j]) pasował do ostatniego wystąpienia tego znaku
            # we wzorcu. Maksymalne przesunięcie to j - bad_char[ord(text[s+j])].
            # Musimy też zapewnić przesunięcie o co najmniej 1.
            shift = j - bad_char[ord(text[s + j])]
            s += max(1, shift)

    return occurrences


# --- Algorytm Rabin-Karp ---
# q: duża liczba pierwsza
# d: rozmiar alfabetu (np. 256 dla ASCII)
def rabin_karp_search(text, pattern, q=101):
    reset_char_comparisons()
    n = len(text)
    m = len(pattern)
    d = 256
    occurrences = []
    if m == 0: return occurrences
    if m > n: return occurrences

    p_hash = 0  # Wartość hasha dla wzorca
    t_hash = 0  # Wartość hasha dla bieżącego okna tekstu
    h = 1  # d^(m-1) % q

    # Oblicz h = d^(m-1) % q
    for _ in range(m - 1):
        h = (h * d) % q

    # Oblicz początkowe hashe dla wzorca i pierwszego okna tekstu
    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    # Przesuwaj wzorzec po tekście
    for i in range(n - m + 1):
        # Sprawdź hashe. Jeśli równe, sprawdź znaki (uniknięcie kolizji)
        if p_hash == t_hash:
            match = True
            for j in range(m):
                increment_char_comparisons()  # Porównanie tylko przy dopasowaniu hasha
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                occurrences.append(i)

        # Oblicz hash dla następnego okna tekstu (rolling hash)
        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            # Możemy dostać ujemny t_hash, dodaj q, aby był dodatni
            if t_hash < 0:
                t_hash = t_hash + q
    return occurrences


# --- Algorytm Aho-Corasick (dla wielu wzorców) ---
# Dla porównania, dostosujemy go do wyszukiwania jednego wzorca,
# ale jego siła leży w wielu wzorcach.
class ACNode:
    def __init__(self):
        self.children = {}
        self.failure_link = None  # Łącze niepowodzenia
        self.output = []  # Wzorce kończące się w tym węźle


class AhoCorasick:
    def __init__(self, patterns):  # patterns to lista stringów
        self.root = ACNode()
        self.patterns = patterns
        self._build_trie()
        self._build_failure_links()

    def _build_trie(self):
        for idx, pattern in enumerate(self.patterns):
            node = self.root
            for char in pattern:
                node = node.children.setdefault(char, ACNode())
            node.output.append(idx)  # Zapisz indeks wzorca

    def _build_failure_links(self):
        queue = []
        # Dla dzieci korzenia, łącza niepowodzenia wskazują na korzeń
        for node in self.root.children.values():
            node.failure_link = self.root
            queue.append(node)

        while queue:
            current_node = queue.pop(0)
            for char, next_node in current_node.children.items():
                queue.append(next_node)
                # Znajdź łącze niepowodzenia dla next_node
                # Idź w górę przez łącza niepowodzenia current_node
                f_link = current_node.failure_link
                while f_link is not None and char not in f_link.children:
                    f_link = f_link.failure_link

                if f_link is None:  # Nie znaleziono odpowiedniego przejścia
                    next_node.failure_link = self.root
                else:
                    next_node.failure_link = f_link.children[char]

                # Dodaj output z łącza niepowodzenia do bieżącego węzła
                # (wszystkie wzorce kończące się na ścieżce failure_link.output
                # są też sufiksami wzorca kończącego się w next_node)
                next_node.output.extend(next_node.failure_link.output)

    def search_in(self, text):
        reset_char_comparisons()  # Reset dla Aho-Corasick
        results = defaultdict(list)  # Słownik: pattern_idx -> [lista pozycji]
        current_node = self.root

        for i, char in enumerate(text):
            # Przejdź przez łącza niepowodzenia, aż znajdziesz przejście dla 'char' lub dojdziesz do korzenia
            # Każde przejście w automacie jest "porównaniem" (logicznie)
            # W tej implementacji, nie ma jawnych porównań znaków w pętli wyszukiwania,
            # ale operacje na słownikach i podążanie za linkami są istotą.
            # Dla spójności, możemy dodać increment_char_comparisons() w pętli while.

            original_node_before_failure_traversal = current_node
            while current_node is not None and char not in current_node.children:
                # To jest odpowiednik "porównania", które nie pasuje
                increment_char_comparisons()
                current_node = current_node.failure_link

            if current_node is None:  # Doszliśmy do końca łączy niepowodzeń
                current_node = self.root
                # Możemy tu też zliczyć porównanie, jeśli `char` nie pasuje nawet z korzenia
                if char not in current_node.children:
                    increment_char_comparisons()
            else:
                # Znak pasuje do krawędzi z `current_node` (jeśli `original_node_before_failure_traversal` go nie miał)
                # lub z `f_link` (jeśli `current_node` jest wynikiem podążania za `failure_link`)
                if char in current_node.children:  # Sprawdzenie, czy po przejściach failure linkiem mamy char
                    increment_char_comparisons()  # To "udane" porównanie
                    current_node = current_node.children[char]
                else:
                    # Jeśli nawet po przejściach failure linkami, char nie jest dzieckiem korzenia,
                    # to też jest "porównanie"
                    increment_char_comparisons()
                    current_node = self.root  # Wróć do korzenia, jeśli char nie pasuje nawet z niego

            # Jeśli w current_node kończą się jakieś wzorce
            if current_node.output:
                for pattern_idx in current_node.output:
                    pattern_len = len(self.patterns[pattern_idx])
                    results[pattern_idx].append(i - pattern_len + 1)
        return results


def aho_corasick_search_single_pattern(text, pattern):
    # Dla pojedynczego wzorca, opakowujemy AhoCorasick
    if not pattern: return []
    ac = AhoCorasick([pattern])  # Tworzymy automat dla jednego wzorca
    all_occurrences_dict = ac.search_in(text)
    return all_occurrences_dict.get(0, [])  # Pobierz wystąpienia dla wzorca o indeksie 0


# --- Drzewo Sufiksów (adaptacja z poprzedniego zadania) ---
# Załóżmy, że klasy Node i SuffixTree są zdefiniowane jak poprzednio
# (z _build_tree_internal, _finalize_tree_edges, get_num_nodes)
# Musimy dodać metodę find_pattern do SuffixTree, która zlicza porównania.

class STNode:  # Uproszczona Node dla SuffixTree, jeśli trzeba
    _node_count_global = 0

    def __init__(self, start=-1, end=-1, suffix_id=-1):
        self.children = {}
        self.suffix_link = None
        self.start = start
        self.end = end
        self.id = suffix_id
        STNode._node_count_global += 1
        self.node_creation_id = STNode._node_count_global

    def edge_length(self, current_global_end_or_final_n_minus_1, open_edge_marker):
        _end = current_global_end_or_final_n_minus_1 if self.end == open_edge_marker else self.end
        return _end - self.start + 1

    def is_leaf(self): return not self.children


class SuffixTreeUKK:  # Zmieniona nazwa, aby uniknąć konfliktu z poprzednią
    OPEN_EDGE_END = object()

    def __init__(self, text: str, add_terminator=True):
        if add_terminator and (not text or text[-1] != "$"):
            self.text = text + "$"
        else:
            self.text = text
        self.N = len(self.text)
        STNode._node_count_global = 0
        self.root = STNode()
        self.root.suffix_link = self.root
        self.num_nodes = 1
        self.active_node = self.root
        self.active_edge_start_of_suffix = 0
        self.active_length = 0
        self.remainder = 0
        self.global_end = -1
        self._build_tree_internal()
        self._finalize_tree_edges()

    def _create_node(self, start=-1, end=-1, suffix_id=-1):
        self.num_nodes += 1
        return STNode(start, end, suffix_id)

    # ... (skopiuj _build_tree_internal, _walk_down, _edge_char..., _char_on_edge...)
    # ... (skopiuj _finalize_tree_edges, _finalize_tree_edges_recursive)
    # --- Skopiowane metody SuffixTreeUKK (muszą być w klasie) ---
    def _edge_char_from_active_point(self):
        return self.text[self.active_edge_start_of_suffix]

    def _char_on_edge_at_active_length(self, node_on_edge):
        return self.text[node_on_edge.start + self.active_length]

    def _walk_down(self, next_node_on_edge):
        edge_len = next_node_on_edge.edge_length(self.global_end, SuffixTreeUKK.OPEN_EDGE_END)
        if self.active_length >= edge_len:
            self.active_node = next_node_on_edge
            self.active_length -= edge_len
            self.active_edge_start_of_suffix += edge_len
            return True
        return False

    def _build_tree_internal(self):
        for i in range(self.N):
            self.global_end = i
            self.remainder += 1
            last_new_internal_node = None
            while self.remainder > 0:
                if self.active_length == 0: self.active_edge_start_of_suffix = i - (self.remainder - 1)
                char_key_for_edge = self._edge_char_from_active_point()
                if char_key_for_edge not in self.active_node.children:
                    current_suffix_actual_start_idx = i - (self.remainder - 1)
                    new_leaf = self._create_node(start=i, end=SuffixTreeUKK.OPEN_EDGE_END,
                                                 suffix_id=current_suffix_actual_start_idx)
                    self.active_node.children[char_key_for_edge] = new_leaf
                    if last_new_internal_node is not None:
                        last_new_internal_node.suffix_link = self.active_node
                        last_new_internal_node = None
                else:
                    next_node = self.active_node.children[char_key_for_edge]
                    if self._walk_down(next_node): continue
                    char_on_edge = self._char_on_edge_at_active_length(next_node)
                    if char_on_edge == self.text[i]:
                        self.active_length += 1
                        if last_new_internal_node is not None and self.active_node != self.root:
                            last_new_internal_node.suffix_link = self.active_node
                        break
                    else:
                        split_node_end_idx = next_node.start + self.active_length - 1
                        split_node = self._create_node(start=next_node.start, end=split_node_end_idx)
                        self.active_node.children[char_key_for_edge] = split_node
                        current_suffix_actual_start_idx = i - (self.remainder - 1)
                        new_leaf = self._create_node(start=i, end=SuffixTreeUKK.OPEN_EDGE_END,
                                                     suffix_id=current_suffix_actual_start_idx)
                        split_node.children[self.text[i]] = new_leaf
                        next_node.start = next_node.start + self.active_length
                        split_node.children[self.text[next_node.start]] = next_node
                        if last_new_internal_node is not None: last_new_internal_node.suffix_link = split_node
                        last_new_internal_node = split_node
                self.remainder -= 1
                if self.active_node == self.root and self.active_length > 0:
                    self.active_length -= 1
                    if self.active_length > 0: self.active_edge_start_of_suffix = (i - (
                                self.remainder - 1)) - self.active_length
                elif self.active_node != self.root:
                    self.active_node = self.active_node.suffix_link

    def _finalize_tree_edges_recursive(self, node, final_val):
        if node.start != -1 and node.end == SuffixTreeUKK.OPEN_EDGE_END: node.end = final_val
        for child_node in node.children.values(): self._finalize_tree_edges_recursive(child_node, final_val)

    def _finalize_tree_edges(self):
        self._finalize_tree_edges_recursive(self.root, self.N - 1)

    def get_num_nodes(self):
        return self.num_nodes

    # --- Koniec skopiowanych metod ---

    def _collect_leaf_ids_dfs(self, node: STNode, results: list[int]):
        if node.is_leaf():
            if node.id != -1: results.append(node.id)
        for child_node in node.children.values():
            self._collect_leaf_ids_dfs(child_node, results)

    def find_pattern(self, pattern: str) -> list[int]:
        # reset_char_comparisons() # Reset jest robiony na zewnątrz przed wywołaniem tej funkcji
        if not pattern: return []
        current_node = self.root
        pattern_idx = 0

        while pattern_idx < len(pattern):
            char_to_match = pattern[pattern_idx]

            # To jest "porównanie" logiczne - czy istnieje krawędź
            # W implementacjach słownikowych, nie ma tu jawnego porównania znaków
            # Ale dla spójności, możemy to zliczyć jako jedno logiczne "przejście"
            # increment_char_comparisons() # Za wyszukiwanie klucza w słowniku

            if char_to_match not in current_node.children:
                # Jeśli nie ma krawędzi, to znaczy, że "porównaliśmy" i nie pasuje
                increment_char_comparisons()
                return []

            edge_node = current_node.children[char_to_match]
            edge_len = edge_node.edge_length(self.N - 1, SuffixTreeUKK.OPEN_EDGE_END)

            for i in range(edge_len):
                if pattern_idx >= len(pattern): break

                text_char_on_edge = self.text[edge_node.start + i]
                pattern_char = pattern[pattern_idx]

                increment_char_comparisons()  # Jawne porównanie znaków
                if text_char_on_edge != pattern_char:
                    return []

                pattern_idx += 1

            if pattern_idx == len(pattern):
                occurrences = []
                self._collect_leaf_ids_dfs(edge_node, occurrences)
                return sorted(list(set(occurrences)))
            current_node = edge_node
        return []


def suffix_tree_search(text, pattern):
    reset_char_comparisons()
    if not pattern: return []
    st = SuffixTreeUKK(text, add_terminator=True)  # Budowa drzewa
    # Czas budowy jest częścią "preprocessingu", ale w tym porównaniu
    # zwykle wlicza się go w całkowity czas, jeśli drzewo nie jest reużywane.
    # Dla tego testu, załóżmy, że budujemy za każdym razem.

    # Pomiar porównań jest resetowany przed `st.find_pattern` jeśli jest robiony na zewnątrz
    # Tutaj jest resetowany na początku funkcji, więc `find_pattern` nie musi go resetować.
    return st.find_pattern(pattern)


# --- Wyszukiwanie oparte na Tablicy Sufiksów ---
# Załóżmy, że construct_suffix_array_and_lcp jest zdefiniowane jak poprzednio.
# Ta funkcja SA była prosta O(N^2 log N). Dla porównania z innymi, to będzie wolne.
# W praktyce używa się SA-IS (O(N)).

def suffix_array_bsearch(text_with_terminator, sa, pattern):
    # reset_char_comparisons() # Reset jest na zewnątrz
    n_sa = len(sa)  # Długość tablicy sufiksów (równe długości tekstu z terminatorem)
    m = len(pattern)
    if m == 0: return []

    # Wyszukiwanie binarne dla pierwszego wystąpienia (lub miejsca wstawienia)
    low = 0
    high = n_sa - 1
    first_occurrence_sa_idx = -1

    while low <= high:
        mid = (low + high) // 2
        suffix_start = sa[mid]

        # Porównaj pattern z text_with_terminator[suffix_start : suffix_start + m]
        # Zliczaj porównania znaków
        comparison_result = 0  # -1 jeśli pattern < sufiks, 0 jeśli równe, 1 jeśli pattern > sufiks
        # Maksymalna długość do porównania to min(m, n_text - suffix_start)
        len_to_compare = min(m, len(text_with_terminator) - suffix_start)

        for k in range(len_to_compare):
            increment_char_comparisons()
            if pattern[k] < text_with_terminator[suffix_start + k]:
                comparison_result = -1
                break
            elif pattern[k] > text_with_terminator[suffix_start + k]:
                comparison_result = 1
                break

        if comparison_result == 0:  # Prefiksy pasują
            if len_to_compare < m:  # Sufiks jest krótszy niż wzorzec, np. text="a", pattern="aa"
                comparison_result = 1  # Wzorzec jest "większy"
            # else: comparison_result = 0, znaleziono dopasowanie

        if comparison_result == 0:  # Znaleziono dopasowanie, szukaj dalej w lewo
            first_occurrence_sa_idx = mid
            high = mid - 1
        elif comparison_result < 0:  # pattern < sufiks
            high = mid - 1
        else:  # pattern > sufiks
            low = mid + 1

    if first_occurrence_sa_idx == -1:
        return []  # Nie znaleziono wzorca

    # Znajdź zakres wystąpień
    # first_occurrence_sa_idx to indeks w SA pierwszego sufiksu zaczynającego się od wzorca.
    # Szukaj w prawo od first_occurrence_sa_idx, aż sufiksy przestaną zaczynać się od wzorca.
    occurrences = [sa[first_occurrence_sa_idx]]

    for i in range(first_occurrence_sa_idx + 1, n_sa):
        suffix_start = sa[i]
        if len(text_with_terminator) - suffix_start < m:  # Sufiks za krótki
            break

        match = True
        for k in range(m):
            increment_char_comparisons()  # Porównania dla potwierdzenia
            if pattern[k] != text_with_terminator[suffix_start + k]:
                match = False
                break
        if match:
            occurrences.append(sa[i])
        else:
            break  # Koniec zakresu pasujących sufiksów

    return sorted(list(set(occurrences)))


def suffix_array_search(text, pattern):
    reset_char_comparisons()
    if not pattern: return []

    # Budowa SA i LCP (LCP nie jest tu używane, ale jest częścią konstrukcji)
    sa_list, _, text_internal = construct_suffix_array_and_lcp(text, add_terminator=True)

    return suffix_array_bsearch(text_internal, sa_list, pattern)


# --- Pomiar Pamięci (uproszczony) ---
# Będziemy używać sys.getsizeof na głównych strukturach. To jest płytkie.
# Dla drzewa sufiksów i Aho-Corasick, rzeczywiste zużycie będzie większe.

def get_memory_usage_approx(obj):
    # Proste przybliżenie, sumując rozmiary niektórych komponentów
    if obj is None: return 0

    size = sys.getsizeof(obj)
    if isinstance(obj, (SuffixTreeUKK, AhoCorasick)):
        size += sys.getsizeof(obj.root)  # i potencjalnie inne duże atrybuty
        if hasattr(obj, 'text'): size += sys.getsizeof(obj.text)
        if hasattr(obj, 'patterns'): size += sys.getsizeof(obj.patterns)
        # To nadal jest bardzo niedokładne dla struktur drzewiastych.
    elif isinstance(obj, list):
        for item in obj: size += sys.getsizeof(item)  # Dla list intów np.
    return size


# --- Funkcja Porównawcza ---
def compare_pattern_matching_algorithms(text: str, pattern: str, patterns_for_ac: list[str] = None) -> dict:
    # patterns_for_ac to lista wzorców dla Aho-Corasick, jeśli chcemy testować jego siłę.
    # Jeśli None, użyjemy pojedynczego `pattern`.
    if patterns_for_ac is None:
        patterns_for_ac = [pattern] if pattern else []

    all_results = {}
    algorithms = {
        "Naive": naive_search,
        "KMP": kmp_search,
        "Boyer-Moore": boyer_moore_search,
        "Rabin-Karp": rabin_karp_search,
        "SuffixTree": suffix_tree_search,
        "SuffixArray": suffix_array_search,
        # Aho-Corasick jest specjalny, bo dla wielu wzorców
    }
    if pattern:  # Jeśli jest pojedynczy wzorzec do testowania
        algorithms["Aho-Corasick (single)"] = lambda t, p: aho_corasick_search_single_pattern(t, p)

    for name, func in algorithms.items():
        gc.collect()  # Spróbuj oczyścić pamięć
        # mem_before = get_memory_usage_approx(None) # Trudne do dokładnego zmierzenia przyrostu

        # Dla ST i SA, preprocesing (budowa struktury) jest częścią algorytmu
        # Jeśli struktura jest budowana tylko raz i używana wielokrotnie, analiza się zmienia.
        # Tutaj zakładamy budowę za każdym razem dla porównania.

        reset_char_comparisons()  # Ważne przed każdym algorytmem
        time_start = time.perf_counter()

        # Specjalna obsługa dla AhoCorasick, jeśli testujemy wiele wzorców
        # W tej funkcji `compare_pattern_matching_algorithms` skupiamy się na pojedynczym `pattern`
        # więc Aho-Corasick (single) jest używane.
        # Jeśli chcemy testować AhoCorasick z `patterns_for_ac`, to trzeba to zrobić oddzielnie.

        # Pomiar pamięci struktur pomocniczych - KMP (lps), BM (bad_char)
        # To jest skomplikowane, bo trzeba by to mierzyć wewnątrz funkcji.
        # Na razie skupimy się na czasie i porównaniach.
        # Pamięć dla ST i SA będzie uwzględniać całe struktury.

        try:
            positions = func(text, pattern)
        except Exception as e:
            print(f"Błąd w algorytmie {name}: {e}")
            positions = f"Error: {e}"

        time_end = time.perf_counter()

        # Zużycie pamięci - bardzo uproszczone.
        # Dla SA/ST, pamięć to głównie sama struktura.
        # Dla innych, to tekst + wzorzec + małe tablice pomocnicze.
        # To wymagałoby bardziej zaawansowanego profilowania pamięci.
        # Na razie ustawimy placeholder.
        memory_kb = 0
        if name == "SuffixTree":
            # Przybliżony rozmiar drzewa (bardzo niedokładne z sys.getsizeof)
            # st_temp = SuffixTreeUKK(text, add_terminator=True)
            # memory_kb = get_memory_usage_approx(st_temp) / 1024
            # del st_temp
            pass  # Zostawmy na razie, bo dokładny pomiar jest trudny
        elif name == "SuffixArray":
            # sa_list, lcp_list, text_int = construct_suffix_array_and_lcp(text, add_terminator=True)
            # memory_kb = (sys.getsizeof(sa_list) + sys.getsizeof(lcp_list) + sys.getsizeof(text_int)) / 1024
            # for x in sa_list: memory_kb += sys.getsizeof(x)/1024
            # for x in lcp_list: memory_kb += sys.getsizeof(x)/1024
            # del sa_list, lcp_list, text_int
            pass

        all_results[name] = {
            "time_ms": (time_end - time_start) * 1000,
            "memory_kb": memory_kb,  # Placeholder
            "comparisons": CHAR_COMPARISONS,
            "positions": positions
        }

    # Oddzielna obsługa Aho-Corasick dla wielu wzorców (jeśli chcemy to włączyć w ten raport)
    if patterns_for_ac and (len(patterns_for_ac) > 1 or (len(patterns_for_ac) == 1 and not pattern)):
        gc.collect()
        reset_char_comparisons()
        ac_multi = AhoCorasick(patterns_for_ac)  # Budowa automatu

        time_start_ac_multi = time.perf_counter()
        positions_ac_multi_dict = ac_multi.search_in(text)  # Wyszukiwanie
        time_end_ac_multi = time.perf_counter()

        # memory_ac_multi = get_memory_usage_approx(ac_multi) / 1024 # Placeholder

        all_results["Aho-Corasick (multiple)"] = {
            "time_ms": (time_end_ac_multi - time_start_ac_multi) * 1000,  # Tylko czas wyszukiwania
            "time_ms_preprocess": (time_start_ac_multi - time.perf_counter()) * 1000,
            # Czas budowy, ale perf_counter tu nie zadziała dobrze
            # Musiałby być mierzony oddzielnie przed search_in
            "memory_kb": 0,  # Placeholder
            "comparisons": CHAR_COMPARISONS,
            "positions_dict": positions_ac_multi_dict  # Słownik {pattern_idx: [pos]}
        }
        # Można dodać czas preprocesingu AC jako osobny wpis.
        # time_ac_build_start = time.perf_counter()
        # ac_multi = AhoCorasick(patterns_for_ac)
        # time_ac_build_end = time.perf_counter()
        # all_results["Aho-Corasick (multiple)"]["preprocess_time_ms"] = (time_ac_build_end - time_ac_build_start) * 1000

    return all_results


# --- Generowanie Danych Testowych i Wykresów ---
def generate_random_string(length, alphabet=string.ascii_lowercase):
    return ''.join(random.choice(alphabet) for _ in range(length))


def run_pattern_matching_experiments():
    text_sizes = [1000, 5000, 10000, 20000, 50000]  # , 100000]
    pattern_lengths_fixed_text = [10, 50, 100, 200, 500]
    fixed_text_size_for_pattern_len_test = 20000  # Użyj tego rozmiaru tekstu do testowania wpływu długości wzorca

    # Wyniki dla wykresów
    # Klucze: 'text_size', 'pattern_len', 'algorithm_name', 'time_ms', 'comparisons', 'memory_kb'
    plot_data = []

    # 1. Testy: Czas/Porównania/Pamięć w zależności od rozmiaru tekstu (stała długość wzorca)
    fixed_pattern_len = 50
    print(f"\n--- Testy: Wpływ rozmiaru tekstu (długość wzorca = {fixed_pattern_len}) ---")
    for ts in text_sizes:
        text = generate_random_string(ts)
        # Wzorzec, który prawdopodobnie występuje kilka razy
        pat_start_idx = random.randint(0, ts - fixed_pattern_len - 1) if ts > fixed_pattern_len else 0
        pattern = text[pat_start_idx: pat_start_idx + fixed_pattern_len]
        if not pattern and fixed_pattern_len > 0: pattern = generate_random_string(fixed_pattern_len)  # Fallback
        if not pattern: continue  # Pomiń, jeśli wzorzec jest pusty

        print(f"\nRozmiar tekstu: {ts}, Długość wzorca: {len(pattern)}")
        results = compare_pattern_matching_algorithms(text, pattern)
        for algo_name, res_data in results.items():
            if "Error" in str(res_data.get("positions", "")):
                print(f"  {algo_name}: Błąd")
                continue

            print(f"  {algo_name}: Time={res_data['time_ms']:.2f}ms, Comparisons={res_data['comparisons']}")
            plot_data.append({
                "test_type": "text_size_impact",
                "text_size": ts, "pattern_len": len(pattern), "algorithm_name": algo_name,
                "time_ms": res_data['time_ms'], "comparisons": res_data['comparisons'],
                "memory_kb": res_data['memory_kb']  # Pamiętaj, że pamięć jest placeholderem
            })

    # 2. Testy: Czas w zależności od długości wzorca (stały rozmiar tekstu)
    print(f"\n--- Testy: Wpływ długości wzorca (rozmiar tekstu = {fixed_text_size_for_pattern_len_test}) ---")
    text_for_pattern_test = generate_random_string(fixed_text_size_for_pattern_len_test)
    for pl in pattern_lengths_fixed_text:
        if pl >= fixed_text_size_for_pattern_len_test: continue  # Wzorzec nie może być dłuższy niż tekst
        pat_start_idx = random.randint(0, fixed_text_size_for_pattern_len_test - pl - 1)
        pattern = text_for_pattern_test[pat_start_idx: pat_start_idx + pl]
        if not pattern and pl > 0: pattern = generate_random_string(pl)  # Fallback
        if not pattern: continue

        print(f"\nRozmiar tekstu: {fixed_text_size_for_pattern_len_test}, Długość wzorca: {pl}")
        results = compare_pattern_matching_algorithms(text_for_pattern_test, pattern)
        for algo_name, res_data in results.items():
            if "Error" in str(res_data.get("positions", "")):
                print(f"  {algo_name}: Błąd")
                continue
            print(f"  {algo_name}: Time={res_data['time_ms']:.2f}ms, Comparisons={res_data['comparisons']}")
            plot_data.append({
                "test_type": "pattern_len_impact",
                "text_size": fixed_text_size_for_pattern_len_test, "pattern_len": pl, "algorithm_name": algo_name,
                "time_ms": res_data['time_ms'], "comparisons": res_data['comparisons'],
                "memory_kb": res_data['memory_kb']
            })

    # Generowanie wykresów
    make_plots(plot_data, text_sizes, pattern_lengths_fixed_text, fixed_text_size_for_pattern_len_test)


def make_plots(plot_data_list, text_sizes_axis, pattern_lengths_axis, fixed_text_size_val):
    # Grupuj dane wg algorytmu
    algo_names = sorted(list(set(d['algorithm_name'] for d in plot_data_list)))

    # Wykres 1: Czas vs Rozmiar Tekstu
    plt.figure(figsize=(12, 7))
    for algo in algo_names:
        data_points = [d for d in plot_data_list if
                       d['algorithm_name'] == algo and d['test_type'] == 'text_size_impact']
        if not data_points: continue
        data_points.sort(key=lambda x: x['text_size'])
        plt.plot([d['text_size'] for d in data_points], [d['time_ms'] for d in data_points], marker='o', label=algo)
    plt.xlabel("Rozmiar tekstu (N)")
    plt.ylabel("Czas wykonania (ms)")
    plt.title(
        f"Czas wykonania vs Rozmiar tekstu (Dł. wzorca ≈ {plot_data_list[0]['pattern_len'] if plot_data_list else 'stała'})")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True);
    plt.xscale('log');
    plt.yscale('log')
    plt.tight_layout(rect=[0, 0, 0.85, 1])  # Zostaw miejsce na legendę
    plt.savefig("pm_time_vs_text_size.png");
    plt.show()

    # Wykres 2: Porównania vs Rozmiar Tekstu
    plt.figure(figsize=(12, 7))
    for algo in algo_names:
        data_points = [d for d in plot_data_list if
                       d['algorithm_name'] == algo and d['test_type'] == 'text_size_impact']
        if not data_points: continue
        data_points.sort(key=lambda x: x['text_size'])
        plt.plot([d['text_size'] for d in data_points], [d['comparisons'] for d in data_points], marker='o', label=algo)
    plt.xlabel("Rozmiar tekstu (N)")
    plt.ylabel("Liczba porównań znaków")
    plt.title(
        f"Liczba porównań vs Rozmiar tekstu (Dł. wzorca ≈ {plot_data_list[0]['pattern_len'] if plot_data_list else 'stała'})")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True);
    plt.xscale('log');
    plt.yscale('log')
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.savefig("pm_comparisons_vs_text_size.png");
    plt.show()

    # Wykres 3: Czas vs Długość Wzorca
    plt.figure(figsize=(12, 7))
    for algo in algo_names:
        data_points = [d for d in plot_data_list if
                       d['algorithm_name'] == algo and d['test_type'] == 'pattern_len_impact']
        if not data_points: continue
        data_points.sort(key=lambda x: x['pattern_len'])
        plt.plot([d['pattern_len'] for d in data_points], [d['time_ms'] for d in data_points], marker='o', label=algo)
    plt.xlabel("Długość wzorca (M)")
    plt.ylabel("Czas wykonania (ms)")
    plt.title(f"Czas wykonania vs Długość wzorca (Rozmiar tekstu = {fixed_text_size_val})")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True);
    plt.xscale('log');
    plt.yscale('log')
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.savefig("pm_time_vs_pattern_len.png");
    plt.show()

    # Wykres Pamięci - pominięty z powodu trudności w dokładnym pomiarze w Pythonie
    # bez zewnętrznych bibliotek jak pympler.


if __name__ == '__main__':
    # Skopiuj definicje klas SuffixTreeUKK, STNode, construct_suffix_array_and_lcp
    # z poprzednich odpowiedzi tutaj, jeśli nie są w tym samym pliku.
    print("Uruchamianie eksperymentów porównania algorytmów dopasowywania wzorców...")
    print("To może zająć sporo czasu.")
    run_pattern_matching_experiments()