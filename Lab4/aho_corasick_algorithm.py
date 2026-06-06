from collections import deque
from typing import List, Tuple, Optional, Dict


class AhoCorasickNode:
    def __init__(self):
        """Inicjalizuje węzeł w drzewie Aho-Corasick."""
        # Przejścia do innych węzłów (słownik: znak -> węzeł)
        self.transitions: Dict[str, 'AhoCorasickNode'] = {}

        # Łącze awaryjne wskazujące na inny węzeł w przypadku niedopasowania
        self.failure_link: Optional['AhoCorasickNode'] = None

        # Lista wzorców kończących się w tym węźle
        self.output: List[str] = []


class AhoCorasick:
    def __init__(self, patterns: List[str]):
        """Inicjalizuje strukturę Aho-Corasick dla podanych wzorców."""
        # Usuwamy puste wzorce
        self.patterns = [p for p in patterns if p]

        # Korzeń drzewa
        self.root = AhoCorasickNode()

        # Budowanie struktury
        self._build_trie()
        self._build_failure_links()

    def _build_trie(self):
        """Builds the trie structure for the given patterns."""
        # Dla każdego wzorca dodajemy go do drzewa
        for pattern in self.patterns:
            current_node = self.root

            # Dodajemy każdy znak wzorca do drzewa
            for char in pattern:
                if char not in current_node.transitions:
                    current_node.transitions[char] = AhoCorasickNode()
                current_node = current_node.transitions[char]

            # Dodajemy wzorzec do listy wyjść dla ostatniego węzła
            current_node.output.append(pattern)

    def _build_failure_links(self):
        """Builds failure links and propagates outputs through them."""
        # Tworzymy kolejkę dla BFS
        queue = deque()

        # Inicjalizacja łączy awaryjnych dla węzłów na głębokości 1
        for char, node in self.root.transitions.items():
            node.failure_link = self.root
            queue.append(node)

        # BFS do ustawienia łączy awaryjnych dla głębszych węzłów
        while queue:
            current_node = queue.popleft()

            # Dla każdego przejścia z bieżącego węzła
            for char, child_node in current_node.transitions.items():
                queue.append(child_node)

                # Ustalamy łącze awaryjne dla dziecka
                failure_node = current_node.failure_link

                # Szukamy węzła, do którego powinniśmy przypisać łącze awaryjne
                while failure_node is not self.root and char not in failure_node.transitions:
                    failure_node = failure_node.failure_link

                # Jeśli znaleźliśmy przejście dla znaku, ustawiamy łącze awaryjne
                # W przeciwnym razie, łącze awaryjne wskazuje na korzeń
                if char in failure_node.transitions:
                    child_node.failure_link = failure_node.transitions[char]
                else:
                    child_node.failure_link = self.root

                # Propagujemy wyjścia przez łącza awaryjne
                child_node.output += child_node.failure_link.output

    def search(self, text: str) -> List[Tuple[int, str]]:
        """
        Searches for all occurrences of patterns in the given text.

        Returns:
            List of tuples (start_index, pattern).
        """
        results = []

        # Jeśli nie ma wzorców, zwróć pustą listę
        if not self.patterns:
            return results

        current_node = self.root

        # Przetwarzamy każdy znak tekstu
        for i, char in enumerate(text):
            # Szukamy odpowiedniego przejścia
            while current_node is not self.root and char not in current_node.transitions:
                current_node = current_node.failure_link

            # Jeśli znaleźliśmy przejście dla znaku, przechodzimy do nowego węzła
            if char in current_node.transitions:
                current_node = current_node.transitions[char]

                # Sprawdzamy, czy w tym węźle kończy się jakiś wzorzec
                for pattern in current_node.output:
                    # Obliczamy pozycję początkową wzorca
                    start_index = i - len(pattern) + 1
                    results.append((start_index, pattern))

        return results