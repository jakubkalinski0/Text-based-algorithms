def is_palindrome(text: str) -> bool:
    # TODO: Usuń spacje i przekształć tekst na małe litery
    text = ''.join(char for char in text.lower() if not char.isspace())

    # TODO: Sprawdź, czy tekst czytany od przodu jest taki sam jak od tyłu
    # WSKAZÓWKA: Użyj notacji text[::-1] aby odwrócić tekst
    return text == text[::-1]


def make_palindrome(text: str) -> str:
    # Usuwamy spacje i konwertujemy do małych liter
    text = text.lower().replace(" ", "")

    # Sprawdzamy, czy już jest palindromem
    if is_palindrome(text):
        return text

    # TODO: Utwórz palindrom dodając odwrócone znaki na końcu
    # (bez ostatniego znaku, który już jest na początku odwróconego tekstu)
    option1 = text + text[-2::-1]

    # TODO: Utwórz palindrom dodając odwrócone znaki na początku
    # (bez pierwszego znaku, który już jest na końcu oryginalnego tekstu)
    option2 = text[:0:-1] + text

    # TODO: Zwróć krótszą opcję jako wynik
    return option1 if len(option1) < len(option2) else option2


def palindrome_checker() -> None:
    # Pobieranie danych od użytkownika
    text = input("Wprowadź słowo lub frazę: ")

    # TODO: Usuń znaki, które nie są literami ani cyframi, i zamień na małe litery
    # WSKAZÓWKA: Wykorzystaj funkcję isalnum() i list comprehension lub wyrażenie generujące
    clean_text = ''.join([char for char in text.lower() if text.isalnum()])

    # Sprawdzanie, czy to palindrom
    if is_palindrome(clean_text):
        print(f"\"{text}\" jest palindromem!")
    else:
        print(f"\"{text}\" nie jest palindromem.")
        suggested = make_palindrome(clean_text)
        print(f"Sugerowany palindrom: {suggested}")


# Wywołanie funkcji
if __name__ == "__main__":
    palindrome_checker()