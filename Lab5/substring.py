class Node:
    _node_count_debug = 0

    def __init__(self, start=-1, end=-1, suffix_id=-1):
        self.children = {}
        self.suffix_link = None
        self.start = start
        self.end = end  # Może być SuffixTree.OPEN_EDGE_END lub konkretny int
        self.id = suffix_id  # Indeks początkowy sufiksu (dla liści)

        Node._node_count_debug += 1
        self.debug_id = Node._node_count_debug

        # Informacje potrzebne do LCS
        self.string_ids_in_subtree = set()  # Zbiór ID ciągów, których sufiksy są w tym poddrzewie
        self.leaf_suffix_starts = {}  # Dla liści: {string_id: original_start_index}
        # Dla węzłów wewn: przechowuje info dla celów LCS, np. najgłębszy wspólny

    def edge_length(self, current_global_end):
        _end = current_global_end if self.end == SuffixTree.OPEN_EDGE_END else self.end
        return _end - self.start + 1

    def is_leaf(self):
        return not self.children

    def __str__(self):
        return (f"Node(id={self.debug_id}, start={self.start}, end={self.end}, "
                f"suffix_id={self.id}, children_keys={list(self.children.keys())}, "
                f"sl->{self.suffix_link.debug_id if self.suffix_link else None}, "
                f"str_ids_subtree={self.string_ids_in_subtree})")


