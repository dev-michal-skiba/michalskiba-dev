from pathlib import Path

from .conf import TITLE_PARSERS
from .utils import apply_parsers, get_section_text_by_tag


def get_title_text(file_path: Path) -> str:
    title_text = get_section_text_by_tag(file_path=file_path, tag="title")
    title_text = apply_parsers(value=title_text, parsers=TITLE_PARSERS)
    return title_text
