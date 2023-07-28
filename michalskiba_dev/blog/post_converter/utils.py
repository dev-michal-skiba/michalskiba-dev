import os
from pathlib import Path

from .conf import COMMON_CONVERTERS
from .converters import BaseConverter


def get_section_text_by_tag(file_path: Path, tag: str, use_default_converters: bool = True) -> str:
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
    if use_default_converters:
        section_text = apply_converters(value=section_text, converters=COMMON_CONVERTERS)
    return section_text


def apply_converters(value: str, converters: list[BaseConverter]) -> str:
    for converter in converters:
        value = converter.apply(value)
    return value
