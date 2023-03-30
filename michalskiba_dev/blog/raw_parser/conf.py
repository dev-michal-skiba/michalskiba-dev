from blog.raw_parser.base_parsers import (
    BaseParser,
    MultipleSpacesParser,
    ReplaceParser,
    StripParser,
)

COMMON_PARSERS: list[BaseParser] = [
    ReplaceParser(old="\n", new=" "),
    StripParser(strip_char=" "),
    MultipleSpacesParser(),
]
