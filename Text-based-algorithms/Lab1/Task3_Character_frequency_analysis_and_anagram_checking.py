def character_frequency(text: str) -> dict:
    char_frequency = {}

    for char in text:
        char_frequency[char] = char_frequency.get(char, 0) + 1

    return char_frequency

def display_by_decreasing_popularity(char_frequency: dict) -> None:

    for char, occurrences in sorted(char_frequency.items(), key=lambda item: item[1], reverse=True):
        print(char, occurrences, sep="; ")

def anagram_checking() -> bool:
    # Pobieranie danych od użytkownika
    text = input("Wprowadź słowo lub frazę: ").replace(" ", "").lower()

    char_frequency = character_frequency(text)

    display_by_decreasing_popularity(char_frequency)

    text2 = input("Wprowadź słowo lub frazę, by sprawdzić czy poprzedni tekst jest jego anagramem: ").replace(" ", "").lower()

    if len(text) != len(text2):
        return False

    return char_frequency == character_frequency(text2)


# Wywołanie funkcji
if __name__ == "__main__":
    print(anagram_checking())