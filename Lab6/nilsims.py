import hashlib
from typing import List, Tuple


class NilsimsHash:
    """Klasa implementująca algorytm Nilsimsa."""

    def __init__(self):
        """
        Inicjalizuje generator hashy Nilsimsa.
        """
        # Rozmiar okna dla trigramów
        self.window_size = 5
        # Rozmiar hasza w bitach
        self.hash_size = 256
        
    def _trigrams(self, text: str) -> List[str]:
        """
        Wyciąga wszystkie trigramy z tekstu.
        
        Args:
            text: Tekst wejściowy
            
        Returns:
            Lista trigramów
        """
        if len(text) < 3:
            return []
            
        trigrams = []
        for i in range(len(text) - 2):
            trigrams.append(text[i:i+3])
            
        return trigrams
    
    def _rolling_hash(self, text: str) -> List[int]:
        """
        Oblicza rolling hash dla każdego znaku w tekście.
        
        Args:
            text: Tekst wejściowy
            
        Returns:
            Lista wartości hash
        """
        if not text:
            return []
            
        hashes = []
        for i in range(len(text)):
            # Prosty hash dla każdego znaku
            char_hash = hash(text[i]) % self.hash_size
            hashes.append(char_hash)
            
        return hashes
        
    def _get_trigrams(self, text: str) -> List[str]:
        """
        Wyciąga wszystkie trigramy z tekstu (alias dla _trigrams).
        
        Args:
            text: Tekst wejściowy
            
        Returns:
            Lista trigramów
        """
        # Normalizuj tekst - małe litery, usuń nadmiarowe spacje
        normalized_text = ' '.join(text.lower().split())
        return self._trigrams(normalized_text)

    def compute_hash(self, text: str) -> bytes:
        """
        Oblicza hash Nilsimsa dla tekstu.

        Args:
            text: Tekst do zahashowania

        Returns:
            256-bitowy hash jako bytes
        """
        if not text:
            return b'\x00' * 32  # 256 bitów = 32 bajty
            
        # Inicjalizuj akumulator hasza
        hash_accumulator = [0] * self.hash_size
        
        # Pobierz trigramy
        trigrams = self._get_trigrams(text)
        
        if not trigrams:
            return b'\x00' * 32
        
        # Dla każdego trigramu
        for trigram in trigrams:
            # Oblicz hash trigramu
            trigram_hash = hash(trigram) % self.hash_size
            
            # Zaktualizuj odpowiedni bit w akumulatorze
            bit_position = trigram_hash % self.hash_size
            hash_accumulator[bit_position] += 1
        
        # Konwertuj akumulator na binarny hash
        # Jeśli licznik > średnia, ustaw bit na 1
        total_count = sum(hash_accumulator)
        if total_count == 0:
            return b'\x00' * 32
            
        average = total_count / len(hash_accumulator)
        
        binary_hash = []
        for count in hash_accumulator:
            binary_hash.append(1 if count > average else 0)
        
        # Konwertuj listę bitów na bytes
        hash_bytes = bytearray()
        for i in range(0, len(binary_hash), 8):
            byte_value = 0
            for j in range(8):
                if i + j < len(binary_hash):
                    byte_value |= (binary_hash[i + j] << (7 - j))
            hash_bytes.append(byte_value)
            
        return bytes(hash_bytes)

    def compare_hashes(self, hash1: bytes, hash2: bytes) -> float:
        """
        Porównuje dwa hashe Nilsimsa i zwraca stopień podobieństwa.

        Args:
            hash1: Pierwszy hash
            hash2: Drugi hash

        Returns:
            Stopień podobieństwa w zakresie [0, 1]
        """
        if len(hash1) != len(hash2):
            return 0.0
            
        # Oblicz odległość Hamminga (liczba różnych bitów)
        hamming_distance = 0
        total_bits = len(hash1) * 8
        
        for b1, b2 in zip(hash1, hash2):
            # XOR i policz bity
            xor_result = b1 ^ b2
            hamming_distance += bin(xor_result).count('1')
        
        # Konwertuj na podobieństwo (1.0 = identyczne, 0.0 = całkowicie różne)
        similarity = 1.0 - (hamming_distance / total_bits)
        return similarity


def nilsims_similarity(text1: str, text2: str) -> float:
    """
    Oblicza podobieństwo między dwoma tekstami używając algorytmu Nilsimsa.

    Args:
        text1: Pierwszy tekst
        text2: Drugi tekst

    Returns:
        Stopień podobieństwa w zakresie [0, 1]
    """
    nilsims = NilsimsHash()
    
    # Oblicz hashe dla obu tekstów
    hash1 = nilsims.compute_hash(text1)
    hash2 = nilsims.compute_hash(text2)
    
    # Porównaj hashe
    return nilsims.compare_hashes(hash1, hash2)


def find_similar_texts(target: str, candidates: List[str], threshold: float = 0.7) -> List[Tuple[int, float]]:
    """
    Znajduje teksty podobne do tekstu docelowego.

    Args:
        target: Tekst docelowy
        candidates: Lista kandydatów
        threshold: Próg podobieństwa

    Returns:
        Lista krotek (indeks, podobieństwo) dla tekstów powyżej progu
    """
    if not candidates:
        return []
        
    nilsims = NilsimsHash()
    target_hash = nilsims.compute_hash(target)
    
    similar_texts = []
    
    for i, candidate in enumerate(candidates):
        candidate_hash = nilsims.compute_hash(candidate)
        similarity = nilsims.compare_hashes(target_hash, candidate_hash)
        
        if similarity >= threshold:
            similar_texts.append((i, similarity))
    
    # Sortuj według podobieństwa (malejąco)
    similar_texts.sort(key=lambda x: x[1], reverse=True)
    
    return similar_texts