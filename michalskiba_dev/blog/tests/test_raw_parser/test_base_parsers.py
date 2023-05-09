from unittest.mock import patch

import pytest

from blog.raw_parser.base_parsers import (
    HTMLBoldParser,
    HTMLHeaderParser,
    HTMLImageParser,
    HTMLItalicParser,
    HTMLLinkParser,
    HTMLOrderedListParser,
    HTMLParagraphParser,
    HTMLUnorderedListParser,
    ListLowercaseParser,
    ListStripParser,
    ListTrimParser,
    MultipleCharsParser,
    RemoveParser,
    ReplaceParser,
    StripParser,
    TrimParser,
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


class TestListStripParser:
    def test_parse(self) -> None:
        parser = ListStripParser(strip_char=" ", split_char="\n")

        parsed_text = parser.parse("line1 \nline2    \nline3  \n\n")

        assert parsed_text == "line1\nline2\nline3"


class TestMultipleCharsParser:
    def test_parse_for_space(self) -> None:
        parser = MultipleCharsParser()

        parsed_text = parser.parse("line1  line2    line3")

        assert parsed_text == "line1 line2 line3"

    def test_parse_for_new_line(self) -> None:
        parser = MultipleCharsParser(char="\n")

        parsed_text = parser.parse("line1\n\nline2\n\n\n\nline3")

        assert parsed_text == "line1\nline2\nline3"


class TestTrimParser:
    def test_parse(self) -> None:
        parser = TrimParser(max_length=5)

        parsed_text = parser.parse("line1  line2    line3")

        assert parsed_text == "line1"


class TestListTrimParser:
    def test_parse(self) -> None:
        parser = ListTrimParser(max_length=4, split_char=",")

        parsed_text = parser.parse("Line1,Line2,Line3")

        assert parsed_text == "Line,Line,Line"


class TestListLowercaseParser:
    def test_parse(self) -> None:
        parser = ListLowercaseParser(split_char=",")

        parsed_text = parser.parse("Line,Line,Line")

        assert parsed_text == "line,line,line"


class TestRemoveParser:
    def test_parse(self) -> None:
        parser = RemoveParser(remove_char=" ")

        parsed_text = parser.parse("Tag1, Tag2, Tag3")

        assert parsed_text == "Tag1,Tag2,Tag3"


class TestHTMLHeaderParser:
    def test_parse(self) -> None:
        parser = HTMLHeaderParser(split_char="\n")

        parsed_text = parser.parse("# H1\n##   H1.1  \n# H2")

        assert parsed_text == "<h2>H1</h2>\n<h3>H1.1</h3>\n<h2>H2</h2>"


class TestHTMLUnorderedListParser:
    def test_parse_when_between_text(self) -> None:
        parser = HTMLUnorderedListParser(split_char="\n")

        parsed_text = parser.parse(
            "text 1 \n- item 1\n  - item 1.1  \n  - item 1.2\n- item 2\ntext 2 "
        )

        assert parsed_text == (
            "text 1 \n"
            "<ul>\n"
            "<li>item 1</li>\n"
            "<ul>\n"
            "<li>item 1.1</li>\n"
            "<li>item 1.2</li>\n"
            "</ul>\n"
            "<li>item 2</li>\n"
            "</ul>\n"
            "text 2 "
        )

    def test_parse_when_between_text_with_multiple_closure(self) -> None:
        parser = HTMLUnorderedListParser(split_char="\n")

        parsed_text = parser.parse("text 1 \n- item 1\n  - item 1.1 \n    - item 1.1.1\ntext 2 ")

        assert parsed_text == (
            "text 1 \n"
            "<ul>\n"
            "<li>item 1</li>\n"
            "<ul>\n"
            "<li>item 1.1</li>\n"
            "<ul>\n"
            "<li>item 1.1.1</li>\n"
            "</ul>\n"
            "</ul>\n"
            "</ul>\n"
            "text 2 "
        )

    def test_parse_when_after_text(self) -> None:
        parser = HTMLUnorderedListParser(split_char="\n")

        parsed_text = parser.parse("text 1 \n- item 1 \n  - item 1.1  \n  - item 1.2\n- item 2")

        assert parsed_text == (
            "text 1 \n"
            "<ul>\n"
            "<li>item 1</li>\n"
            "<ul>\n"
            "<li>item 1.1</li>\n"
            "<li>item 1.2</li>\n"
            "</ul>\n"
            "<li>item 2</li>\n"
            "</ul>"
        )

    def test_parse_when_after_text_with_multiple_closure(self) -> None:
        parser = HTMLUnorderedListParser(split_char="\n")

        parsed_text = parser.parse("text 1 \n- item 1  \n  - item 1.1\n    - item 1.1.1")

        assert parsed_text == (
            "text 1 \n"
            "<ul>\n"
            "<li>item 1</li>\n"
            "<ul>\n"
            "<li>item 1.1</li>\n"
            "<ul>\n"
            "<li>item 1.1.1</li>\n"
            "</ul>\n"
            "</ul>\n"
            "</ul>"
        )

    def test_parse_with_multiple_closure_in_the_middle(self) -> None:
        parser = HTMLUnorderedListParser(split_char="\n")

        parsed_text = parser.parse("- item 1\n  - item 1.1\n    - item 1.1.1\n- item 2")

        assert parsed_text == (
            "<ul>\n"
            "<li>item 1</li>\n"
            "<ul>\n"
            "<li>item 1.1</li>\n"
            "<ul>\n"
            "<li>item 1.1.1</li>\n"
            "</ul>\n"
            "</ul>\n"
            "<li>item 2</li>\n"
            "</ul>"
        )


class TestHTMLOrderedListParser:
    def test_parse_when_between_text(self) -> None:
        parser = HTMLOrderedListParser(split_char="\n")

        parsed_text = parser.parse("text 1 \n1. item 1\n2. item 2  \n3. item 3 \ntext 2 ")

        assert parsed_text == (
            "text 1 \n"
            "<ol>\n"
            "<li>item 1</li>\n"
            "<li>item 2</li>\n"
            "<li>item 3</li>\n"
            "</ol>\n"
            "text 2 "
        )

    def test_parse_for_multiple_lists_between_text(self) -> None:
        parser = HTMLOrderedListParser(split_char="\n")

        parsed_text = parser.parse(
            "text 1 \n1. item 1\n2. item 2  \n3. item 3 \ntext 2 \n"
            "1. item a\n2. item b\ntext 3 "
        )

        assert parsed_text == (
            "text 1 \n"
            "<ol>\n"
            "<li>item 1</li>\n"
            "<li>item 2</li>\n"
            "<li>item 3</li>\n"
            "</ol>\n"
            "text 2 \n"
            "<ol>\n"
            "<li>item a</li>\n"
            "<li>item b</li>\n"
            "</ol>\n"
            "text 3 "
        )

    def test_parse_when_after_text(self) -> None:
        parser = HTMLOrderedListParser(split_char="\n")

        parsed_text = parser.parse("text 1 \n1. item 1\n2. item 2  \n3. item 3 ")

        assert parsed_text == (
            "text 1 \n"
            "<ol>\n"
            "<li>item 1</li>\n"
            "<li>item 2</li>\n"
            "<li>item 3</li>\n"
            "</ol>"
        )

    def test_parse_with_two_lists_next_to_each_other(self) -> None:
        parser = HTMLOrderedListParser(split_char="\n")

        parsed_text = parser.parse("1.   item 1\n2. item 2  \n1. item a\n2. item b  ")

        assert parsed_text == (
            "<ol>\n"
            "<li>item 1</li>\n"
            "<li>item 2</li>\n"
            "</ol>\n"
            "<ol>\n"
            "<li>item a</li>\n"
            "<li>item b</li>\n"
            "</ol>"
        )


@patch("blog.raw_parser.base_parsers.static", lambda path: f"/static/{path}")
class TestHTMLImageParser:
    def test_parse(self) -> None:
        parser = HTMLImageParser()

        parsed_text = parser.parse(
            "dummy\n![alternative_text](../images/relative_path.jpg)\ndummy"
        )

        assert parsed_text == (
            'dummy\n<img src="/static/blog/images/relative_path.jpg" '
            'alt="alternative_text">\ndummy'
        )

    def test_parse_multiple_with_alternative_text_with_spaces(self) -> None:
        parser = HTMLImageParser()

        parsed_text = parser.parse(
            "dummy\n![alternative text 1](../images/relative_path_1.jpg)\n"
            "dummy\n![alternative text 2](../images/relative_path_2.jpg)\ndummy"
        )

        assert parsed_text == (
            'dummy\n<img src="/static/blog/images/relative_path_1.jpg" '
            'alt="alternative text 1">\n'
            'dummy\n<img src="/static/blog/images/relative_path_2.jpg" '
            'alt="alternative text 2">\ndummy'
        )

    def test_parse_multiple_with_alternative_text_with_spaces_in_one_line(self) -> None:
        parser = HTMLImageParser()

        parsed_text = parser.parse(
            "![alternative text 1](../images/relative_path_1.jpg)"
            "![alternative text 2](../images/relative_path_2.jpg)"
        )

        assert parsed_text == (
            '<img src="/static/blog/images/relative_path_1.jpg" '
            'alt="alternative text 1">'
            '<img src="/static/blog/images/relative_path_2.jpg" '
            'alt="alternative text 2">'
        )


class TestHTMLParagraphParser:
    def test_parse(self) -> None:
        parser = HTMLParagraphParser()

        parsed_text = parser.parse(
            "<h1>Header</h1>\n"
            " some text   \n"
            "continuing with text \n"
            "still continuing\n"
            "<h2>bla bla</h2>"
        )

        assert parsed_text == (
            "<h1>Header</h1>\n"
            "<p>some text continuing with text still continuing</p>\n"
            "<h2>bla bla</h2>"
        )

    def test_parse_when_at_the_end(self) -> None:
        parser = HTMLParagraphParser()

        parsed_text = parser.parse(
            "<h1>Header</h1>\n" " some text   \n" "continuing with text \n" "still continuing"
        )

        assert parsed_text == (
            "<h1>Header</h1>\n" "<p>some text continuing with text still continuing</p>"
        )


class TestHTMLLinkParser:
    def test_parse(self) -> None:
        parser = HTMLLinkParser()

        parsed_text = parser.parse(
            "[link 1](https://www.google.com/) dummy [link 2](facebook.com) dummy"
        )

        assert parsed_text == (
            '<a href="https://www.google.com/">link 1</a> '
            'dummy <a href="facebook.com">link 2</a> dummy'
        )

    @pytest.mark.parametrize(
        "text",
        (
            "![alternative text 1](../images/relative_path_1.jpg)",
            "dummy ![alternative text 1](../images/relative_path_1.jpg)",
        ),
    )
    def test_parse_do_nothing_for_markdown_image(self, text: str) -> None:
        parser = HTMLLinkParser()

        parsed_text = parser.parse(text)

        assert parsed_text == text


class TestBoldParser:
    def test_parse(self) -> None:
        parser = HTMLBoldParser()

        parsed_text = parser.parse("dummy ***bold 1** dummy **bold 2** dummy")

        assert parsed_text == "dummy *<b>bold 1</b> dummy <b>bold 2</b> dummy"


class TestHTMLItalicParser:
    def test_parse(self) -> None:
        parser = HTMLItalicParser()

        parsed_text = parser.parse("dummy ***italic 1* dummy *italic 2* dummy")

        assert parsed_text == "dummy **<i>italic 1</i> dummy <i>italic 2</i> dummy"
