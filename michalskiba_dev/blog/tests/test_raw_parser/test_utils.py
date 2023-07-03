from pathlib import Path

import pytest

from blog.models import BlogPostRaw
from blog.raw_parser.utils import get_section_text_by_tag


@pytest.mark.django_db
class TestGetSectionTextByTag:
    def test_correct_section(self, blog_post_raw: BlogPostRaw) -> None:
        section_text = get_section_text_by_tag(file_path=blog_post_raw.absolute_path, tag="title")

        assert section_text == (
            "Some title title title title title title title title title title title title title "
            "title title title title title title title title title opsie"
        )

    def test_correct_section_without_default_parsers(self, blog_post_raw: BlogPostRaw) -> None:
        section_text = get_section_text_by_tag(
            file_path=blog_post_raw.absolute_path, tag="title", use_default_parsers=False
        )

        assert section_text == (
            "\nSome title title title title title     title title title title title   title title "
            "title title title title title title title title title        title opsie\n\n"
        )

    def test_empty_section_text_for_not_existing_file(self) -> None:
        section_text = get_section_text_by_tag(file_path=Path("/dummy/path/foo.md"), tag="content")

        assert section_text == ""

    def test_empty_section_text_for_directory(self) -> None:
        section_text = get_section_text_by_tag(file_path=Path("/"), tag="content")

        assert section_text == ""
