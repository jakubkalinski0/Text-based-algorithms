from Lab6.nilsims import (
    NilsimsHash,
    nilsims_similarity,
    find_similar_texts
)


class TestNilsims:
    def test_nilsims_hash_initialization(self):
        nh = NilsimsHash()
        assert nh is not None, "Obiekt NilsimsHash powinien być utworzony"

    def test_nilsims_trigrams_basic(self):
        nh = NilsimsHash()
        text = "abcdef"
        trigrams = nh._trigrams(text)
        expected = ["abc", "bcd", "cde", "def"]
        assert trigrams == expected, f"Oczekiwano: {expected}, otrzymano: {trigrams}"

    def test_nilsims_trigrams_short_text(self):
        nh = NilsimsHash()
        text = "ab"
        trigrams = nh._trigrams(text)
        expected = []
        assert trigrams == expected, f"Oczekiwano: {expected}, otrzymano: {trigrams}"

    def test_nilsims_trigrams_empty_text(self):
        nh = NilsimsHash()
        text = ""
        trigrams = nh._trigrams(text)
        expected = []
        assert trigrams == expected, f"Oczekiwano: {expected}, otrzymano: {trigrams}"

    def test_nilsims_trigrams_exact_length(self):
        nh = NilsimsHash()
        text = "abc"
        trigrams = nh._trigrams(text)
        expected = ["abc"]
        assert trigrams == expected, f"Oczekiwano: {expected}, otrzymano: {trigrams}"

    def test_nilsims_rolling_hash_basic(self):
        nh = NilsimsHash()
        text = "abcd"
        hashes = nh._rolling_hash(text)
        assert len(hashes) == len(text), f"Oczekiwano {len(text)} hashy, otrzymano: {len(hashes)}"
        assert all(isinstance(h, int) for h in hashes), "Wszystkie hashe powinny być liczbami całkowitymi"

    def test_nilsims_rolling_hash_empty(self):
        nh = NilsimsHash()
        text = ""
        hashes = nh._rolling_hash(text)
        expected = []
        assert hashes == expected, f"Oczekiwano: {expected}, otrzymano: {hashes}"

    def test_nilsims_compute_hash_basic(self):
        nh = NilsimsHash()
        text = "To jest przykładowy tekst do testowania"
        hash_value = nh.compute_hash(text)
        assert isinstance(hash_value, bytes), "Hash powinien być typu bytes"
        assert len(hash_value) == 32, f"Hash powinien mieć 32 bajty (256 bitów), otrzymano: {len(hash_value)}"

    def test_nilsims_compute_hash_empty(self):
        nh = NilsimsHash()
        text = ""
        hash_value = nh.compute_hash(text)
        assert isinstance(hash_value, bytes), "Hash powinien być typu bytes"
        assert len(hash_value) == 32, f"Hash powinien mieć 32 bajty, otrzymano: {len(hash_value)}"

    def test_nilsims_compute_hash_consistency(self):
        nh = NilsimsHash()
        text = "consistent text"
        hash1 = nh.compute_hash(text)
        hash2 = nh.compute_hash(text)
        assert hash1 == hash2, "Ten sam tekst powinien dawać ten sam hash"

    def test_nilsims_compute_hash_different_texts(self):
        nh = NilsimsHash()
        text1 = "tekst pierwszy"
        text2 = "tekst drugi"
        hash1 = nh.compute_hash(text1)
        hash2 = nh.compute_hash(text2)
        assert hash1 != hash2, "Różne teksty powinny dawać różne hashe"

    def test_nilsims_compare_hashes_identical(self):
        nh = NilsimsHash()
        text = "identyczny tekst"
        hash1 = nh.compute_hash(text)
        hash2 = nh.compute_hash(text)
        similarity = nh.compare_hashes(hash1, hash2)
        assert similarity == 1.0, f"Identyczne hashe powinny mieć podobieństwo 1.0, otrzymano: {similarity}"

    def test_nilsims_compare_hashes_different(self):
        nh = NilsimsHash()
        hash1 = b'\x00' * 32  # Wszystkie bity = 0
        hash2 = b'\xff' * 32  # Wszystkie bity = 1
        similarity = nh.compare_hashes(hash1, hash2)
        assert similarity == 0.0, f"Całkowicie różne hashe powinny mieć podobieństwo 0.0, otrzymano: {similarity}"

    def test_nilsims_compare_hashes_partial(self):
        nh = NilsimsHash()
        text1 = "To jest przykładowy tekst"
        text2 = "To jest podobny tekst"
        hash1 = nh.compute_hash(text1)
        hash2 = nh.compute_hash(text2)
        similarity = nh.compare_hashes(hash1, hash2)
        assert 0.0 < similarity < 1.0, f"Podobne teksty powinny mieć podobieństwo między 0 a 1, otrzymano: {similarity}"

    def test_nilsims_similarity_function(self):
        text1 = "To jest przykładowy tekst do testowania"
        text2 = "To jest przykładowy tekst dla testów"
        similarity = nilsims_similarity(text1, text2)
        assert 0.0 <= similarity <= 1.0, f"Podobieństwo powinno być w zakresie [0,1], otrzymano: {similarity}"
        assert similarity > 0.5, f"Podobne teksty powinny mieć wysokie podobieństwo, otrzymano: {similarity}"

    def test_nilsims_similarity_identical(self):
        text = "identyczny tekst"
        similarity = nilsims_similarity(text, text)
        assert similarity == 1.0, f"Identyczne teksty powinny mieć podobieństwo 1.0, otrzymano: {similarity}"

    def test_nilsims_similarity_empty_texts(self):
        text1 = ""
        text2 = ""
        similarity = nilsims_similarity(text1, text2)
        assert similarity == 1.0, f"Puste teksty powinny mieć podobieństwo 1.0, otrzymano: {similarity}"

    def test_nilsims_similarity_one_empty(self):
        text1 = "niepusty tekst"
        text2 = ""
        similarity = nilsims_similarity(text1, text2)
        assert 0.0 <= similarity <= 1.0, f"Podobieństwo powinno być w zakresie [0,1], otrzymano: {similarity}"

    def test_find_similar_texts_basic(self):
        target = "To jest tekst docelowy"
        candidates = [
            "To jest tekst podobny",
            "Zupełnie inny tekst",
            "To jest tekst docelowy",
            "Jeszcze jeden podobny tekst"
        ]
        results = find_similar_texts(target, candidates, threshold=0.7)
        assert len(results) >= 1, "Powinno znaleźć przynajmniej jeden podobny tekst"
        assert all(0 <= idx < len(candidates) for idx, _ in results), "Indeksy powinny być prawidłowe"
        assert all(0.7 <= sim <= 1.0 for _, sim in results), "Podobieństwa powinny być powyżej progu"

    def test_find_similar_texts_no_matches(self):
        target = "tekst docelowy"
        candidates = [
            "zupełnie inny",
            "kompletnie odmienny",
            "absolutnie różny"
        ]
        results = find_similar_texts(target, candidates, threshold=0.9)
        # Może nie być żadnych wyników lub bardzo mało
        assert all(0.9 <= sim <= 1.0 for _, sim in results), "Wszystkie wyniki powinny być powyżej progu"

    def test_find_similar_texts_empty_candidates(self):
        target = "tekst docelowy"
        candidates = []
        results = find_similar_texts(target, candidates, threshold=0.5)
        assert results == [], "Pusta lista kandydatów powinna zwrócić pustą listę wyników"

    def test_find_similar_texts_high_threshold(self):
        target = "tekst"
        candidates = ["tekst", "tekst podobny", "inny tekst"]
        results = find_similar_texts(target, candidates, threshold=0.99)
        # Tylko bardzo podobne teksty powinny przejść
        assert all(sim >= 0.99 for _, sim in results), "Wszystkie wyniki powinny być powyżej wysokiego progu"

    def test_find_similar_texts_low_threshold(self):
        target = "tekst"
        candidates = ["tekst", "test", "xxxx"]
        results = find_similar_texts(target, candidates, threshold=0.1)
        # Więcej tekstów powinno przejść przez niski próg
        assert len(results) >= 1, "Niski próg powinien znaleźć więcej wyników"

    def test_nilsims_case_sensitivity(self):
        text1 = "Test Case Sensitivity"
        text2 = "test case sensitivity"
        similarity = nilsims_similarity(text1, text2)
        assert similarity > 0.8, f"Teksty różniące się wielkością liter powinny być podobne, otrzymano: {similarity}"

    def test_nilsims_punctuation_handling(self):
        text1 = "Test, punctuation!"
        text2 = "Test punctuation"
        similarity = nilsims_similarity(text1, text2)
        assert similarity > 0.7, f"Teksty różniące się interpunkcją powinny być podobne, otrzymano: {similarity}"