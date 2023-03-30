import re


class BaseParser:
    def parse(self, text: str) -> str:  # pragma: no cover
        return text


class ReplaceParser(BaseParser):
    def __init__(self, old: str, new: str):
        self._old = old
        self._new = new

    def parse(self, text: str) -> str:
        return text.replace(self._old, self._new)


class StripParser(BaseParser):
    def __init__(self, strip_char: str = " "):
        self._strip_char = strip_char

    def parse(self, text: str) -> str:
        return text.strip(self._strip_char)


class MultipleSpacesParser(BaseParser):
    def parse(self, text: str) -> str:
        result = re.sub(" +", " ", text)
        return str(result)
