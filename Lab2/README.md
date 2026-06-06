# Wyrażenia regularne

W tym laboratorium będziesz implementować różne techniki przetwarzania tekstu przy użyciu wyrażeń regularnych i algorytmów formalnych. Dostarczono szkielety kodu, które należy uzupełnić zgodnie z instrukcjami w komentarzach.

### Zadanie 1: Ekstrakcja informacji z publikacji naukowych - `parse_publication` (2 pkt)

Uzupełnij funkcję `parse_publication`, która analizuje referencje publikacji naukowych w formacie:
```
Nazwisko, I., Nazwisko2, I2. (Rok). Tytuł publikacji. Nazwa czasopisma, Tom(Numer), strony.
```

Przykład:
```
Kowalski, J., Nowak, A. (2023). Analiza algorytmów tekstowych. Journal of Computer Science, 45(2), 123-145.
```

Twoje zadanie:
1. Zaimplementuj wzorce wyrażeń regularnych dla różnych części referencji
2. Połącz je w pełny wzorzec do dopasowania całej referencji
3. Wyodrębnij informacje o autorach, roku, tytule, czasopiśmie, tomie, numerze i stronach
4. Zwróć słownik zawierający wszystkie wyodrębnione informacje w określonym formacie

Wynikowa struktura powinna zawierać:
- listę autorów (każdy autor jako słownik `{'last_name': nazwisko, 'initial': inicjał}`)
- rok publikacji (jako liczba całkowita)
- tytuł (jako string)
- czasopismo (jako string)
- tom (jako liczba całkowita)
- numer (jako liczba całkowita lub `None` jeśli nie istnieje)
- zakres stron (jako słownik `{'start': pierwsza_strona, 'end': ostatnia_strona}`)

### Zadanie 2: Analiza linków w kodzie HTML - `extract_links` (2 pkt)

Uzupełnij funkcję `extract_links`, która analizuje fragment kodu HTML i wyodrębnia wszystkie linki (`<a>` tagi).

Twoje zadanie:
1. Zaimplementuj wyrażenie regularne do dopasowania tagów `<a>` i wyodrębnienia potrzebnych atrybutów
2. Użyj `re.finditer` do znalezienia wszystkich wystąpień wzorca
3. Dla każdego znalezionego linku stwórz słownik z odpowiednimi informacjami
4. Zwróć listę wszystkich znalezionych linków

Każdy słownik w wynikowej liście powinien zawierać:
- `url`: adres URL (wartość atrybutu `href`)
- `title`: tytuł linku (wartość atrybutu `title` lub `None` jeśli nie istnieje)
- `text`: tekst wyświetlany jako link (tekst pomiędzy tagami `<a>` i `</a>`)

Przykład:
```python
html = '<div><a href="https://www.agh.edu.pl">AGH</a> <a href="https://www.agh.edu.pl/wydzialy" title="Wydziały">Wydziały AGH</a></div>'
extract_links(html) 
-> [
    {'url': 'https://www.agh.edu.pl', 'text': 'AGH', 'title': None},
    {'url': 'https://www.agh.edu.pl/wydzialy', 'text': 'Wydziały AGH', 'title': 'Wydziały'}
]
```

### Zadanie 3: Analiza pliku tekstowego - `analyze_text_file` (3 pkt)

Uzupełnij funkcję `analyze_text_file`, która analizuje podany plik tekstowy i zwraca różne statystyki i wzorce.

Twoje zadanie:
1. Zaimplementuj wyrażenia regularne do:
   - Wyodrębnienia słów
   - Podziału tekstu na zdania
   - Wykrycia adresów e-mail
   - Wykrycia dat w różnych formatach
   - Podziału tekstu na akapity
2. Oblicz statystyki:
   - Zlicz słowa
   - Zlicz zdania
   - Znajdź najczęściej występujące słowa (z wyłączeniem stop-words)
   - Oblicz rozmiary akapitów (liczba słów)

Funkcja powinna zwracać słownik zawierający:
- `word_count`: całkowitą liczbę słów
- `sentence_count`: liczbę zdań
- `emails`: listę znalezionych adresów e-mail
- `frequent_words`: 10 najczęściej występujących słów (z wyłączeniem słów stopowych)
- `dates`: listę znalezionych dat w różnych formatach
- `paragraph_sizes`: słownik określający liczbę słów w każdym akapicie

### Zadanie 4: Implementacja uproszczonego parsera regexpów `build_dfa` (3 pkt)

Uzupełnij kod implementujący algorytm Brzozowskiego, który konwertuje wyrażenia regularne na deterministyczny automat skończony (DFA).

Twoje zadanie:
1. Zaimplementuj metody `nullable()` dla klas reprezentujących wyrażenia regularne:
   - Określ, czy dane wyrażenie akceptuje pusty ciąg
2. Zaimplementuj metody `derivative(symbol)` dla każdej klasy wyrażeń:
   - Oblicz pochodną Brzozowskiego wyrażenia względem podanego symbolu
3. Uzupełnij funkcję `simplify()` dla różnych typów wyrażeń:
   - Zastosuj reguły upraszczające wyrażenia regularne
4. Zaimplementuj funkcję `build_dfa()`:
   - Użyj algorytmu Brzozowskiego do konstrukcji DFA na podstawie wyrażenia regularnego

Twoja implementacja powinna obsługiwać:
- Symbole literalne (a, b, c, ...)
- Konkatenację wyrażeń (ab)
- Alternatywę wyrażeń (a|b)
- Gwiazdkę Kleene'a (a*)
- Epsilon (ε) - pusty ciąg
- Empty (∅) - pusty język

Wskazówki do implementacji pochodnych Brzozowskiego:
- Dla symbolu: D(a, a) = ε, D(a, b) = ∅
- Dla konkatencji: D(rs, a) = D(r, a)s + δ(r)D(s, a), gdzie δ(r) = ε jeśli r nullable, inaczej ∅
- Dla alternatywy: D(r|s, a) = D(r, a) | D(s, a)
- Dla gwiazdki Kleene'a: D(r*, a) = D(r, a)r*

Wskazówki do implementacji upraszczania (simplify):
- r|∅ = r, ∅|r = r, r|r = r
- r∅ = ∅, ∅r = ∅, rε = r, εr = r
- (r*)* = r*, ε* = ε, ∅* = ε

Przykład użycia (to będzie działać po poprawnej implementacji):
```python
# Wyrażenie regularne: (a|b)*abb
regex = Concatenation(
    Concatenation(
        Concatenation(
            KleeneStar(Alternative(Symbol('a'), Symbol('b'))),
            Symbol('a')
        ),
        Symbol('b')
    ),
    Symbol('b')
)

# Sprawdzenie, czy łańcuch pasuje do wyrażenia
dfa = build_dfa(regex, {'a', 'b'})
assert dfa.accepts("abb") == True
assert dfa.accepts("aabb") == True
assert dfa.accepts("babb") == True
assert dfa.accepts("ab") == False
```