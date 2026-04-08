# tests/test_preprocessing.py
from src.features.preprocessing import clean_text


def test_handles_null():
    assert clean_text(None) == ""


def test_handles_empty_string():
    assert clean_text("") == ""


def test_lowercases():
    assert clean_text("HELLO SPAM") == "hello spam"


def test_strips_html():
    assert "<" not in clean_text("<html>buy now</html>")


def test_strips_whitespace():
    assert clean_text("  hello   world  ") == "hello world"


def test_handles_very_long_input():
    long_text = "spam " * 10_000
    result = clean_text(long_text)
    assert len(result) <= 10_000
