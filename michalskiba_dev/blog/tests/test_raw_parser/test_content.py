from pathlib import Path
from typing import Callable
from unittest.mock import patch

import pytest

from blog.models import BlogPost, BlogPostRaw
from blog.raw_parser import get_content_text
from blog.raw_parser.content import get_content_html_text


@pytest.fixture
def expected_content_text() -> str:
    return (
        "#   Section 1\n"
        " Blablablabla, I need to display some images     \n"
        "Dupa  [link 1](https://www.google.com/) dummy [link 2](facebook.com)   \n"
        "![empty shelves](../images/empty_shelves.jpg)   \n"
        "## Section 1.1\n"
        "some text  \n"
        "![empty shelves grayscale](../images/empty_shelves_grayscale.png)\n"
        "## Section 1.2\n"
        "some text *italic 1*  \n"
        "![empty shelves edges](../images/empty_shelves_edges.png)\n"
        "## Section 1.3\n"
        "some text **bold 1**  \n"
        "1. item a\n"
        "2. item b *italic 2*\n"
        "3. item c \n"
        "4. item d\n"
        "# Section 2\n"
        "![empty shelves erosion](../images/empty_shelves_erosion.png)\n"
        "    \n"
        "## Section 2.1\n"
        "some text:\n"
        "- item 1\n"
        "  - item 1.1\n"
        "  - item 1.2\n"
        "    - item 1.2.1\n"
        "    - item 1.2.2\n"
        "      - item 1.2.2.1\n"
        "      - item 1.2.2.2\n"
        "    - item 1.2.3\n"
        "  - item 1.3\n"
        "  - item 1.4 **bold 2**\n"
        "- item 2\n"
        "- item 3\n"
        "  - item 3.1\n"
        "    - item 3.1.1\n"
        "    - item 3.1.2\n"
        "  - item 3.2\n"
        "- item 4\n"
        "  \n"
        "![empty shelves dilation](../images/empty_shelves_dilation.png)\n"
        "  \n"
        "## Section 2.2\n"
        "some text [link 3](https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley)\n"
        "- item 1\n"
        "- item 2\n"
        "  - item 2.1\n"
        "    - item 2.1.1\n"
        "    - item 2.1.2\n"
        "  - item 2.2\n"
        "- item 3"
    )


@pytest.mark.django_db
class TestGetContentText:
    def test_correct_content_text(
        self, blog_post_raw: BlogPostRaw, expected_content_text: str
    ) -> None:
        content_text = get_content_text(file_path=blog_post_raw.absolute_path)

        assert content_text == expected_content_text


@pytest.mark.django_db
@patch("blog.raw_parser.base_parsers.static", lambda path: f"/static/{path}")
class TestGetContextHtmlText:
    def test_correct_html_text(
        self,
        assert_file_content: Callable[[Path, str], None],
        blog_post: BlogPost,
        expected_content_text: str,
    ) -> None:
        content_html_text = get_content_html_text(expected_content_text)

        assert_file_content(blog_post.absolute_path, content_html_text)
