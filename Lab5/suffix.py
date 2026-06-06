import sys
import time
import random
import string
import gc  # Garbage collector, do dokładniejszego pomiaru pamięci
import matplotlib.pyplot as plt


# --- Implementacja Drzewa Sufiksów (Ukkonen) ---
class Node:
    _node_count_global = 0  # Globalny licznik dla wszystkich instancji Node

    def __init__(self, start=-1, end=-1, suffix_id=-1):
        self.children = {}
        self.suffix_link = None
        self.start = start
        self.end = end
        self.id = suffix_id  # Indeks początkowy sufiksu (dla liści)

        Node._node_count_global += 1
        self.node_creation_id = Node._node_count_global  # Unikalne ID dla każdego węzła

    def edge_length(self, current_global_end_or_final_n_minus_1, open_edge_marker):
        _end = current_global_end_or_final_n_minus_1 if self.end == open_edge_marker else self.end
        return _end - self.start + 1

    def is_leaf(self):
        return not self.children


class SuffixTree:
    OPEN_EDGE_END = object()

    def __init__(self, text: str, add_terminator=True):
        if add_terminator and (not text or text[-1] != "$"):
            self.text = text + "$"
        else:
            self.text = text

        self.N = len(self.text)
        Node._node_count_global = 0  # Resetuj licznik dla nowego drzewa
        self.root = Node()
        self.root.suffix_link = self.root
        self.num_nodes = 1  # Zaczynamy od korzenia

        self.active_node = self.root
        self.active_edge_start_of_suffix = 0
        self.active_length = 0
        self.remainder = 0
        self.global_end = -1

        self._build_tree_internal()
        self._finalize_tree_edges()

    def _edge_char_from_active_point(self):
        return self.text[self.active_edge_start_of_suffix]

    def _char_on_edge_at_active_length(self, node_on_edge):
        return self.text[node_on_edge.start + self.active_length]

    def _walk_down(self, next_node_on_edge):
        edge_len = next_node_on_edge.edge_length(self.global_end, SuffixTree.OPEN_EDGE_END)
        if self.active_length >= edge_len:
            self.active_node = next_node_on_edge
            self.active_length -= edge_len
            self.active_edge_start_of_suffix += edge_len
            return True
        return False

    def _create_node(self, start=-1, end=-1, suffix_id=-1):
        self.num_nodes += 1
        return Node(start, end, suffix_id)

    def _build_tree_internal(self):
        for i in range(self.N):
            self.global_end = i
            self.remainder += 1
            last_new_internal_node = None

            while self.remainder > 0:
                if self.active_length == 0:
                    self.active_edge_start_of_suffix = i - (self.remainder - 1)

                char_key_for_edge = self._edge_char_from_active_point()

                if char_key_for_edge not in self.active_node.children:
                    assert self.active_length == 0
                    current_suffix_actual_start_idx = i - (self.remainder - 1)
                    new_leaf = self._create_node(start=i, end=SuffixTree.OPEN_EDGE_END,
                                                 suffix_id=current_suffix_actual_start_idx)
                    self.active_node.children[char_key_for_edge] = new_leaf
                    if last_new_internal_node is not None:
                        last_new_internal_node.suffix_link = self.active_node
                        last_new_internal_node = None
                else:
                    next_node = self.active_node.children[char_key_for_edge]
                    if self._walk_down(next_node):
                        continue

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
                        new_leaf = self._create_node(start=i, end=SuffixTree.OPEN_EDGE_END,
                                                     suffix_id=current_suffix_actual_start_idx)
                        split_node.children[self.text[i]] = new_leaf

                        next_node.start = next_node.start + self.active_length
                        split_node.children[self.text[next_node.start]] = next_node

                        if last_new_internal_node is not None:
                            last_new_internal_node.suffix_link = split_node
                        last_new_internal_node = split_node

                self.remainder -= 1
                if self.active_node == self.root and self.active_length > 0:
                    self.active_length -= 1
                    if self.active_length > 0:
                        self.active_edge_start_of_suffix = (i - (self.remainder - 1)) - self.active_length
                elif self.active_node != self.root:
                    self.active_node = self.active_node.suffix_link

    def _finalize_tree_edges_recursive(self, node, final_val):
        if node.start != -1 and node.end == SuffixTree.OPEN_EDGE_END:
            node.end = final_val
        for child_node in node.children.values():
            self._finalize_tree_edges_recursive(child_node, final_val)

    def _finalize_tree_edges(self):
        self._finalize_tree_edges_recursive(self.root, self.N - 1)

    def get_num_nodes(self):
        return self.num_nodes


