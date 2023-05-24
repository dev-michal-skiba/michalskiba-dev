import os
from pathlib import Path

from .base_parsers import BaseParser
from .conf import COMMON_PARSERS


def get_section_text_by_tag(file_path: Path, tag: str, use_default_parsers: bool = True) -> str:
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
    if use_default_parsers:
        section_text = apply_parsers(value=section_text, parsers=COMMON_PARSERS)
    return section_text


def apply_parsers(value: str, parsers: list[BaseParser]) -> str:
    for parser in parsers:
        value = parser.parse(value)
    return value
