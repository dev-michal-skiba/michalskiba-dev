from blog.raw_parser.base_parsers import (
    MultipleSpacesParser,
    ReplaceParser,
    StripParser,
)


class TestReplaceParser:
    def test_parse(self) -> None:
        parser = ReplaceParser(old="\n", new=" ")

        parsed_text = parser.parse("\n\nline1\n\nline2\n\n\n\nline3\n\n")

        assert parsed_text == "  line1  line2    line3  "


class TestStripParser:
    def test_parse(self) -> None:
        parser = StripParser(strip_char=" ")

        parsed_text = parser.parse("  line1  line2    line3  ")

        assert parsed_text == "line1  line2    line3"


class TestMultipleSpacesParser:
    def test_parse(self) -> None:
        parser = MultipleSpacesParser()

        parsed_text = parser.parse("line1  line2    line3")

        assert parsed_text == "line1 line2 line3"