# --- Implementacja Tablicy Sufiksów i LCP ---
def construct_suffix_array_and_lcp(text: str, add_terminator=True):
    if add_terminator and (not text or text[-1] != "$"):
        text_internal = text + "$"
    else:
        text_internal = text

    n = len(text_internal)

    # Prosta konstrukcja tablicy sufiksów O(N^2 log N) lub O(N log^2 N) z porównaniami
    # W Pythonie, sortowanie krotek (sufiks, indeks) jest bardziej w stylu O(N^2 log N)
    # Alternatywnie: sortuj indeksy używając sufiksów jako kluczy
    sa = sorted(range(n), key=lambda i: text_internal[i:])

    # Konstrukcja LCP array (Kasai's Algorithm - O(N))
    lcp = [0] * n
    # inv_sa[SA[i]] = i (rank array)
    inv_sa = [0] * n
    for i in range(n):
        inv_sa[sa[i]] = i

    k = 0  # Długość bieżącego LCP
    for i in range(n):  # Przechodzimy przez tekst w oryginalnej kolejności
        if inv_sa[i] == n - 1:  # Ostatni sufiks w SA nie ma następcy
            k = 0
            continue

        # j to indeks w tekście następnego sufiksu w SA po sufiksie text[i:]
        j = sa[inv_sa[i] + 1]

        # Oblicz LCP(text[i:], text[j:])
        while i + k < n and j + k < n and text_internal[i + k] == text_internal[j + k]:
            k += 1
        lcp[inv_sa[i] + 1] = k  # LCP dla SA[inv_sa[i]+1] i SA[inv_sa[i]]
        # Zapisujemy w pozycji odpowiadającej drugiemu sufiksowi w parze

        if k > 0:
            k -= 1

    return sa, lcp, text_internal  # Zwracamy też tekst, bo może być zmodyfikowany


# --- Pomiar Pamięci ---
# sys.getsizeof jest płytki. Dla głębokiego rozmiaru, potrzebujemy czegoś więcej.
# Prosta rekursywna funkcja dla drzewa sufiksów.
# Dla tablicy sufiksów, sys.getsizeof na liście integerów jest dość reprezentatywne.

def get_deep_sizeof_st_node(node, text_ref_size, visited_nodes):
    if node.node_creation_id in visited_nodes:  # suffix_link może tworzyć cykle
        return 0
    visited_nodes.add(node.node_creation_id)

    size = sys.getsizeof(node)
    size += sys.getsizeof(node.children)  # Rozmiar słownika
    for char_key, child_node in node.children.items():
        size += sys.getsizeof(char_key)  # Rozmiar klucza (znaku)
        size += get_deep_sizeof_st_node(child_node, text_ref_size, visited_nodes)

    # Pola start, end, id to inty, ich rozmiar jest w sys.getsizeof(node)
    # suffix_link to referencja, rozmiar referencji jest w sys.getsizeof(node)
    return size


def get_suffix_tree_memory(st_instance):
    if st_instance is None: return 0

    total_size = sys.getsizeof(st_instance)
    total_size += sys.getsizeof(st_instance.text)  # Sam tekst

    # Rozmiar korzenia i jego potomków
    visited_nodes_for_size = set()
    total_size += get_deep_sizeof_st_node(st_instance.root, sys.getsizeof(st_instance.text), visited_nodes_for_size)

    # Dodatkowe atrybuty instancji SuffixTree
    total_size += sys.getsizeof(st_instance.active_node)  # To referencja, ale dla pewności
    total_size += sys.getsizeof(st_instance.active_edge_start_of_suffix)
    total_size += sys.getsizeof(st_instance.active_length)
    total_size += sys.getsizeof(st_instance.remainder)
    total_size += sys.getsizeof(st_instance.global_end)
    # ... i inne drobne atrybuty

    return total_size


