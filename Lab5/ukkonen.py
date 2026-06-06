class Node:
    _node_count_debug = 0  # Do debugowania, aby nadać unikalne ID każdemu węzłowi

    def __init__(self, start=-1, end=-1, suffix_id=-1):
        self.children = {}
        self.suffix_link = None
        self.start = start  # Indeks początkowy etykiety krawędzi PROWADZĄCEJ do tego węzła
        self.end = end  # Indeks końcowy etykiety krawędzi. Może być referencją do global_end.
        self.id = suffix_id  # Indeks początkowy sufiksu (tylko dla liści)

        Node._node_count_debug += 1
        self.debug_id = Node._node_count_debug

    def edge_length(self, current_global_end):
        # Jeśli self.end == SuffixTree.OPEN_EDGE_END, użyj obecnego global_end
        _end = current_global_end if self.end == SuffixTree.OPEN_EDGE_END else self.end
        return _end - self.start + 1

    def is_leaf(self):
        return not self.children

    def __str__(self):  # Pomocnicze do debugowania
        return f"Node(id={self.debug_id}, start={self.start}, end={self.end}, suffix_id={self.id}, children_keys={list(self.children.keys())}, sl->{self.suffix_link.debug_id if self.suffix_link else None})"


class SuffixTree:
    OPEN_EDGE_END = object()  # Unikalny obiekt-znacznik dla otwartych krawędzi

    def __init__(self, text: str):
        self.text = text + "$"  # Dodanie unikalnego znaku końca
        self.N = len(self.text)
        Node._node_count_debug = 0  # Resetuj licznik dla nowego drzewa
        self.root = Node()
        self.root.suffix_link = self.root  # Łącze sufiksowe korzenia wskazuje na siebie

        # Aktywny Punkt (AP)
        self.active_node = self.root
        # self.active_edge: indeks w self.text pierwszego znaku krawędzi z active_node.
        # Jeśli active_length = 0, active_edge wskazuje na text[i] (bieżący znak fazy).
        # W mojej implementacji, active_edge to indeks startowy sufiksu, który aktualnie przetwarzamy.
        self.active_edge_start_of_suffix = 0
        self.active_length = 0

        self.remainder = 0
        self.global_end = -1  # Indeks bieżącego znaku w fazie (np. dla text[i], global_end = i)

        self.build_tree()

    def _edge_char_from_active_point(self):
        """Zwraca znak w tekście, który odpowiada początkowi krawędzi
           zgodnie z aktywnym punktem (active_edge_start_of_suffix, active_length).
        """
        return self.text[self.active_edge_start_of_suffix]

    def _char_on_edge_at_active_length(self, node_on_edge):
        """Zwraca znak na krawędzi prowadzącej do node_on_edge,
           na pozycji wskazanej przez active_length.
        """
        return self.text[node_on_edge.start + self.active_length]

    def _walk_down(self, next_node_on_edge):
        """Implementuje technikę Skip/Count.
           Jeśli active_length >= długości krawędzi do next_node_on_edge,
           przesuwa active_point w dół drzewa.
           Zwraca True jeśli AP został zmieniony (przeskoczono węzeł), False wpp.
        """
        edge_len = next_node_on_edge.edge_length(self.global_end)
        if self.active_length >= edge_len:
            self.active_node = next_node_on_edge
            self.active_length -= edge_len
            self.active_edge_start_of_suffix += edge_len  # Przesuwamy "kursor" w sufiksie
            return True
        return False

    def build_tree(self):
        for i in range(self.N):  # Faza i, przetwarzamy znak self.text[i]
            self.global_end = i
            self.remainder += 1
            last_new_internal_node = None

            while self.remainder > 0:
                if self.active_length == 0:
                    # Jesteśmy w węźle, active_edge_start_of_suffix wskazuje na początek bieżącego sufiksu
                    # który zaczyna się od text[i - (remainder -1)]
                    self.active_edge_start_of_suffix = i - (self.remainder - 1)

                # Znak, który powinien być na początku krawędzi z active_node
                char_key_for_edge = self._edge_char_from_active_point()

                if char_key_for_edge not in self.active_node.children:
                    # Reguła 2 (jeśli active_node != root) lub 3 (jeśli active_node == root):
                    # Ścieżka nie istnieje, tworzymy nowy liść.
                    # active_length musi być 0, bo inaczej bylibyśmy na krawędzi, która istnieje.
                    assert self.active_length == 0

                    # Indeks początkowy tego konkretnego sufiksu
                    current_suffix_actual_start_idx = i - (self.remainder - 1)

                    new_leaf = Node(start=i, end=SuffixTree.OPEN_EDGE_END, suffix_id=current_suffix_actual_start_idx)
                    self.active_node.children[char_key_for_edge] = new_leaf

                    # Utwórz łącze sufiksowe z poprzednio utworzonego węzła wewnętrznego
                    if last_new_internal_node is not None:
                        last_new_internal_node.suffix_link = self.active_node
                        last_new_internal_node = None  # Reset, bo utworzyliśmy liść, nie węzeł wewnętrzny
                else:
                    # Krawędź istnieje.
                    next_node = self.active_node.children[char_key_for_edge]

                    if self._walk_down(next_node):  # Spróbuj przejść w dół (Skip/Count)
                        continue  # AP został zaktualizowany, zacznij pętlę while od nowa z nowym AP

                    # Jesteśmy na krawędzi (next_node), ale nie przeszliśmy jej całej.
                    # Znak na krawędzi, który porównujemy z text[i]
                    char_on_edge = self._char_on_edge_at_active_length(next_node)

                    if char_on_edge == self.text[i]:
                        # Reguła 1: Znak self.text[i] już jest na ścieżce.
                        # "Showstopper". Zwiększ active_length i zakończ tę fazę dla tego sufiksu.
                        self.active_length += 1
                        if last_new_internal_node is not None and self.active_node != self.root:
                            last_new_internal_node.suffix_link = self.active_node
                            # last_new_internal_node = None # Nie resetujemy, jeśli active_node to węzeł wewnętrzny
                            # bo łącze sufiksowe może być potrzebne w następnej iteracji.
                            # Jednakże, reguła 1 nie tworzy nowego węzła wewnętrznego,
                            # więc last_new_internal_node powinien być już None lub wskazywać
                            # na węzeł z poprzedniego podziału.
                            # Generalnie, po regule 1, jeśli last_new_internal_node istnieje,
                            # jego SL powinien wskazywać na active_node.
                        break  # Koniec pętli while dla bieżącego `remainder`
                    else:
                        # Reguła 2: Podział krawędzi.
                        # Tworzymy nowy węzeł wewnętrzny (split_node)
                        split_node_end_idx = next_node.start + self.active_length - 1
                        split_node = Node(start=next_node.start, end=split_node_end_idx)

                        # Aktualny active_node wskazuje teraz na split_node przez tę samą krawędź
                        self.active_node.children[char_key_for_edge] = split_node

                        # Nowy liść dla znaku self.text[i]
                        current_suffix_actual_start_idx = i - (self.remainder - 1)
                        new_leaf = Node(start=i, end=SuffixTree.OPEN_EDGE_END,
                                        suffix_id=current_suffix_actual_start_idx)
                        split_node.children[self.text[i]] = new_leaf

                        # Stary next_node staje się dzieckiem split_node
                        next_node.start = next_node.start + self.active_length
                        split_node.children[
                            self.text[next_node.start]] = next_node  # Kluczem jest nowy pierwszy znak krawędzi

                        # Utwórz łącze sufiksowe
                        if last_new_internal_node is not None:
                            last_new_internal_node.suffix_link = split_node
                        last_new_internal_node = split_node

                # Jeden sufiks został przetworzony (jawnie dodany lub znaleziony)
                self.remainder -= 1

                # Aktualizacja Aktywnego Punktu za pomocą łącza sufiksowego (Reguła 3)
                if self.active_node == self.root and self.active_length > 0:
                    self.active_length -= 1
                    # active_edge_start_of_suffix przesuwa się o 1, bo przetwarzamy krótszy sufiks
                    # text[ (i - remainder +1) ... i ] -> text[ (i - remainder +1)+1 ... i ]
                    # Jeśli active_length = 0, self.active_edge_start_of_suffix zostanie ustawione na początku pętli while.
                    if self.active_length > 0:  # tylko jeśli nadal jesteśmy na krawędzi
                        self.active_edge_start_of_suffix = i - (self.remainder - 1) - self.active_length
                    # else: self.active_edge_start_of_suffix zostanie ustawiony na i - (self.remainder -1)

                elif self.active_node != self.root:
                    self.active_node = self.active_node.suffix_link
                # Jeśli active_node == self.root i active_length == 0, AP pozostaje w korzeniu.

    def _collect_leaf_ids_dfs(self, node: Node, results: list[int]):
        """Pomocnicza funkcja DFS do zbierania ID liści (pozycji startowych sufiksów)."""
        if node.is_leaf():
            # Upewnij się, że liść ma prawidłowe id (nie -1, chyba że to specjalny przypadek)
            if node.id != -1:
                results.append(node.id)
            # Jeśli liść nie ma dzieci, ale jego id to -1, to jest to problem w konstrukcji
            # lub jest to węzeł wewnętrzny, który przypadkowo nie ma dzieci (np. dla "$")
            # Dla "$" liść może mieć ID = N-1 (start ostatniego sufiksu "$")
            # W tej implementacji liście zawsze powinny mieć poprawne suffix_id >= 0.

        for child_node in node.children.values():
            self._collect_leaf_ids_dfs(child_node, results)

    def find_pattern(self, pattern: str) -> list[int]:
        """Znajdź wszystkie wystąpienia wzorca w tekście."""
        if not pattern:
            return []

        current_node = self.root
        pattern_idx = 0

        while pattern_idx < len(pattern):
            char_to_match = pattern[pattern_idx]

            if char_to_match not in current_node.children:
                return []  # Wzorzec nie znaleziony

            edge_node = current_node.children[char_to_match]
            edge_len = edge_node.edge_length(self.global_end)  # Użyj global_end z końca budowy
            # lub self.N -1 jeśli $ jest ostatni

            # Sprawdź znaki na krawędzi
            for i in range(edge_len):
                if pattern_idx >= len(pattern):  # Wzorzec się skończył na tej krawędzi
                    break

                text_char_on_edge = self.text[edge_node.start + i]
                pattern_char = pattern[pattern_idx]

                if text_char_on_edge != pattern_char:
                    return []  # Niedopasowanie na krawędzi

                pattern_idx += 1

            if pattern_idx == len(pattern):  # Cały wzorzec dopasowany
                # Wzorzec kończy się w węźle edge_node lub na krawędzi do niego prowadzącej
                # Jeśli pattern_idx < len(pattern) po pętli for, to znaczy, że skończył się na krawędzi
                # ale nasza logika pętli while i for obsłużyła to jako "cały wzorzec dopasowany"
                # gdy pattern_idx osiągnie len(pattern)

                # Zbierz wszystkie ID liści z poddrzewa zaczynającego się w edge_node
                occurrences = []
                self._collect_leaf_ids_dfs(edge_node, occurrences)
                return sorted(list(set(occurrences)))  # Unikalne i posortowane

            # Jeśli wzorzec się nie skończył, a krawędź tak, przejdź do następnego węzła
            current_node = edge_node

        return []  # Teoretycznie nie powinno się tu dojść, jeśli pattern_idx == len(pattern)
        # chyba że pattern jest pusty (obsłużone na początku)

    def print_tree_recursive(self, node, indent="", edge_label_prefix=""):
        """Pomocnicza funkcja do wizualizacji drzewa."""
        label = ""
        if node.start != -1:  # Nie dla korzenia
            _end = self.global_end if node.end == SuffixTree.OPEN_EDGE_END else node.end
            label = self.text[node.start: _end + 1]

        suffix_id_str = f" (sid:{node.id})" if node.id != -1 else ""
        sl_str = f" [sl->{node.suffix_link.debug_id if node.suffix_link else 'None'}]" if node != self.root else ""

        print(f"{indent}{edge_label_prefix}'{label}' (node_id:{node.debug_id}){suffix_id_str}{sl_str}")

        for char_key, child_node in sorted(node.children.items()):
            self.print_tree_recursive(child_node, indent + "  ", f"{char_key} -> ")

    def print_tree(self):
        print("Suffix Tree:")
        self.print_tree_recursive(self.root)