from Lab2.parse_publication import parse_publication


class TestPublicationParsing:
    def test_basic_publication(self):
        reference = (
            "Kowalski, J., Nowak, A. (2023). Analiza algorytmów tekstowych. Journal of Computer Science, "
            "45(2), 123-145."
        )
        result = parse_publication(reference)

        assert result["authors"] == [
            {"last_name": "Kowalski", "initial": "J"},
            {"last_name": "Nowak", "initial": "A"},
        ]
        assert result["year"] == 2023
        assert result["title"] == "Analiza algorytmów tekstowych"
        assert result["journal"] == "Journal of Computer Science"
        assert result["volume"] == 45
        assert result["issue"] == 2
        assert result["pages"] == {"start": 123, "end": 145}

    def test_single_author(self):
        reference = "Kowalski, J. (2021). Podstawy wyrażeń regularnych. Computer Science Review, 30, 45-67."
        result = parse_publication(reference)

        assert result["authors"] == [{"last_name": "Kowalski", "initial": "J"}]
        assert result["year"] == 2021
        assert result["title"] == "Podstawy wyrażeń regularnych"
        assert result["journal"] == "Computer Science Review"
        assert result["volume"] == 30
        assert result["issue"] is None
        assert result["pages"] == {"start": 45, "end": 67}

    def test_three_authors(self):
        reference = (
            "Kowalski, J., Nowak, A., Wiśniewski, P. (2022). Analiza wydajności algorytmów. Journal of "
            "Algorithms, 15(3), 201-225."
        )
        result = parse_publication(reference)

        assert len(result["authors"]) == 3
        assert result["authors"][0] == {"last_name": "Kowalski", "initial": "J"}
        assert result["authors"][1] == {"last_name": "Nowak", "initial": "A"}
        assert result["authors"][2] == {"last_name": "Wiśniewski", "initial": "P"}

    def test_invalid_references(self):
        assert parse_publication("Niepoprawna referencja") is None
        assert parse_publication("") is None