# --- Główna funkcja porównawcza ---
def compare_suffix_structures(text_input: str) -> dict:
    results = {
        "suffix_array": {
            "construction_time_ms": 0,
            "memory_usage_bytes": 0,  # Zmieniono na bajty dla większej precyzji
            "size": 0,  # Liczba elementów w SA (+ LCP)
            "lcp_construction_time_ms": 0  # Oddzielnie dla LCP, jeśli chcemy
        },
        "suffix_tree": {
            "construction_time_ms": 0,
            "memory_usage_bytes": 0,
            "size": 0  # Liczba węzłów
        }
    }

    # --- Tablica Sufiksów ---
    gc.collect()  # Wymuś garbage collection przed pomiarem
    mem_before_sa = sys.getallocatedblocks() if hasattr(sys, 'getallocatedblocks') else 0  # Python 3.4+

    time_sa_start = time.perf_counter()
    sa, lcp, text_for_sa = construct_suffix_array_and_lcp(text_input, add_terminator=True)
    time_sa_end = time.perf_counter()

    results["suffix_array"]["construction_time_ms"] = (time_sa_end - time_sa_start) * 1000

    # Pamięć dla SA i LCP
    mem_sa = sys.getsizeof(sa)
    for x in sa: mem_sa += sys.getsizeof(x)  # Rozmiar intów w liście
    mem_lcp = sys.getsizeof(lcp)
    for x in lcp: mem_lcp += sys.getsizeof(x)
    mem_text_sa = sys.getsizeof(text_for_sa)  # Tekst używany przez SA

    results["suffix_array"]["memory_usage_bytes"] = mem_sa + mem_lcp + mem_text_sa  # Głównie listy intów i tekst
    # Alternatywnie, spróbujmy przez alokację, jeśli dostępne:
    if hasattr(sys, 'getallocatedblocks'):
        mem_after_sa = sys.getallocatedblocks()
        # To jest przybliżenie, bo inne rzeczy mogły być alokowane.
        # Lepsze byłoby użycie pympler.asizeof
        # Na razie, powyższe `sys.getsizeof` jest naszym wskaźnikiem.

    results["suffix_array"]["size"] = len(sa) + len(lcp)  # SA + LCP

    del sa, lcp, text_for_sa  # Zwolnij pamięć
    gc.collect()

    # --- Drzewo Sufiksów ---
    mem_before_st = sys.getallocatedblocks() if hasattr(sys, 'getallocatedblocks') else 0

    time_st_start = time.perf_counter()
    st = SuffixTree(text_input, add_terminator=True)
    time_st_end = time.perf_counter()

    results["suffix_tree"]["construction_time_ms"] = (time_st_end - time_st_start) * 1000
    results["suffix_tree"]["memory_usage_bytes"] = get_suffix_tree_memory(st)
    results["suffix_tree"]["size"] = st.get_num_nodes()

    del st
    gc.collect()

    return results


