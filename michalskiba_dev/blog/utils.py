import os
from pathlib import Path

from blog.constants import MARKDOWN_IMAGES_REGEX
from blog.raw_parser import get_section_text_by_tag


def remove_files(file_paths_to_remove: list[Path]) -> None:
    for file_path in file_paths_to_remove:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)


def extract_images_absolute_paths_from_blog_post_raw_file(file_path: Path) -> list[Path]:
    images_absolute_paths: list[Path] = []
    content_text = get_section_text_by_tag(file_path=file_path, tag="content")
    matches = MARKDOWN_IMAGES_REGEX.findall(content_text)
    for match in matches:
        _, relative_path = match
        absolute_path = os.path.join(os.path.dirname(file_path), relative_path)
        absolute_path = os.path.normpath(absolute_path)
        images_absolute_paths.append(Path(absolute_path))
    return images_absolute_paths
