import pytest

from blog.models import BlogPostRaw
from blog.raw_parser import get_title_text


@pytest.mark.django_db
class TestGetTitleText:
    def test_correct_title_text(self, blog_post_raw: BlogPostRaw) -> None:
        title_text = get_title_text(file_path=blog_post_raw.absolute_path)

        assert title_text == (
            "Some title title title title title title title title title title title title title "
            "title title title title title title title tit"
        )