# --- Generowanie Danych Testowych i Wykresów ---
def run_experiments_and_plot():
    # text_lengths = [100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
    text_lengths = [100, 500, 1000, 2500, 5000, 7500, 10000]  # Mniejsze dla szybszych testów
    if len(sys.argv) > 1 and sys.argv[1] == 'full':  # Uruchom pełny zestaw
        text_lengths = [100, 1000, 10000, 20000, 50000, 75000, 100000]

    all_results = {"sa": [], "st": []}

    for length in text_lengths:
        print(f"Testing with text length: {length}")
        # Generuj tekst losowy, ale powtarzalny dla spójności między przebiegami, jeśli potrzebne
        # random.seed(42)
        # text = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
        # Dla trudniejszych przypadków (więcej powtórzeń)
        alphabet = string.ascii_lowercase[:4]  # Mały alfabet 'abcd'
        text = ''.join(random.choice(alphabet) for _ in range(length))

        res = compare_suffix_structures(text)
        all_results["sa"].append(res["suffix_array"])
        all_results["st"].append(res["suffix_tree"])
        print(
            f"  SA: Time={res['suffix_array']['construction_time_ms']:.2f}ms, Mem={res['suffix_array']['memory_usage_bytes'] / 1024:.2f}KB, Size={res['suffix_array']['size']}")
        print(
            f"  ST: Time={res['suffix_tree']['construction_time_ms']:.2f}ms, Mem={res['suffix_tree']['memory_usage_bytes'] / 1024:.2f}KB, Size={res['suffix_tree']['size']}")

    # Wykresy
    fig, axs = plt.subplots(3, 1, figsize=(10, 18))
    plt.subplots_adjust(hspace=0.4)

    # 1. Czas konstrukcji
    axs[0].plot(text_lengths, [r["construction_time_ms"] for r in all_results["sa"]], marker='o',
                label="Suffix Array (construct_suffix_array_and_lcp)")
    axs[0].plot(text_lengths, [r["construction_time_ms"] for r in all_results["st"]], marker='x',
                label="Suffix Tree (Ukkonen)")
    axs[0].set_xlabel("Rozmiar tekstu (N)")
    axs[0].set_ylabel("Czas konstrukcji (ms)")
    axs[0].set_title("Czas konstrukcji w zależności od rozmiaru tekstu")
    axs[0].legend()
    axs[0].grid(True)
    axs[0].set_xscale('log')
    axs[0].set_yscale('log')

    # 2. Zużycie pamięci
    axs[1].plot(text_lengths, [r["memory_usage_bytes"] / 1024 for r in all_results["sa"]], marker='o',
                label="Suffix Array (SA + LCP + Text)")
    axs[1].plot(text_lengths, [r["memory_usage_bytes"] / 1024 for r in all_results["st"]], marker='x',
                label="Suffix Tree (Nodes + Text)")
    axs[1].set_xlabel("Rozmiar tekstu (N)")
    axs[1].set_ylabel("Zużycie pamięci (KB)")
    axs[1].set_title("Zużycie pamięci w zależności od rozmiaru tekstu")
    axs[1].legend()
    axs[1].grid(True)
    axs[1].set_xscale('log')
    axs[1].set_yscale('log')

    # 3. Rozmiar (liczba elementów/węzłów)
    axs[2].plot(text_lengths, [r["size"] for r in all_results["sa"]], marker='o',
                label="Suffix Array (len(SA) + len(LCP))")
    axs[2].plot(text_lengths, [r["size"] for r in all_results["st"]], marker='x', label="Suffix Tree (liczba węzłów)")
    axs[2].set_xlabel("Rozmiar tekstu (N)")
    axs[2].set_ylabel("Rozmiar struktury")
    axs[2].set_title("Rozmiar struktury w zależności od rozmiaru tekstu")
    axs[2].legend()
    axs[2].grid(True)
    axs[2].set_xscale('log')
    # axs[2].set_yscale('log') # Rozmiar jest liniowy, więc log niekoniecznie

    plt.suptitle("Porównanie Tablicy Sufiksów i Drzewa Sufiksów", fontsize=16)
    plt.savefig("suffix_structures_comparison.png")
    print("\nWykresy zapisane jako suffix_structures_comparison.png")
    plt.show()


if __name__ == '__main__':
    # Uwaga: Aby uzyskać bardziej wiarygodne pomiary pamięci, szczególnie dla SuffixTree,
    # biblioteka taka jak `pympler` (asizeof.asizeof) byłaby lepsza niż sys.getsizeof.
    # Nasza implementacja get_deep_sizeof_st_node jest przybliżeniem.
    print("Uruchamianie eksperymentów... Może to chwilę potrwać.")
    print("Możesz uruchomić z argumentem 'full' dla dłuższego zestawu testów: python skrypt.py full")
    run_experiments_and_plot()