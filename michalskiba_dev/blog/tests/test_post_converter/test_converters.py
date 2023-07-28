from unittest.mock import patch

import pytest

from blog.post_converter.converters import (
    HTMLBold,
    HTMLHeader,
    HTMLImage,
    HTMLItalic,
    HTMLLink,
    HTMLOrderedList,
    HTMLParagraph,
    HTMLTableOfContents,
    HTMLUnorderedList,
    ListLowercase,
    ListStrip,
    ListTrim,
    MultipleChars,
    Remove,
    Replace,
    Strip,
    Trim,
)


class TestReplace:
    def test_apply(self) -> None:
        converter = Replace(old="\n", new=" ")

        converted_text = converter.apply("\n\nline1\n\nline2\n\n\n\nline3\n\n")

        assert converted_text == "  line1  line2    line3  "


class TestStrip:
    def test_apply(self) -> None:
        converter = Strip(strip_char=" ")

        converted_text = converter.apply("  line1  line2    line3  ")

        assert converted_text == "line1  line2    line3"


class TestListStrip:
    def test_apply(self) -> None:
        converter = ListStrip(strip_char=" ", split_char="\n")

        converted_text = converter.apply("line1 \nline2    \nline3  \n\n")

        assert converted_text == "line1\nline2\nline3"


class TestMultipleChars:
    def test_apply_for_space(self) -> None:
        converter = MultipleChars()

        converted_text = converter.apply("line1  line2    line3")

        assert converted_text == "line1 line2 line3"

    def test_apply_for_new_line(self) -> None:
        converter = MultipleChars(char="\n")

        converted_text = converter.apply("line1\n\nline2\n\n\n\nline3")

        assert converted_text == "line1\nline2\nline3"


class TestTrim:
    def test_apply(self) -> None:
        converter = Trim(max_length=5)

        converted_text = converter.apply("line1  line2    line3")

        assert converted_text == "line1"


class TestListTrim:
    def test_apply(self) -> None:
        converter = ListTrim(max_length=4, split_char=",")

        converted_text = converter.apply("Line1,Line2,Line3")

        assert converted_text == "Line,Line,Line"


class TestListLowercase:
    def test_apply(self) -> None:
        converter = ListLowercase(split_char=",")

        converted_text = converter.apply("Line,Line,Line")

        assert converted_text == "line,line,line"


class TestRemove:
    def test_apply(self) -> None:
        converter = Remove(remove_char=" ")

        converted_text = converter.apply("Tag1, Tag2, Tag3")

        assert converted_text == "Tag1,Tag2,Tag3"


class TestHTMLHeader:
    def test_apply(self) -> None:
        converter = HTMLHeader(split_char="\n")

        converted_text = converter.apply("# H1\n##   H1.1  \n# H2")

        assert converted_text == "<h2>H1</h2>\n<h3>H1.1</h3>\n<h2>H2</h2>"


