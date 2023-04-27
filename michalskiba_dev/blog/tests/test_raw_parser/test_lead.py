import pytest

from blog.models import BlogPostRaw
from blog.raw_parser import get_lead_text


@pytest.mark.django_db
class TestGetLeadText:
    def test_correct_lead_text(self, blog_post_raw: BlogPostRaw) -> None:
        lead_text = get_lead_text(file_path=blog_post_raw.absolute_path)

        assert lead_text == "Some xy" + 101 * " lead"
