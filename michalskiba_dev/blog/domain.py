from dataclasses import dataclass


@dataclass
class ExtractedBlogPostInfo:
    title: str
    slug: str
    lead: str
    tags: list[str]
    html_content: str