class SuffixTree:
    OPEN_EDGE_END = object()

    def __init__(self, text: str, num_strings_info=None):
        """
        Args:
            text: The input text (possibly concatenated with separators).
            num_strings_info: List of tuples (original_string_id, length_of_original_string_before_sep)
                              lub None, jeśli tylko jeden ciąg.
                              Np. dla "str1#str2$", info = [(0, len(str1)), (1, len(str2))]
                              Separator jest liczony jako część poprzedniego ciągu dla uproszczenia offsetu.
        """
        self.text = text  # Zakładamy, że "$" jest już dodany, jeśli to ostatni ciąg
        self.N = len(self.text)
        Node._node_count_debug = 0
        self.root = Node()
        self.root.suffix_link = self.root

        self.active_node = self.root
        self.active_edge_start_of_suffix = 0
        self.active_length = 0
        self.remainder = 0
        self.global_end = -1  # Bieżący indeks w fazie

        self._tree_finalized = False
        self.num_strings_info = num_strings_info  # Dla LCS

        self.build_tree()

    def _edge_char_from_active_point(self):
        return self.text[self.active_edge_start_of_suffix]

    def _char_on_edge_at_active_length(self, node_on_edge):
        return self.text[node_on_edge.start + self.active_length]

    def _walk_down(self, next_node_on_edge):
        edge_len = next_node_on_edge.edge_length(self.global_end)
        if self.active_length >= edge_len:
            self.active_node = next_node_on_edge
            self.active_length -= edge_len
            self.active_edge_start_of_suffix += edge_len
            return True
        return False

    def build_tree(self):
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
                    new_leaf = Node(start=i, end=SuffixTree.OPEN_EDGE_END, suffix_id=current_suffix_actual_start_idx)
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
                        split_node = Node(start=next_node.start, end=split_node_end_idx)
                        self.active_node.children[char_key_for_edge] = split_node

                        current_suffix_actual_start_idx = i - (self.remainder - 1)
                        new_leaf = Node(start=i, end=SuffixTree.OPEN_EDGE_END,
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
                    # Wcześniej: self.active_edge_start_of_suffix = i - self.remainder +1 - self.active_length
                    # Teraz, gdy self.active_length jest > 0, oznacza to, że active_edge_start_of_suffix
                    # powinno zostać przesunięte o 1 w prawo.
                    # Aktualny sufiks: S_k = text[k...i]. Następny S_{k+1} = text[k+1...i]
                    # active_edge_start_of_suffix wskazuje na k. Po przejściu do S_{k+1},
                    # active_edge_start_of_suffix powinno wskazywać na k+1.
                    # Jeśli self.active_length > 0, to self.active_edge_start_of_suffix +=1
                    # wydaje się bardziej intuicyjne.
                    # Lub, jeśli self.active_edge_start_of_suffix jest rozumiane jako początek przetwarzanego sufiksu:
                    if self.active_length > 0:
                        self.active_edge_start_of_suffix = (i - (self.remainder - 1)) - self.active_length
                    # else: active_edge_start_of_suffix zostanie ustawiony na początku pętli while

                elif self.active_node != self.root:
                    self.active_node = self.active_node.suffix_link

        self.finalize_tree()  # Automatycznie finalizuj po budowie

    def _fix_open_edges_recursive(self, node, final_val):
        if node.start != -1 and node.end == SuffixTree.OPEN_EDGE_END:
            node.end = final_val
        for child_node in node.children.values():
            self._fix_open_edges_recursive(child_node, final_val)

    def finalize_tree(self):
        if self._tree_finalized:
            return
        # global_end wskazuje na ostatni przetworzony znak, więc to jest N-1
        self._fix_open_edges_recursive(self.root, self.N - 1)
        self._tree_finalized = True

        # Po finalizacji, oznacz liście informacją o pochodzeniu
        if self.num_strings_info:
            self._mark_leaf_string_ids(self.root)

    def _get_string_id_and_original_start(self, suffix_start_in_combined):
        """Określa, z którego oryginalnego ciągu pochodzi sufiks i jaki jest jego start w tym ciągu."""
        current_offset = 0
        for str_id, length_before_sep in self.num_strings_info:
            # Długość ciągu oryginalnego (bez jego separatora)
            # Zakładamy, że `length_before_sep` to `len(original_str_i)`
            # Jeśli suffix_start_in_combined < current_offset + length_before_sep, to należy do str_id
            if suffix_start_in_combined < current_offset + length_before_sep:
                return str_id, suffix_start_in_combined - current_offset
            current_offset += length_before_sep + 1  # +1 za separator
        # Jeśli nie znaleziono, to błąd lub ostatni ciąg (który może nie mieć info w num_strings_info)
        # Jeśli num_strings_info pokrywa wszystkie ciągi oprócz ostatniego specjalnego ($), to ok.
        # Dla bezpieczeństwa, zwróćmy ostatni znany ID, jeśli nic nie pasuje (co nie powinno się zdarzyć)
        last_str_id, last_len = self.num_strings_info[-1]
        # Sprawdźmy czy to ostatni ciąg, który może nie mieć separatora w `length_before_sep`
        if suffix_start_in_combined < current_offset + last_len:  # Ostatni ciąg nie ma +1 za separator
            return last_str_id, suffix_start_in_combined - current_offset

        # Powinno być obsłużone przez pętlę, jeśli num_strings_info jest kompletne
        # Np. dla "s1#s2$", num_strings_info=[(0, len(s1)), (1, len(s2))]
        # sufiks "$" start=len(s1)+1+len(s2)
        # pętla:
        # id=0, len=len(s1). offset=0. start < 0+len(s1)? (nie, jeśli z s2 lub $)
        # offset = len(s1)+1
        # id=1, len=len(s2). start < len(s1)+1+len(s2)? (tak, jeśli z s2 lub $) -> return 1, start-(len(s1)+1)
        # To powinno działać.
        raise ValueError(f"Nie można określić ID ciągu dla sufiksu startującego w {suffix_start_in_combined}")

    def _mark_leaf_string_ids(self, node):
        if node.is_leaf():
            if node.id != -1:  # Prawidłowy liść
                str_id, original_start = self._get_string_id_and_original_start(node.id)
                node.string_ids_in_subtree.add(str_id)
                node.leaf_suffix_starts[str_id] = original_start
        else:
            for child_node in node.children.values():
                self._mark_leaf_string_ids(child_node)
                node.string_ids_in_subtree.update(child_node.string_ids_in_subtree)

    def _collect_leaf_ids_dfs(self, node: Node, results: list[int]):
        if node.is_leaf():
            if node.id != -1:
                results.append(node.id)
        for child_node in node.children.values():
            self._collect_leaf_ids_dfs(child_node, results)

    def find_pattern(self, pattern: str) -> list[int]:
        if not pattern: return []
        current_node = self.root
        pattern_idx = 0

        # Upewnij się, że drzewo jest sfinalizowane dla poprawnych długości krawędzi
        # self.finalize_tree() # Powinno być zrobione po __init__

        while pattern_idx < len(pattern):
            char_to_match = pattern[pattern_idx]
            if char_to_match not in current_node.children:
                return []

            edge_node = current_node.children[char_to_match]
            # Użyj N-1 jako global_end dla obliczeń długości krawędzi po konstrukcji
            edge_len = edge_node.edge_length(self.N - 1)

            for i in range(edge_len):
                if pattern_idx >= len(pattern): break
                text_char_on_edge = self.text[edge_node.start + i]
                pattern_char = pattern[pattern_idx]
                if text_char_on_edge != pattern_char: return []
                pattern_idx += 1

            if pattern_idx == len(pattern):
                occurrences = []
                # Zbieraj ID liści z self.text, a nie z oryginalnych stringów
                self._collect_leaf_ids_dfs(edge_node, occurrences)
                return sorted(list(set(occurrences)))
            current_node = edge_node
        return []

    def print_tree_recursive(self, node, indent="", edge_label_prefix=""):
        label = ""
        if node.start != -1:
            _end = node.end if node.end != SuffixTree.OPEN_EDGE_END else (self.N - 1)  # Użyj N-1 dla wizualizacji
            label = self.text[node.start: _end + 1]

        suffix_id_str = f" (sid:{node.id})" if node.id != -1 else ""
        sl_str = f" [sl->{node.suffix_link.debug_id if node.suffix_link else 'None'}]" if node != self.root else ""
        str_ids_info = f" str_ids:{node.string_ids_in_subtree}" if node.string_ids_in_subtree else ""
        leaf_starts_info = f" leaf_starts:{node.leaf_suffix_starts}" if node.leaf_suffix_starts else ""

        print(
            f"{indent}{edge_label_prefix}'{label}' (nid:{node.debug_id}){suffix_id_str}{sl_str}{str_ids_info}{leaf_starts_info}")

        for char_key, child_node in sorted(node.children.items()):  # Sortuj dla spójności wydruku
            self.print_tree_recursive(child_node, indent + "  ", f"{char_key} -> ")

    def print_tree(self):
        print(f"Suffix Tree for: '{self.text}'")
        self.print_tree_recursive(self.root)


def longest_common_substring(str1: str, str2: str) -> str:
    """
    Find the longest common substring of two strings using a suffix tree.
    """
    if not str1 or not str2:
        return ""

    # Unikalne separatory, różne od potencjalnego końca tekstu ($)
    # Użyjemy znaków o wysokich wartościach Unicode, mało prawdopodobne w typowym tekście.
    sep1 = "\x01"
    sep2 = "\x02"

    combined_text = str1 + sep1 + str2 + sep2

    # Informacje dla SuffixTree do identyfikacji pochodzenia sufiksów
    # (string_id, length_of_original_string_WITHOUT_its_separator)
    # Długość `str1` to `len(str1)`. Długość `str2` to `len(str2)`.
    # Separator sep1 jest na indeksie len(str1).
    # str2 zaczyna się na len(str1)+1.
    num_strings_info = [
        (0, len(str1)),  # string 0 ma długość len(str1)
        (1, len(str2))  # string 1 ma długość len(str2)
    ]

    st = SuffixTree(combined_text, num_strings_info=num_strings_info)
    # st.print_tree() # Do debugowania

    max_len = 0
    lcs_end_pos_in_combined = -1  # Koniec LCS w combined_text

    # DFS do znalezienia najgłębszego węzła, którego poddrzewo zawiera sufiksy z obu ciągów
    # `path_len` to długość ścieżki od korzenia do *rodzica* bieżącego `node`
    # `node_depth` to długość ścieżki do `node`

    # Zmienne do przechowywania wyniku
    # Używamy nonlocal lub atrybutów obiektu, jeśli DFS jest metodą klasy,
    # albo przekazujemy listę/słownik do modyfikacji.
    # Tutaj zrobimy to jako funkcję zagnieżdżoną.

    # global_end dla obliczania długości krawędzi po konstrukcji
    final_ge = len(combined_text) - 1

    # Zmienne do śledzenia LCS
    # Dostęp przez listę, aby móc modyfikować w zagnieżdżonej funkcji
    # result_tracker[0] = max_len, result_tracker[1] = lcs_start_in_str1
    result_tracker = [0, -1]

    def find_lcs_dfs(node, current_depth):
        # Jeśli node.string_ids_in_subtree zostało już obliczone przez _mark_leaf_string_ids,
        # nie musimy tego robić tutaj ponownie.
        # Ta funkcja DFS służy tylko do znalezienia najgłębszego węzła wspólnego.

        if 0 in node.string_ids_in_subtree and 1 in node.string_ids_in_subtree:
            # Ten węzeł (lub ścieżka do niego) jest wspólny
            if current_depth > result_tracker[0]:
                result_tracker[0] = current_depth
                # Aby znaleźć początek: potrzebujemy startu krawędzi prowadzącej do tego węzła
                # i odjąć (current_depth - długość tej krawędzi).
                # Prościej: jeśli 'node' jest wynikiem, to ścieżka do niego ma 'current_depth'.
                # Sufiks zaczynający się od node.id (jeśli liść) lub dowolnego liścia w poddrzewie
                # z string_id=0, będzie zawierał ten LCS.
                # start_LCS_in_combined = node.start - (current_depth - node.edge_length(final_ge))
                # To jest skomplikowane. Zamiast tego, znajdźmy dowolny liść z string_id=0 w poddrzewie tego node.

                # Znajdźmy jakikolwiek liść z string_id=0 w poddrzewie tego węzła.
                # To da nam start_pos_in_combined dla całego sufiksu.
                # LCS to prefiks tego sufiksu o długości current_depth.
                # Start LCS = start_pos_in_combined.

                # Prostszy sposób: przechowajmy sam węzeł
                # result_tracker[1] = node # Zamiast lcs_start_in_str1
                # A jeszcze prościej: node.start to początek etykiety krawędzi DO TEGO WĘZŁA.
                # Ścieżka od korzenia do tego węzła reprezentuje LCS.
                # Jej początek w combined_text to node.start - (current_depth - node.edge_length(final_ge))
                # To jest start etykiety na ostatniej krawędzi ścieżki.
                # To nie jest to, czego szukamy.
                # Szukamy startu całego LCS w str1.
                # Znajdźmy liść z string_id=0 pod tym węzłem.
                # Jego node.id to start_sufiksu_w_combined. LCS to combined_text[node.id : node.id + current_depth]
                # A w str1 to str1[oryginalny_start : oryginalny_start + current_depth]

                # Potrzebujemy oryginalnego indeksu startowego.
                # Musimy przeszukać poddrzewo node, aby znaleźć liść z string_id = 0.
                # To może być nieefektywne.
                # Zamiast tego, _mark_leaf_string_ids powinno było propagować min_start_index.
                # Na razie, dla uproszczenia, po znalezieniu max_len, zrobimy drugi DFS.
                # Albo:
                # Przyjmijmy, że `node.start` krawędzi prowadzącej do węzła `node` jest częścią ścieżki.
                # Ścieżka do `node` ma długość `current_depth`.
                # Etykieta na krawędzi do `node` to `combined_text[node.start : node.end+1]`
                # Początek tej etykiety w `combined_text` to `node.start`.
                # Początek LCS w `combined_text` to `node.start - (current_depth - node.edge_length(final_ge))`.
                # To jest początek ostatniej krawędzi na ścieżce. Nie, to nie to.

                # Najprościej jest zapamiętać node i potem odtworzyć ścieżkę.
                # Lub, jeśli mamy start_id jakiegoś sufiksu z str1, który przechodzi przez ten węzeł:
                # start_LCS_w_str1 = ten_start_id. LCS = str1[start_LCS_w_str1 : start_LCS_w_str1 + current_depth]
                # Zmodyfikujmy _mark_leaf_string_ids, aby przechowywać `min_original_start_for_string_id` w węzłach.
                # To na razie pominiemy dla prostoty i zrekonstruujemy po znalezieniu długości.

                # Zapamiętujemy koniec LCS w combined_text. Najgłębszy węzeł 'node' oznacza,
                # że ścieżka kończy się na końcu krawędzi prowadzącej do 'node' (jeśli 'node'
                # nie jest korzeniem).
                # lcs_end_pos_in_combined to node.end (jeśli node nie jest rootem)
                # To też nie jest poprawne. LCS może kończyć się w środku krawędzi.
                # `current_depth` jest kluczowe.
                # Po znalezieniu max_len, odtworzymy string.
                pass

        for child_node in node.children.values():
            find_lcs_dfs(child_node, current_depth + child_node.edge_length(final_ge))

    find_lcs_dfs(st.root, 0)

    max_lcs_len = result_tracker[0]

    if max_lcs_len == 0:
        return ""

    # Odtworzenie LCS: Znajdź węzeł i ścieżkę, która dała max_lcs_len
    # i upewnij się, że pochodzi z str1.
    # Można to zrobić przez ponowne DFS lub przechowywanie więcej info.
    # Najprościej: wiemy, że LCS o długości max_lcs_len istnieje.
    # Przeszukajmy wszystkie sufiksy str1. Dla każdego sufiksu str1[i:],
    # sprawdźmy, czy str1[i : i+max_lcs_len] występuje w str2.
    # To nie jest efektywne.

    # Lepsze odtworzenie:
    # Ponownie DFS, tym razem szukając węzła na głębokości max_lcs_len
    # który ma w poddrzewie string_id=0 i string_id=1.
    # Gdy znajdziemy taki węzeł, musimy znaleźć start tego LCS w oryginalnym str1.
    # Potrzebujemy start_index_of_suffix_from_str1_that_goes_through_this_node.

    lcs_str = ""
    # Drugi DFS do odtworzenia
    path_chars = []

    # Zmienna do przechowywania znalezionego LCS
    # Dostęp przez listę, aby móc modyfikować w zagnieżdżonej funkcji
    # lcs_found_container[0] = "znaleziony_lcs"
    lcs_found_container = [""]

    def reconstruct_lcs_dfs(node, current_depth, current_path_chars):
        if lcs_found_container[0]:  # Już znaleziono
            return

        if 0 in node.string_ids_in_subtree and 1 in node.string_ids_in_subtree:
            if current_depth == max_lcs_len:
                # Mamy węzeł (lub ścieżkę na krawędzi), który jest LCS
                # Musimy znaleźć start tego LCS w oryginalnym str1.
                # Przeszukaj poddrzewo node w poszukiwaniu liścia z string_id=0

                queue = [node]
                found_start_in_str1 = -1

                visited_dfs_reconstruct = set()

                # DFS w poddrzewie `node` aby znaleźć liść z str1
                # (lub użyj `node.leaf_suffix_starts` jeśli zaimplementowane głębiej)
                temp_q = [node]
                processed_nodes = set()
                leaf_from_str1_id_in_combined = -1

                while temp_q:
                    curr_n = temp_q.pop(0)
                    if curr_n.debug_id in processed_nodes:
                        continue
                    processed_nodes.add(curr_n.debug_id)

                    if curr_n.is_leaf():
                        # Sprawdź, czy ten liść pochodzi z str1
                        # node.id to start w combined_text
                        if curr_n.id < len(str1):  # Pochodzi z str1
                            leaf_from_str1_id_in_combined = curr_n.id
                            break
                    for child in curr_n.children.values():
                        if child.debug_id not in processed_nodes:
                            temp_q.append(child)

                if leaf_from_str1_id_in_combined != -1:
                    # LCS to combined_text[leaf_from_str1_id_in_combined : leaf_from_str1_id_in_combined + max_lcs_len]
                    # Ale my chcemy z oryginalnego str1:
                    # original_start_in_str1 to to samo co leaf_from_str1_id_in_combined
                    lcs_found_container[0] = str1[
                                             leaf_from_str1_id_in_combined: leaf_from_str1_id_in_combined + max_lcs_len]
                else:
                    # To nie powinno się zdarzyć, jeśli logika jest poprawna
                    # Alternatywnie, odtwórz ze ścieżki znaków
                    lcs_found_container[0] = "".join(current_path_chars)
                return

        # Kontynuuj DFS
        for char_key, child_node in child_node.children.items():
            edge_chars = list(st.text[child_node.start: child_node.end + 1])
            current_path_chars.extend(edge_chars)
            reconstruct_lcs_dfs(child_node, current_depth + len(edge_chars), current_path_chars)
            if lcs_found_container[0]: return  # Szybkie wyjście
            # Backtrack
            for _ in range(len(edge_chars)):
                current_path_chars.pop()

    # Ta metoda rekonstrukcji powyżej jest skomplikowana. Prostsza:
    # W pierwszym DFS, gdy `current_depth > result_tracker[0]`, zapisz `node.start` i `node.end`
    # węzła, który osiągnął tę głębokość. Etykieta do tego węzła jest LCS.
    # Ale to nie jest sam węzeł, to ścieżka.
    # Przechowajmy start_index_in_str1, który osiągnął ten LCS.

    # Uproszczony pierwszy DFS, który przechowuje więcej informacji:
    # result_tracker = [max_len, start_of_lcs_in_str1]
    result_tracker = [0, -1]

    def find_lcs_dfs_improved(node, current_depth):
        # Propaguj minimalny indeks startowy z str1
        min_s1_start_idx_in_node_subtree = float('inf')

        if node.is_leaf():
            if node.id != -1 and node.id < len(str1):  # Liść z str1
                min_s1_start_idx_in_node_subtree = node.id

        for child_node in node.children.values():
            child_min_s1_start = find_lcs_dfs_improved(child_node, current_depth + child_node.edge_length(final_ge))
            min_s1_start_idx_in_node_subtree = min(min_s1_start_idx_in_node_subtree, child_min_s1_start)

        if 0 in node.string_ids_in_subtree and 1 in node.string_ids_in_subtree:
            if current_depth > result_tracker[0]:
                result_tracker[0] = current_depth
                result_tracker[1] = min_s1_start_idx_in_node_subtree
                # Jeśli current_depth == result_tracker[0], wybierz mniejszy indeks startowy (leksykograficznie)
            elif current_depth == result_tracker[0] and min_s1_start_idx_in_node_subtree < result_tracker[1]:
                result_tracker[1] = min_s1_start_idx_in_node_subtree

        return min_s1_start_idx_in_node_subtree

    find_lcs_dfs_improved(st.root, 0)

    max_lcs_len = result_tracker[0]
    start_idx_in_str1 = result_tracker[1]

    if max_lcs_len > 0 and start_idx_in_str1 != float('inf') and start_idx_in_str1 != -1:
        return str1[start_idx_in_str1: start_idx_in_str1 + max_lcs_len]
    else:
        return ""


def longest_common_substring_multiple(strings: list[str]) -> str:
    if not strings or len(strings) < 2:
        return strings[0] if strings else ""
    if any(not s for s in strings):  # Jeśli któryś ciąg jest pusty, LCS jest pusty
        return ""

    num_actual_strings = len(strings)

    # Unikalne separatory dla każdego ciągu
    # Użyjemy znaków specjalnych z zakresu Private Use Area Unicode, np. E000+
    # lub prostsze, jeśli wiemy, że nie wystąpią w tekście
    separators = [chr(0xE000 + i) for i in range(num_actual_strings)]

    combined_text = ""
    num_strings_info = []  # (string_id, length_of_original_string_WITHOUT_its_separator)
    current_offset = 0

    for i, s in enumerate(strings):
        combined_text += s
        num_strings_info.append((i, len(s)))  # string_id = i, len = len(s)
        if i < num_actual_strings - 1:  # Nie dodawaj separatora po ostatnim ciągu
            combined_text += separators[i]
        # current_offset nie jest tu potrzebny, _get_string_id_and_original_start sobie poradzi

    # Ostatni ciąg potrzebuje unikalnego terminatora, jeśli nie ma go w separatorach
    # Ale nasza SuffixTree dodaje "$" jeśli to był jej oryginalny tekst.
    # Tutaj przekazujemy już połączony. Dodajmy końcowy unikalny terminator.
    final_terminator = chr(0xE000 + num_actual_strings)  # Jeszcze jeden unikalny znak
    combined_text += final_terminator

    # Zaktualizuj info dla ostatniego ciągu, aby uwzględnić, że nie ma po nim standardowego separatora,
    # ale jest final_terminator. Długość oryginalnego ciągu się nie zmienia.
    # Nasza funkcja _get_string_id_and_original_start używa długości oryginalnych ciągów
    # i odtwarza offsety na podstawie tych długości i faktu, że separatory mają dł. 1.

    st = SuffixTree(combined_text, num_strings_info=num_strings_info)
    # st.print_tree() # Do debugowania

    final_ge = len(combined_text) - 1

    result_tracker = [0, -1]  # [max_len, start_of_lcs_in_first_string_if_applicable]

    def find_lcs_dfs_multi(node, current_depth):
        min_s0_start_idx_in_node_subtree = float('inf')  # Start w pierwszym ciągu (id=0)

        if node.is_leaf():
            if node.id != -1:
                # Sprawdź, czy ten liść pochodzi z pierwszego ciągu (id=0)
                # _get_string_id_and_original_start(node.id) da nam (str_id, original_start)
                # Jeśli str_id == 0, to original_start jest tym, czego szukamy.
                # To jest już obsługiwane przez node.leaf_suffix_starts po _mark_leaf_string_ids
                if 0 in node.leaf_suffix_starts:
                    min_s0_start_idx_in_node_subtree = node.leaf_suffix_starts[0]

        for child_node in node.children.values():
            child_min_s0_start = find_lcs_dfs_multi(child_node, current_depth + child_node.edge_length(final_ge))
            min_s0_start_idx_in_node_subtree = min(min_s0_start_idx_in_node_subtree, child_min_s0_start)

        # Sprawdź, czy wszystkie string_ids są obecne w poddrzewie tego węzła
        # set(range(num_actual_strings)) to zbiór {0, 1, ..., k-1}
        if node.string_ids_in_subtree == set(range(num_actual_strings)):
            if current_depth > result_tracker[0]:
                result_tracker[0] = current_depth
                result_tracker[1] = min_s0_start_idx_in_node_subtree
            elif current_depth == result_tracker[0] and min_s0_start_idx_in_node_subtree < result_tracker[1]:
                result_tracker[1] = min_s0_start_idx_in_node_subtree

        return min_s0_start_idx_in_node_subtree

    find_lcs_dfs_multi(st.root, 0)

    max_lcs_len = result_tracker[0]
    start_idx_in_s0 = result_tracker[1]

    if max_lcs_len > 0 and start_idx_in_s0 != float('inf') and start_idx_in_s0 != -1:
        # LCS jest fragmentem pierwszego ciągu
        return strings[0][start_idx_in_s0: start_idx_in_s0 + max_lcs_len]
    else:
        return ""


def longest_palindromic_substring(text: str) -> str:
    if not text:
        return ""

    n = len(text)
    if n == 1:
        return text

    rev_text = text[::-1]

    # Separatory. Muszą być różne od siebie i od znaków w tekście.
    sep1 = "\x01"
    sep2 = "\x02"

    combined_text = text + sep1 + rev_text + sep2

    # Informacje dla SuffixTree
    # String 0 to 'text', String 1 to 'rev_text'
    num_strings_info = [
        (0, n),  # string 0 (text) ma długość n
        (1, n)  # string 1 (rev_text) ma długość n
    ]

    st = SuffixTree(combined_text, num_strings_info=num_strings_info)
    # st.print_tree() # Do debugowania

    final_ge = len(combined_text) - 1

    # result_tracker = [max_pal_len, start_of_palindrome_in_original_text]
    result_tracker = [0, -1]

    # DFS do znalezienia palindromu
    # Musimy zbierać zbiory indeksów startowych dla text i rev_text
    def find_lps_dfs(node, current_depth):
        # Zbiory oryginalnych indeksów startowych w poddrzewie tego węzła
        # Dla text: indeksy w oryginalnym 'text'
        # Dla rev_text: indeksy w oryginalnym 'rev_text'
        s0_indices_in_subtree = set()
        s1_indices_in_subtree = set()

        if node.is_leaf():
            if node.id != -1:  # Prawidłowy liść
                # node.leaf_suffix_starts przechowuje {str_id: original_start}
                if 0 in node.leaf_suffix_starts:
                    s0_indices_in_subtree.add(node.leaf_suffix_starts[0])
                if 1 in node.leaf_suffix_starts:
                    s1_indices_in_subtree.add(node.leaf_suffix_starts[1])

        for child_node in node.children.values():
            child_s0_indices, child_s1_indices = find_lps_dfs(child_node,
                                                              current_depth + child_node.edge_length(final_ge))
            s0_indices_in_subtree.update(child_s0_indices)
            s1_indices_in_subtree.update(child_s1_indices)

        # Jeśli ścieżka do 'node' jest wspólna dla 'text' i 'rev_text'
        if s0_indices_in_subtree and s1_indices_in_subtree:
            # current_depth to długość L potencjalnego palindromu
            # Sprawdź warunek palindromu: idx_text + idx_rev_text + L == n
            # Gdzie n to długość oryginalnego 'text'.
            # Szukamy i in s0_indices, j in s1_indices_rev_text_coords
            # takich, że i + j + current_depth == n
            # K = n - current_depth
            # Szukamy i + j == K

            # Optymalizacja: jeśli s1 jest mniejsze, iteruj po nim i sprawdzaj w s0 (w haszowanym s0)
            set_to_hash = s0_indices_in_subtree
            set_to_iter = s1_indices_in_subtree
            if len(s0_indices_in_subtree) > len(s1_indices_in_subtree):
                set_to_hash = s1_indices_in_subtree
                set_to_iter = s0_indices_in_subtree

            # Można stworzyć hash set z mniejszego zbioru dla szybszego sprawdzania
            # Jednak dla Pythona, 'in' na secie jest już szybkie.

            target_sum_minus_j = n - current_depth
            for j_rev_idx in set_to_iter:  # j_rev_idx to start w rev_text
                # Potrzebujemy i_text_idx takiego, że i_text_idx = target_sum_minus_j - j_rev_idx
                required_i_text_idx = target_sum_minus_j - j_rev_idx
                if required_i_text_idx in set_to_hash:  # set_to_hash to drugi zbiór
                    # Znaleziono palindrom o długości current_depth
                    # zaczynający się w 'text' od 'required_i_text_idx' (jeśli set_to_hash to s0)
                    # lub od innego i_text_idx z s0_indices... (jeśli set_to_hash to s1)

                    actual_start_in_text = -1
                    if set_to_hash == s0_indices_in_subtree:  # required_i_text_idx jest z s0
                        actual_start_in_text = required_i_text_idx
                    else:  # required_i_text_idx jest tym, co szukamy w s0, a j_rev_idx jest z s0, więc iterujemy po s0
                        # to znaczy, że `j_rev_idx` jest tak naprawdę `i_text_idx` (zmienna źle nazwana dla tego przypadku)
                        # a `required_i_text_idx` to to, czego szukamy w `s1_indices_in_subtree`
                        # Zmieńmy logikę, żeby była jaśniejsza:
                        pass  # Poniższa pętla jest bardziej ogólna

                    # Ogólniejsza pętla sprawdzająca:
                    for i_text_idx in s0_indices_in_subtree:
                        if (n - current_depth - i_text_idx) in s1_indices_in_subtree:
                            actual_start_in_text = i_text_idx  # Palindrom startuje tu w 'text'
                            if current_depth > result_tracker[0]:
                                result_tracker[0] = current_depth
                                result_tracker[1] = actual_start_in_text
                            elif current_depth == result_tracker[0] and actual_start_in_text < result_tracker[1]:
                                result_tracker[1] = actual_start_in_text
                            break  # Znaleziono parę dla tego węzła, idź dalej
                    break  # Znaleziono parę (i,j) dla tego węzła, przerywamy iterację po j_rev_idx

        return s0_indices_in_subtree, s1_indices_in_subtree

    find_lps_dfs(st.root, 0)

    max_pal_len = result_tracker[0]
    start_idx_in_text = result_tracker[1]

    if max_pal_len > 0 and start_idx_in_text != -1:
        return text[start_idx_in_text: start_idx_in_text + max_pal_len]
    elif not text and max_pal_len == 0:  # Pusty tekst
        return ""
    elif text and max_pal_len == 0:  # Niepusty tekst, ale nie znaleziono (np. błąd lub tylko pojedyncze znaki)
        # Każdy pojedynczy znak jest palindromem
        return text[0] if text else ""

    return ""  # Domyślnie, jeśli nic nie znaleziono


def lcs_dynamic_programming(str1: str, str2: str) -> str:
    m = len(str1)
    n = len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0
    end_pos_str1 = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_pos_str1 = i - 1  # Koniec w str1 (indeks 0-based)
            else:
                dp[i][j] = 0  # Dla podciągu wspólnego resetujemy, dla podsekwencji bralibyśmy max

    if max_len == 0:
        return ""
    return str1[end_pos_str1 - max_len + 1: end_pos_str1 + 1]


import time
import matplotlib.pyplot as plt
import random
import string


# Funkcje: longest_common_substring (z SuffixTree), lcs_dynamic_programming

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def run_lcs_experiments():
    lengths = [10, 50, 100, 200, 300, 400, 500, 700, 1000, 1500, 2000]  # Dla DP, większe mogą być wolne
    # lengths = [100, 500, 1000, 2000, 5000, 10000, 20000] # Dla SuffixTree

    times_st = []
    times_dp = []

    for l in lengths:
        print(f"Testing LCS for length: {l}")
        str1 = generate_random_string(l)
        # Dla testu LCS, drugi string może mieć inną długość, lub podobną
        # Aby LCS był sensowny, stwórzmy str2 z częścią str1
        if l > 10:
            common_part_len = l // 4
            common_start = random.randint(0, l - common_part_len - 1)
            common = str1[common_start: common_start + common_part_len]
            str2_l1 = generate_random_string(l // 2 - common_part_len // 2)
            str2_l2 = generate_random_string(l // 2 - common_part_len // 2)
            str2 = str2_l1 + common + str2_l2
            if len(str2) == 0 and l > 0: str2 = generate_random_string(l // 2)  # fallback
            if not str2: str2 = "a"  # na wypadek l=0
        else:
            str2 = generate_random_string(l)

        start_time = time.perf_counter()
        lcs_s = longest_common_substring(str1, str2)
        end_time = time.perf_counter()
        times_st.append(end_time - start_time)
        # print(f"  ST LCS: '{lcs_s}' ({end_time - start_time:.6f}s)")

        if l <= 2000:  # DP jest wolne dla dużych N
            start_time = time.perf_counter()
            lcs_d = lcs_dynamic_programming(str1, str2)
            end_time = time.perf_counter()
            times_dp.append(end_time - start_time)
            # print(f"  DP LCS: '{lcs_d}' ({end_time - start_time:.6f}s)")
            # assert lcs_s == lcs_d or len(lcs_s) == len(lcs_d) # Mogą znaleźć różne LCSy o tej samej długości
            if len(lcs_s) != len(lcs_d):
                print(f"WARN: LCS length mismatch for L={l}! ST: {len(lcs_s)}, DP: {len(lcs_d)}")
                # print(f"s1: {str1[:50]}, s2: {str2[:50]}")
                # print(f"LCS_ST: {lcs_s}, LCS_DP: {lcs_d}")
        else:
            times_dp.append(float('nan'))  # Za długo by czekać

    plt.figure(figsize=(10, 6))
    plt.plot(lengths, times_st, marker='o', label='Suffix Tree LCS')
    plt.plot(lengths[:len(times_dp)], times_dp, marker='x',
             label='Dynamic Programming LCS')  # Dopasuj długość osi X dla DP

    plt.xlabel("Długość ciągów (N)")
    plt.ylabel("Czas wykonania (s)")
    plt.title("Porównanie wydajności algorytmów LCS")
    plt.legend()
    plt.grid(True)
    plt.xscale('log')  # Można użyć skali logarytmicznej dla osi, jeśli zakresy są duże
    plt.yscale('log')
    plt.savefig("lcs_performance_comparison.png")
    print("Wykres zapisany jako lcs_performance_comparison.png")
    plt.show()

# Aby uruchomić testy i generowanie wykresu:
# run_lcs_experiments()