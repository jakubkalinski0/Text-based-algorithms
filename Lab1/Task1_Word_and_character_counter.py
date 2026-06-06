def text_counter() -> None:
    # Pobieranie danych od użytkownika
    text = input("Wprowadź tekst do analizy: ")

    # Obliczenia
    # TODO: Oblicz liczbę wszystkich znaków w tekście
    char_count = len(text)

    # TODO: Oblicz liczbę znaków bez spacji
    char_count_no_spaces = len(text.replace(" ", ""))

    # TODO: Podziel tekst na słowa i oblicz ich liczbę
    words = text.split()
    word_count = len(words)

    # Liczenie samogłosek i spółgłosek
    vowels = "aeiouAEIOUąęióóyĄĘIÓÓY"
    consonants = "bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZćłńśźżĆŁŃŚŹŻ"

    # TODO: Zlicz samogłoski w tekście
    vowel_count = sum(1 for character in text if character in vowels)

    # TODO: Zlicz spółgłoski w tekście
    consonant_count = sum(1 for character in text if character in consonants)

    # Wyświetlanie wyników
    print(f"\nAnaliza tekstu: \"{text}\"")
    print(f"Liczba słów: {word_count}")
    print(f"Liczba znaków (ze spacjami): {char_count}")
    print(f"Liczba znaków (bez spacji): {char_count_no_spaces}")
    print(f"Liczba samogłosek: {vowel_count}")
    print(f"Liczba spółgłosek: {consonant_count}")


# Wywołanie funkcji
if __name__ == "__main__":
    text_counter()