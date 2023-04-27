from pathlib import Path

from .conf import TAGS_PARSERS
from .utils import apply_parsers, get_section_text_by_tag


def get_tags(file_path: Path) -> list[str]:
    tags_text = get_section_text_by_tag(file_path=file_path, tag="tags")
    tags_text = apply_parsers(value=tags_text, parsers=TAGS_PARSERS)
    tags = tags_text.split(",")
    return tags
