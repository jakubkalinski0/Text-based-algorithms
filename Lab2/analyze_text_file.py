import re
from collections import Counter


def analyze_text_file(filename: str) -> dict:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
    except Exception as e:
        return {"error": f"Could not read file: {str(e)}"}

    # Common English stop words to filter out from frequency analysis
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "with",
        "by",
        "about",
        "as",
        "into",
        "like",
        "through",
        "after",
        "over",
        "between",
        "out",
        "of",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "this",
        "that",
        "these",
        "those",
        "it",
        "its",
        "from",
        "there",
        "their",
    }

    # TODO: Implement word extraction using regex
    # Find all words in the content (lowercase for consistency)
    words = re.findall(r'\b\w[\w-]*\b', content.lower())
    word_count = len(words)

    # TODO: Implement sentence splitting using regex
    # A sentence typically ends with ., !, or ? followed by a space
    # Be careful about abbreviations (e.g., "Dr.", "U.S.A.")
    sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
    sentences = re.split(sentence_pattern, content)
    sentence_count = len([s for s in sentences if s.strip()])

    # TODO: Implement email extraction using regex
    # Extract all valid email addresses from the content
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, content)

    # TODO: Calculate word frequencies
    # Count occurrences of each word, excluding stop words and short words
    # Use the Counter class from collections
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2] # dodalem bo jakis losowy test nie dziala
    frequent_words = dict(Counter(filtered_words).most_common(20))

    # TODO: Implement date extraction with multiple formats
    # Detect dates in various formats: YYYY-MM-DD, DD.MM.YYYY, MM/DD/YYYY, etc.
    # Create multiple regex patterns for different date formats
    date_patterns = [
        r'\b\d{4}-\d{2}-\d{2}\b',                     # YYYY-MM-DD
        r'\b\d{2}\.\d{2}\.\d{4}\b',                   # DD.MM.YYYY
        r'\b\d{2}/\d{2}/\d{4}\b',                     # MM/DD/YYYY
        r'\b\d{2}-\d{2}-\d{4}\b',                     # MM-DD-YYYY
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}\b',  # Month DD, YYYY
    ]
    dates = []

    for pattern in date_patterns:
        dates.extend(re.findall(pattern, content))

    # TODO: Analyze paragraphs
    # Split the content into paragraphs and count words in each
    # Paragraphs are typically separated by one or more blank lines
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', content) if p.strip()]
    paragraph_sizes = {i: len(re.findall(r'\b\w+\b', p)) for i, p in enumerate(paragraphs, 1)}

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "emails": emails,
        "frequent_words": frequent_words,
        "dates": dates,
        "paragraph_sizes": paragraph_sizes,
    }