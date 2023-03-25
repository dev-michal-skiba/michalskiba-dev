import os
from pathlib import Path

from blog.constants import MARKDOWN_IMAGES_REGEX


def extract_images_absolute_paths_from_markdown_file(file_path: Path) -> list[Path]:
    images_absolute_paths: list[Path] = []
    content_string = get_content_string_from_markdown_file(file_path)
    matches = MARKDOWN_IMAGES_REGEX.findall(content_string)
    for match in matches:
        _, relative_path = match
        absolute_path = os.path.join(os.path.dirname(file_path), relative_path)
        absolute_path = os.path.normpath(absolute_path)
        images_absolute_paths.append(Path(absolute_path))
    return images_absolute_paths


def get_content_string_from_markdown_file(file_path: Path) -> str:
    content_string = ""
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return ""
    with open(file_path, "r") as file:
        should_read = False
        for line in file.readlines():
            if "[end content]" in line:
                break
            if should_read:
                content_string += line
            if "[start content]" in line:
                should_read = True
    return content_string.strip("\n")


def remove_files(file_paths_to_remove: list[Path]) -> None:
    for file_path in file_paths_to_remove:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
