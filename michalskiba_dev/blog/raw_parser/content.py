from pathlib import Path

from .conf import CONTENT_HTML_PARSERS, CONTENT_PARSERS
from .utils import apply_parsers, get_section_text_by_tag


def get_content_text(file_path: Path) -> str:
    content_text = get_section_text_by_tag(
        file_path=file_path, tag="content", use_default_parsers=False
    )
    content_text = apply_parsers(value=content_text, parsers=CONTENT_PARSERS)
    return content_text


def get_content_html_text(content_text: str) -> str:
    context_html_text = apply_parsers(value=content_text, parsers=CONTENT_HTML_PARSERS)
    return context_html_text
