# src/features/preprocessing.py

import re
from html.parser import HTMLParser


class _HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []

    def handle_data(self, data):
        self._parts.append(data.strip())

    def get_text(self):
        return " ".join(p for p in self._parts if p.strip())


def clean_text(text: str | None) -> str:
    if text is None or not str(text).strip():
        return ""
    stripper = _HTMLStripper()
    stripper.feed(str(text))
    text = stripper.get_text()

    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 10000:
        text = text[:10000]

    return text
