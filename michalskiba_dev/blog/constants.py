import re

MARKDOWN_IMAGES_REGEX = re.compile(r"!\[([^\[\]]+)]\(([^()]+)\)")
MARKDOWN_LINK_REGEX = re.compile(r"(^|[^!])\[([^\[\]]+)]\(([^()]+)\)")
MARKDOWN_BOLD_REGEX = re.compile(r"\*\*([^*]+)\*\*")
MARKDOWN_ITALIC_REGEX = re.compile(r"\*([^*]+)\*")
