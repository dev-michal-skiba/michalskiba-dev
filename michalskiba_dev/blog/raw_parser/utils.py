import os
from pathlib import Path

from blog.raw_parser.base_parsers import BaseParser
from blog.raw_parser.conf import COMMON_PARSERS


def get_section_text_by_tag(file_path: Path, tag: str) -> str:
    section_text = ""
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return ""
    with open(file_path, "r") as file:
        should_read = False
        for line in file.readlines():
            if f"[end {tag}]" in line:
                break
            if should_read:
                section_text += line
            if f"[start {tag}]" in line:
                should_read = True
    section_text = apply_parsers(text=section_text, parsers=COMMON_PARSERS)
    return section_text


def apply_parsers(text: str, parsers: list[BaseParser]) -> str:
    for parser in parsers:
        text = parser.parse(text)
    return text
