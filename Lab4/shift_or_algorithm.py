def set_nth_bit(n: int) -> int:
    """
    Zwraca maskę bitową z ustawionym n-tym bitem na 1.

    Args:
        n: Pozycja bitu do ustawienia (0-indeksowana)

    Returns:
        Maska bitowa z n-tym bitem ustawionym na 1
    """
    return 1 << n


def nth_bit(m: int, n: int) -> int:
    """
    Zwraca wartość n-tego bitu w masce m.

    Args:
        m: Maska bitowa
        n: Pozycja bitu do odczytania (0-indeksowana)

    Returns:
        Wartość n-tego bitu (0 lub 1)
    """
    return bool(m & set_nth_bit(n))  # konwersja kazdej liczby innej od 0 na true


def make_mask(pattern: str) -> list:
    """
    Tworzy tablicę masek dla algorytmu Shift-Or.

    Args:
        pattern: Wzorzec do wyszukiwania

    Returns:
        Tablica 256 masek, gdzie każda maska odpowiada jednemu znakowi ASCII
    """
    # TODO: Zaimplementuj tworzenie tablicy masek dla algorytmu Shift-Or
    # TODO: Utwórz tablicę z maskami dla wszystkich znaków ASCII
    # TODO: Dla każdego znaku w pattern, ustaw odpowiednie bity w maskach
    # pass
    if not len(pattern): return []

    masks = [~0 for _ in range(256)]  # wszystkie maski na same 1

    for i, char in enumerate(pattern):  masks[ord(char)] &= ~(1 << i)

    return masks


def shift_or(text: str, pattern: str) -> list[int]:
    """
    Implementacja algorytmu Shift-Or do wyszukiwania wzorca.

    Args:
        text: Tekst do przeszukania
        pattern: Wzorzec do wyszukiwania

    Returns:
        Lista pozycji (0-indeksowanych), na których znaleziono wzorzec
    """
    # TODO: Zaimplementuj algorytm Shift-Or
    # TODO: Obsłuż przypadki brzegowe (pusty wzorzec, wzorzec dłuższy niż tekst)
    # TODO: Utwórz maski dla wzorca
    # TODO: Zainicjalizuj stan początkowy
    # TODO: Zaimplementuj główną logikę algorytmu
    # TODO: Wykryj i zapisz pozycje dopasowań

    m = len(pattern)
    n = len(text)

    if m == 0 or m > n: return []
    if m == n: return [0] if text == pattern else []

    result = []
    masks = make_mask(pattern)  # zwracamy maski patternu
    state = ~0  # wszystkie bity ustawiamy na 1
    match_bit = 1 << (
                m - 1)  # Tworzy maskę, która ma ustawiony tylko najbardziej znaczący bit, jesli sie zmieni to znalazlo pattern

    for i in range(n):

        state = (state << 1) | masks[ord(text[i])]  # przeuwamy bit w lewo i patrzymy czy pattern sie zachowuje
        # Sprawdzenie, czy znaleziono dopasowanie
        # jesli najbardziej znaczy bit matcha jest 0 to znalazl dopasowanie w tekscie
        if (state & match_bit) == 0:
            # Jesli najbardziej znaczacy bit w state jest ustawiony na 0 -> dopasowalo sie prefiks o m
            match_pos = i - m + 1

            if match_pos >= 0:  # poczatkowa pozycja jest dodatnia
                if text[match_pos:match_pos + m] == pattern:
                    result.append(match_pos)

    return result

# maski dla znaku  i jesli pojawia sie w tekscie to ustawiamy na 0