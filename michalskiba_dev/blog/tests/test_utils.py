from pathlib import Path
from typing import Any, Callable
from unittest.mock import Mock, call, patch

import pytest

from blog.models import BlogPost, BlogPostRaw
from blog.tests.factories import BlogPostRawFactory
from blog.utils import (
    create_blog_post_file,
    extract_images_absolute_paths_from_blog_post_raw_file,
    get_extracted_blog_post_info_from_blog_post_raw_file,
    remove_files,
)


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


@pytest.mark.django_db
class TestExtractImagesFromBlogPostRawFile:
    def test_images_extracted_correctly(
        self, blog_post_raw: BlogPostRaw, test_working_directory: Path
    ) -> None:
        images_absolute_paths = extract_images_absolute_paths_from_blog_post_raw_file(
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
class TestGetExtractedBlogPostInfoFromBlogPostRawFile:
    def test_extracted_blog_post_info_is_correct(
        self,
        blog_post_raw: BlogPostRaw,
        blog_post: BlogPost,
        assert_file_content: Callable[[Path, str], None],
    ) -> None:
        extracted_blog_post_info = get_extracted_blog_post_info_from_blog_post_raw_file(
            blog_post_raw.absolute_path
        )

        assert extracted_blog_post_info.title == (
            "Some title title title title title title title title title title"
        )
        assert extracted_blog_post_info.slug == (
            "some-title-title-title-title-title-title-title-title-title-title"
        )
        assert extracted_blog_post_info.lead == "Some xy" + 101 * " lead"
        assert extracted_blog_post_info.tags == ["tag1", "tag2", "reallylongtag123"]
        assert_file_content(blog_post.absolute_path, extracted_blog_post_info.html_content)


@patch("blog.utils.settings")
class TestCreateBlogPostFile:
    def test_blog_post_file_created(self, settings_mock: Mock, tmpdir: Any) -> None:
        tmp_file = tmpdir.join(Path("test.html"))
        settings_mock.BLOG_POSTS_PATH = Path(tmp_file.strpath[:-10])
        html_content = "<div>\nHello World!\n</div>"

        create_blog_post_file(content_path="test.html", html_content=html_content)

        assert tmp_file.read() == html_content
