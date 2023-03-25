from unittest.mock import Mock, patch

from _pytest.logging import LogCaptureFixture
from django.conf import settings
from django.core.management import call_command

OS_WALK: list[tuple[str, list[str], list[str]]] = [
    (f"{settings.BLOG_POSTS_RAW_PATH}/test_root", [], ["test_filename.md"])
]


@patch("blog.management.commands.detect_new_raw_files.os.walk", Mock(return_value=OS_WALK))
@patch("blog.management.commands.detect_new_raw_files.BlogPostRaw.objects.get_or_create")
class TestCommand:
    def test_existing_file(
        self, mock_blog_post_raw_get_or_create: Mock, caplog: LogCaptureFixture
    ) -> None:
        mock_blog_post_raw_get_or_create.return_value = (Mock(pk=1), False)

        call_command("detect_new_raw_files")

        assert caplog.messages == ["Detecting new blog post raw files"]

    def test_not_existing_file(
        self, mock_blog_post_raw_get_or_create: Mock, caplog: LogCaptureFixture
    ) -> None:
        mock_blog_post_raw_get_or_create.return_value = (Mock(pk=1), True)

        call_command("detect_new_raw_files")

        assert caplog.messages == [
            "Detecting new blog post raw files",
            "Blog post raw for test_root/test_filename.md created with pk 1",
        ]
