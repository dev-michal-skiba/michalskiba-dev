from .base_parsers import (
    BaseParser,
    HTMLBoldParser,
    HTMLHeaderParser,
    HTMLImageParser,
    HTMLItalicParser,
    HTMLLinkParser,
    HTMLOrderedListParser,
    HTMLParagraphParser,
    HTMLTableOfContentsParser,
    HTMLUnorderedListParser,
    ListLowercaseParser,
    ListStripParser,
    ListTrimParser,
    MultipleCharsParser,
    RemoveParser,
    ReplaceParser,
    StripParser,
    TrimParser,
)

COMMON_PARSERS: list[BaseParser] = [
    ReplaceParser(old="\n", new=" "),
    StripParser(strip_char=" "),
    MultipleCharsParser(char=" "),
]
TITLE_PARSERS: list[BaseParser] = [TrimParser(max_length=128)]
LEAD_PARSERS: list[BaseParser] = [
    TrimParser(max_length=512),
    HTMLLinkParser(),
    HTMLBoldParser(),
    HTMLItalicParser(),
    MultipleCharsParser(char=" "),
]
TAGS_PARSERS: list[BaseParser] = [
    RemoveParser(remove_char=" "),
    ListTrimParser(max_length=32, split_char=","),
    ListLowercaseParser(split_char=","),
]
CONTENT_PARSERS: list[BaseParser] = [
    MultipleCharsParser(char="\n"),
    StripParser(strip_char=" \n"),
    StripParser(strip_char="\n"),
]
CONTENT_HTML_PARSERS: list[BaseParser] = [
    HTMLHeaderParser(split_char="\n"),
    HTMLUnorderedListParser(split_char="\n"),
    HTMLOrderedListParser(split_char="\n"),
    ListStripParser(strip_char=" ", split_char="\n"),
    HTMLImageParser(),
    HTMLParagraphParser(split_char="\n"),
    HTMLLinkParser(),
    HTMLBoldParser(),
    HTMLItalicParser(),
    MultipleCharsParser(char=" "),
    HTMLTableOfContentsParser(split_char="\n"),
]
