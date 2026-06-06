from Lab2.extract_links import extract_links


class TestHtmlLinkExtraction:
    def test_basic_links(self):
        html = (
            '<div><a href="https://www.agh.edu.pl">AGH</a> <a href="https://www.agh.edu.pl/wydzialy" '
            'title="Wydziały">Wydziały AGH</a></div>'
        )
        result = extract_links(html)

        assert len(result) == 2
        assert result[0] == {
            "url": "https://www.agh.edu.pl",
            "text": "AGH",
            "title": None,
        }
        assert result[1] == {
            "url": "https://www.agh.edu.pl/wydzialy",
            "text": "Wydziały AGH",
            "title": "Wydziały",
        }

    def test_empty_html(self):
        assert extract_links("") == []
        assert extract_links("<div>Tekst bez linków</div>") == []

    def test_complex_html(self):
        html = """
        <div>
            <p>Odwiedź naszą stronę <a href="https://www.agh.edu.pl" title="Strona główna">AGH</a>.</p>
            <ul>
                <li><a href="https://www.agh.edu.pl/wydzialy">Lista wydziałów</a></li>
                <li><a href="https://www.agh.edu.pl/studenci" title="Informacje dla studentów">Dla studentów</a></li>
            </ul>
        </div>
        """
        result = extract_links(html)

        assert len(result) == 3
        assert result[0]["url"] == "https://www.agh.edu.pl"
        assert result[0]["title"] == "Strona główna"
        assert result[1]["text"] == "Lista wydziałów"
        assert result[2]["title"] == "Informacje dla studentów"
