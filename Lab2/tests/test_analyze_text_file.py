import os

from Lab2.analyze_text_file import analyze_text_file

TEST_FILE_PATH = os.path.join(os.path.dirname(__file__), "test_file.md")


class TestAnalyzeTextFile:
    def test_file_exists(self):
        assert os.path.isfile(
            TEST_FILE_PATH
        ), f"Test file not found at {TEST_FILE_PATH}"

    def test_analyze_text_file(self):
        result = analyze_text_file(TEST_FILE_PATH)

        assert isinstance(result, dict)
        expected_keys = [
            "word_count",
            "sentence_count",
            "emails",
            "frequent_words",
            "dates",
            "paragraph_sizes",
        ]
        for key in expected_keys:
            assert key in result, f"Expected key '{key}' missing from result"

    def test_word_count(self):
        result = analyze_text_file(TEST_FILE_PATH)
        assert result["word_count"] > 300, "Word count is suspiciously low"

    def test_sentence_count(self):
        result = analyze_text_file(TEST_FILE_PATH)
        assert result["sentence_count"] >= 20, "Sentence count is suspiciously low"

    def test_email_extraction(self):
        result = analyze_text_file(TEST_FILE_PATH)

        expected_emails = [
            "jane.smith@university.edu",
            "research.team@nlp-studies.org",
            "history@text-algorithms.com",
            "archives@cs-history.org",
            "regex.help@programming-resources.net",
            "performance@algorithm-testing.org",
            "support@regex-benchmarks.com",
            "dates@formatting-tools.net",
            "developers@text-processing-examples.org",
        ]

        for email in expected_emails:
            assert email in result["emails"], f"Expected email '{email}' not found"

        example_emails = [
            "user@domain.com",
            "name@sub.domain.org",
            "first.last+tag@company-name.co.uk",
        ]

        found_examples = [
            email for email in example_emails if email in result["emails"]
        ]
        assert len(found_examples) > 0, "None of the example emails were found"

        assert len(result["emails"]) >= len(
            expected_emails
        ), "Not enough emails were found"

    def test_date_extraction(self):
        result = analyze_text_file(TEST_FILE_PATH)

        expected_dates = [
            "2023-09-15",
            "15.03.2023",
            "01/05/2022",
            "12/31/2022",
            "10/15/1968",
            "2023-04-30",
            "11-22-2023",
        ]

        found_date_count = 0
        for expected_date in expected_dates:
            found = False
            for extracted_date in result["dates"]:
                if (
                    expected_date in extracted_date
                    or expected_date.replace("/", "-") in extracted_date
                ):
                    found = True
                    found_date_count += 1
                    break
            assert found, f"Expected date '{expected_date}' or similar not found"

        text_date_formats = ["May 23, 1977", "January 5, 2024", "September 15, 2023"]
        found_text_dates = False

        for extracted_date in result["dates"]:
            for _ in text_date_formats:
                if any(
                    month in extracted_date for month in ["May", "January", "September"]
                ):
                    found_text_dates = True
                    break
            if found_text_dates:
                break

        assert found_text_dates, "No text-format dates were found"

        assert len(result["dates"]) >= 10, "Not enough dates were found"

    def test_frequent_words(self):
        result = analyze_text_file(TEST_FILE_PATH)

        likely_frequent_words = [
            "text",
            "processing",
            "regex",
            "pattern",
            "algorithm",
            "format",
        ]

        found_count = 0
        for word in likely_frequent_words:
            for result_word in result["frequent_words"].keys():
                if word in result_word:
                    found_count += 1
                    break

        assert found_count >= 3, "Expected frequent words not found in results"

        for word, count in result["frequent_words"].items():
            assert (
                count > 1
            ), f"Frequent word '{word}' has suspiciously low count: {count}"

    def test_paragraph_sizes(self):
        result = analyze_text_file(TEST_FILE_PATH)

        assert len(result["paragraph_sizes"]) >= 10, "Not enough paragraphs detected"

        for para_num, size in result["paragraph_sizes"].items():
            assert size > 0, f"Paragraph {para_num} has size 0, which is unlikely"

        total_words_in_paras = sum(result["paragraph_sizes"].values())
        assert (
            0.9 <= total_words_in_paras / result["word_count"] <= 1.1
        ), "Total words in paragraphs doesn't match overall word count"
