from pathlib import Path
from unittest.mock import Mock, call, patch

import pytest

from blog.tests.factories import BlogPostRawFactory
from blog.utils import (
    extract_images_absolute_paths_from_markdown_file,
    get_content_string_from_markdown_file,
    remove_files,
)


@pytest.mark.django_db
class TestExtractImagesFromMarkdownFile:
    def test_images_extracted_correctly(
        self, blog_post_raw: BlogPostRawFactory, test_working_directory: Path
    ) -> None:
        images_absolute_paths = extract_images_absolute_paths_from_markdown_file(
            blog_post_raw.absolute_path
        )

        assert sorted(images_absolute_paths) == sorted(
            [
                test_working_directory / "blog/tests/data/images/empty_shelves.jpg",
                test_working_directory / "blog/tests/data/images/empty_shelves_grayscale.png",
                test_working_directory / "blog/tests/data/images/empty_shelves_edges.png",
                test_working_directory / "blog/tests/data/images/empty_shelves_erosion.png",
                test_working_directory / "blog/tests/data/images/empty_shelves_dilation.png",
            ]
        )


@pytest.mark.django_db
class TestGetContentString:
    def test_correct_content_string(self, blog_post_raw: BlogPostRawFactory) -> None:
        content_string = get_content_string_from_markdown_file(blog_post_raw.absolute_path)

        assert content_string == (
            "Blablablabla, I need to display some images\n"
            "![empty_shelves.jpg](../images/empty_shelves.jpg)\n\n"
            "some text\n\n"
            "![empty_shelves.jpg](../images/empty_shelves_grayscale.png)\n\n"
            "some text\n\n"
            "![empty_shelves.jpg](../images/empty_shelves_edges.png)\n\n"
            "some text\n\n"
            "![empty_shelves.jpg](../images/empty_shelves_erosion.png)\n\n"
            "some text\n\n"
            "![empty_shelves.jpg](../images/empty_shelves_dilation.png)\n\n"
            "some text"
        )

    def test_empty_string_for_not_existing_file(self) -> None:
        content_string = get_content_string_from_markdown_file(Path("/dummy/path/foo.md"))

        assert content_string == ""

    def test_empty_string_for_directory(self, test_working_directory: Path) -> None:
        content_string = get_content_string_from_markdown_file(test_working_directory)

        assert content_string == ""


@pytest.mark.django_db
@patch("blog.utils.os.remove")
class TestRemoveFiles:
    def test_files_removed(
        self, os_remove_mock: Mock, blog_post_raw: BlogPostRawFactory, test_working_directory: Path
    ) -> None:
        file_paths_to_remove = [
            test_working_directory / "blog/tests/data/images/empty_shelves.jpg",
            test_working_directory / "blog/tests/data/images/empty_shelves_grayscale.png",
            test_working_directory / "blog/tests/data/images/empty_shelves_edges.png",
            test_working_directory / "blog/tests/data/images/empty_shelves_erosion.png",
            test_working_directory / "blog/tests/data/images/empty_shelves_dilation.png",
        ]

        remove_files(file_paths_to_remove)

        assert os_remove_mock.call_count == len(file_paths_to_remove)
        calls = [
            call(file_paths_to_remove[0]),
            call(file_paths_to_remove[1]),
            call(file_paths_to_remove[2]),
            call(file_paths_to_remove[3]),
            call(file_paths_to_remove[4]),
        ]
        os_remove_mock.assert_has_calls(calls)

    def test_not_existing_files_not_removed(
        self, os_remove_mock: Mock, blog_post_raw: BlogPostRawFactory
    ) -> None:
        remove_files([Path("/dummy/path/foo.md")])

        assert os_remove_mock.call_count == 0

    def test_directories_not_removed(
        self, os_remove_mock: Mock, blog_post_raw: BlogPostRawFactory, test_working_directory: Path
    ) -> None:
        remove_files([test_working_directory])

        assert os_remove_mock.call_count == 0
