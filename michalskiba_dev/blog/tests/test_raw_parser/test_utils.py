from pathlib import Path

import pytest

from blog.models import BlogPostRaw
from blog.raw_parser import get_section_text_by_tag


@pytest.mark.django_db
class TestGetSectionTextByTag:
    def test_correct_section_text(self, blog_post_raw: BlogPostRaw) -> None:
        section_text = get_section_text_by_tag(
            file_path=blog_post_raw.absolute_path, tag="content"
        )

        assert section_text == (
            "Blablablabla, I need to display some images "
            "![empty_shelves.jpg](../images/empty_shelves.jpg) "
            "some text "
            "![empty_shelves_grayscale.jpg](../images/empty_shelves_grayscale.png) "
            "some text "
            "![empty_shelves_edges.jpg](../images/empty_shelves_edges.png) "
            "some text "
            "![empty_shelves_erosion.jpg](../images/empty_shelves_erosion.png) "
            "some text "
            "![empty_shelves_dilation.jpg](../images/empty_shelves_dilation.png) "
            "some text"
        )

    def test_empty_section_text_for_not_existing_file(self) -> None:
        section_text = get_section_text_by_tag(file_path=Path("/dummy/path/foo.md"), tag="content")

        assert section_text == ""

    def test_empty_section_text_for_directory(self, test_working_directory: Path) -> None:
        section_text = get_section_text_by_tag(file_path=test_working_directory, tag="content")

        assert section_text == ""
