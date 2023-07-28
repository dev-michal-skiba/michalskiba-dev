from pathlib import Path

from .conf import (
    CONTENT_CONVERTERS,
    CONTENT_HTML_CONVERTERS,
    LEAD_CONVERTERS,
    TAGS_CONVERTERS,
    TITLE_CONVERTERS,
)
from .utils import apply_converters, get_section_text_by_tag


def get_tags(file_path: Path) -> list[str]:
    tags_text = get_section_text_by_tag(file_path=file_path, tag="tags")
    tags_text = apply_converters(value=tags_text, converters=TAGS_CONVERTERS)
    tags = tags_text.split(",")
    return tags


def get_title_text(file_path: Path) -> str:
    title_text = get_section_text_by_tag(file_path=file_path, tag="title")
    title_text = apply_converters(value=title_text, converters=TITLE_CONVERTERS)
    return title_text


def get_lead_text(file_path: Path) -> str:
    lead_text = get_section_text_by_tag(file_path=file_path, tag="lead")
    lead_text = apply_converters(value=lead_text, converters=LEAD_CONVERTERS)
    return lead_text


def get_content_text(file_path: Path) -> str:
    content_text = get_section_text_by_tag(
        file_path=file_path, tag="content", use_default_converters=False
    )
    content_text = apply_converters(value=content_text, converters=CONTENT_CONVERTERS)
    return content_text


def get_content_html_text(content_text: str) -> str:
    context_html_text = apply_converters(value=content_text, converters=CONTENT_HTML_CONVERTERS)
    return context_html_text
