from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractedBlogPost:
    content_path: str
    title: str
    slug: str
    lead: str
    tags: list[str]
    html_content: str