class TestHTMLUnorderedList:
    def test_apply_when_between_text(self) -> None:
        converter = HTMLUnorderedList(split_char="\n")

        converted_text = converter.apply(
            "text 1 \n- item 1\n  - item 1.1  \n  - item 1.2\n- item 2\ntext 2 "
        )

        assert converted_text == (
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

    def test_apply_when_between_text_with_multiple_closure(self) -> None:
        converter = HTMLUnorderedList(split_char="\n")

        converted_text = converter.apply(
            "text 1 \n- item 1\n  - item 1.1 \n    - item 1.1.1\ntext 2 "
        )

        assert converted_text == (
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

    def test_apply_when_after_text(self) -> None:
        converter = HTMLUnorderedList(split_char="\n")

        converted_text = converter.apply(
            "text 1 \n- item 1 \n  - item 1.1  \n  - item 1.2\n- item 2"
        )

        assert converted_text == (
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

    def test_apply_when_after_text_with_multiple_closure(self) -> None:
        converter = HTMLUnorderedList(split_char="\n")

        converted_text = converter.apply("text 1 \n- item 1  \n  - item 1.1\n    - item 1.1.1")

        assert converted_text == (
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

    def test_apply_with_multiple_closure_in_the_middle(self) -> None:
        converter = HTMLUnorderedList(split_char="\n")

        converted_text = converter.apply("- item 1\n  - item 1.1\n    - item 1.1.1\n- item 2")

        assert converted_text == (
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


class TestHTMLOrderedList:
    def test_apply_when_between_text(self) -> None:
        converter = HTMLOrderedList(split_char="\n")

        converted_text = converter.apply("text 1 \n1. item 1\n2. item 2  \n3. item 3 \ntext 2 ")

        assert converted_text == (
            "text 1 \n"
            "<ol>\n"
            "<li>item 1</li>\n"
            "<li>item 2</li>\n"
            "<li>item 3</li>\n"
            "</ol>\n"
            "text 2 "
        )

    def test_apply_for_multiple_lists_between_text(self) -> None:
        converter = HTMLOrderedList(split_char="\n")

        converted_text = converter.apply(
            "text 1 \n1. item 1\n2. item 2  \n3. item 3 \ntext 2 \n"
            "1. item a\n2. item b\ntext 3 "
        )

        assert converted_text == (
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

    def test_apply_when_after_text(self) -> None:
        converter = HTMLOrderedList(split_char="\n")

        converted_text = converter.apply("text 1 \n1. item 1\n2. item 2  \n3. item 3 ")

        assert converted_text == (
            "text 1 \n"
            "<ol>\n"
            "<li>item 1</li>\n"
            "<li>item 2</li>\n"
            "<li>item 3</li>\n"
            "</ol>"
        )

    def test_apply_with_two_lists_next_to_each_other(self) -> None:
        converter = HTMLOrderedList(split_char="\n")

        converted_text = converter.apply("1.   item 1\n2. item 2  \n1. item a\n2. item b  ")

        assert converted_text == (
            "<ol>\n"
            "<li>item 1</li>\n"
            "<li>item 2</li>\n"
            "</ol>\n"
            "<ol>\n"
            "<li>item a</li>\n"
            "<li>item b</li>\n"
            "</ol>"
        )


@patch("blog.post_converter.converters.static", lambda path: f"/static/{path}")
class TestHTMLImage:
    def test_apply(self) -> None:
        converter = HTMLImage()

        converted_text = converter.apply(
            "dummy\n![alternative_text](../images/relative_path.jpg)\ndummy"
        )

        assert converted_text == (
            'dummy\n<img class="img-fluid post-img" src="/static/blog/images/relative_path.jpg" '
            'alt="alternative_text">\ndummy'
        )

    def test_apply_multiple_with_alternative_text_with_spaces(self) -> None:
        converter = HTMLImage()

        converted_text = converter.apply(
            "dummy\n![alternative text 1](../images/relative_path_1.jpg)\n"
            "dummy\n![alternative text 2](../images/relative_path_2.jpg)\ndummy"
        )

        assert converted_text == (
            'dummy\n<img class="img-fluid post-img" src="/static/blog/images/relative_path_1.jpg" '
            'alt="alternative text 1">\n'
            'dummy\n<img class="img-fluid post-img" src="/static/blog/images/relative_path_2.jpg" '
            'alt="alternative text 2">\ndummy'
        )

    def test_apply_multiple_with_alternative_text_with_spaces_in_one_line(self) -> None:
        converter = HTMLImage()

        converted_text = converter.apply(
            "![alternative text 1](../images/relative_path_1.jpg)"
            "![alternative text 2](../images/relative_path_2.jpg)"
        )

        assert converted_text == (
            '<img class="img-fluid post-img" src="/static/blog/images/relative_path_1.jpg" '
            'alt="alternative text 1">'
            '<img class="img-fluid post-img" src="/static/blog/images/relative_path_2.jpg" '
            'alt="alternative text 2">'
        )


class TestHTMLParagraph:
    def test_apply(self) -> None:
        converter = HTMLParagraph()

        converted_text = converter.apply(
            "<h1>Header</h1>\n"
            " some text   \n"
            "continuing with text \n"
            "still continuing\n"
            "<h2>bla bla</h2>"
        )

        assert converted_text == (
            "<h1>Header</h1>\n"
            "<p>some text continuing with text still continuing</p>\n"
            "<h2>bla bla</h2>"
        )

    def test_apply_when_at_the_end(self) -> None:
        converter = HTMLParagraph()

        converted_text = converter.apply(
            "<h1>Header</h1>\n" " some text   \n" "continuing with text \n" "still continuing"
        )

        assert converted_text == (
            "<h1>Header</h1>\n" "<p>some text continuing with text still continuing</p>"
        )


class TestHTMLLink:
    def test_apply(self) -> None:
        converter = HTMLLink()

        converted_text = converter.apply(
            "[link 1](https://www.google.com/) dummy [link 2](facebook.com) dummy"
        )

        assert converted_text == (
            '<a class="link" target="_blank" href="https://www.google.com/">link 1</a> '
            'dummy <a class="link" target="_blank" href="facebook.com">link 2</a> dummy'
        )

    @pytest.mark.parametrize(
        "text",
        (
            "![alternative text 1](../images/relative_path_1.jpg)",
            "dummy ![alternative text 1](../images/relative_path_1.jpg)",
        ),
    )
    def test_apply_do_nothing_for_markdown_image(self, text: str) -> None:
        converter = HTMLLink()

        converted_text = converter.apply(text)

        assert converted_text == text


class TestBold:
    def test_apply(self) -> None:
        converter = HTMLBold()

        converted_text = converter.apply("dummy ***bold 1** dummy **bold 2** dummy")

        assert converted_text == "dummy *<b>bold 1</b> dummy <b>bold 2</b> dummy"


class TestHTMLItalic:
    def test_apply(self) -> None:
        converter = HTMLItalic()

        converted_text = converter.apply("dummy ***italic 1* dummy *italic 2* dummy")

        assert converted_text == "dummy **<i>italic 1</i> dummy <i>italic 2</i> dummy"


class TestHTMLTableOfContents:
    def test_apply(self) -> None:
        converter = HTMLTableOfContents()

        converted_text = converter.apply(
            "<h2>Section 1</h2>\n"
            "<p>section 1 text</p>\n"
            "<h2>Section 2</h2>\n"
            "<p>section 2 text</p>\n"
            "<p>Some other text</p>"
        )

        assert converted_text == (
            '<div class="toc_container">\n'
            '<p class="toc_title">Table of Contents</p>\n'
            '<ol class="toc_list">\n'
            '<li><a class="link" href="#section-1">Section 1</a></li>\n'
            '<li><a class="link" href="#section-2">Section 2</a></li>\n'
            "</ol>\n"
            "</div>\n"
            '<h2 id="section-1">Section 1</h2>\n'
            "<p>section 1 text</p>\n"
            '<h2 id="section-2">Section 2</h2>\n'
            "<p>section 2 text</p>\n"
            "<p>Some other text</p>"
        )
