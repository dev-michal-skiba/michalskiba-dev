from pathlib import Path

from .conf import LEAD_PARSERS
from .utils import apply_parsers, get_section_text_by_tag


def get_lead_text(file_path: Path) -> str:
    lead_text = get_section_text_by_tag(file_path=file_path, tag="lead")
    lead_text = apply_parsers(value=lead_text, parsers=LEAD_PARSERS)
    return lead_text
