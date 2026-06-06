from Lab6.allison import allison_global_alignment, allison_local_alignment


class TestAllisonAlgorithm:
    def test_allison_global_alignment_identical(self):
        s1 = "ACGT"
        s2 = "ACGT"
        score, align1, align2 = allison_global_alignment(s1, s2)
        expected_score = 8  # 4 matches * 2 points each
        assert score == expected_score, f"Oczekiwano wyniku {expected_score}, otrzymano: {score}"
        assert align1 == "ACGT", f"Oczekiwano 'ACGT', otrzymano: {align1}"
        assert align2 == "ACGT", f"Oczekiwano 'ACGT', otrzymano: {align2}"

    def test_allison_global_alignment_with_mismatch(self):
        s1 = "ACGT"
        s2 = "ATGT"
        score, align1, align2 = allison_global_alignment(s1, s2)
        expected_score = 5  # 3 matches (2*3=6) + 1 mismatch (-1) = 5
        assert score == expected_score, f"Oczekiwano wyniku {expected_score}, otrzymano: {score}"
        assert len(align1) == len(align2), "Wyrównania powinny mieć tę samą długość"

    def test_allison_global_alignment_with_gap(self):
        s1 = "ACGT"
        s2 = "ACT"
        score, align1, align2 = allison_global_alignment(s1, s2)
        assert len(align1) == len(align2), "Wyrównania powinny mieć tę samą długość"
        assert "-" in align1 or "-" in align2, "Wyrównanie powinno zawierać lukę"

    def test_allison_global_alignment_empty_strings(self):
        s1 = ""
        s2 = ""
        score, align1, align2 = allison_global_alignment(s1, s2)
        assert score == 0, f"Oczekiwano wyniku 0, otrzymano: {score}"
        assert align1 == "", f"Oczekiwano pustego ciągu, otrzymano: {align1}"
        assert align2 == "", f"Oczekiwano pustego ciągu, otrzymano: {align2}"

    def test_allison_global_alignment_one_empty(self):
        s1 = "ACGT"
        s2 = ""
        score, align1, align2 = allison_global_alignment(s1, s2)
        expected_score = -4  # 4 gaps * -1 each
        assert score == expected_score, f"Oczekiwano wyniku {expected_score}, otrzymano: {score}"
        assert align1 == "ACGT", f"Oczekiwano 'ACGT', otrzymano: {align1}"
        assert align2 == "----", f"Oczekiwano '----', otrzymano: {align2}"

    def test_allison_global_alignment_custom_scores(self):
        s1 = "AC"
        s2 = "AT"
        score, align1, align2 = allison_global_alignment(s1, s2, match_score=3, mismatch_score=-2, gap_penalty=-3)
        expected_score = 1  # 1 match (3) + 1 mismatch (-2) = 1
        assert score == expected_score, f"Oczekiwano wyniku {expected_score}, otrzymano: {score}"

    def test_allison_local_alignment_identical(self):
        s1 = "ACGT"
        s2 = "ACGT"
        score, align1, align2, start1, start2 = allison_local_alignment(s1, s2)
        expected_score = 8  # 4 matches * 2 points each
        assert score == expected_score, f"Oczekiwano wyniku {expected_score}, otrzymano: {score}"
        assert align1 == "ACGT", f"Oczekiwano 'ACGT', otrzymano: {align1}"
        assert align2 == "ACGT", f"Oczekiwano 'ACGT', otrzymano: {align2}"

    def test_allison_local_alignment_with_mismatch(self):
        s1 = "AAACGTAAA"
        s2 = "TTTACGTTTT"
        score, align1, align2, start1, start2 = allison_local_alignment(s1, s2)
        # Powinno znaleźć lokalne dopasowanie dla "ACGT"
        assert score > 0, f"Lokalny wynik powinien być dodatni, otrzymano: {score}"
        assert "ACGT" in align1 or "ACG" in align1, "Wyrównanie powinno zawierać część wspólną"

    def test_allison_local_alignment_no_match(self):
        s1 = "AAAA"
        s2 = "TTTT"
        score, align1, align2, start1, start2 = allison_local_alignment(s1, s2)
        assert score == 0, f"Oczekiwano wyniku 0 dla braku dopasowania, otrzymano: {score}"

    def test_allison_local_alignment_empty_strings(self):
        s1 = ""
        s2 = ""
        score, align1, align2, start1, start2 = allison_local_alignment(s1, s2)
        assert score == 0, f"Oczekiwano wyniku 0, otrzymano: {score}"

    def test_allison_local_alignment_substring_match(self):
        s1 = "GGGACGTGGG"
        s2 = "ACGT"
        score, align1, align2, start1, start2 = allison_local_alignment(s1, s2)
        expected_score = 8  # Perfect match of "ACGT"
        assert score == expected_score, f"Oczekiwano wyniku {expected_score}, otrzymano: {score}"
        assert align1 == "ACGT", f"Oczekiwano 'ACGT', otrzymano: {align1}"
        assert align2 == "ACGT", f"Oczekiwano 'ACGT', otrzymano: {align2}"

    def test_allison_local_alignment_overlapping_sequences(self):
        s1 = "ACGTACGT"
        s2 = "CGTACG"
        score, align1, align2, start1, start2 = allison_local_alignment(s1, s2)
        assert score > 0, f"Lokalny wynik powinien być dodatni, otrzymano: {score}"
        assert len(align1) == len(align2), "Wyrównania powinny mieć tę samą długość"

    def test_allison_local_vs_global_comparison(self):
        s1 = "AAACGTAAA"
        s2 = "TTTACGTTTT"

        global_score, _, _, = allison_global_alignment(s1, s2)
        local_score, _, _, _, _ = allison_local_alignment(s1, s2)

        # Lokalny wynik powinien być lepszy lub równy globalnemu dla tego przypadku
        assert local_score >= global_score, f"Lokalny wynik ({local_score}) powinien być >= globalnego ({global_score})"