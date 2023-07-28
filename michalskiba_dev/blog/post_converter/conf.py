from .converters import (
    BaseConverter,
    HTMLBold,
    HTMLHeader,
    HTMLImage,
    HTMLItalic,
    HTMLLink,
    HTMLOrderedList,
    HTMLParagraph,
    HTMLTableOfContents,
    HTMLUnorderedList,
    ListLowercase,
    ListStrip,
    ListTrim,
    MultipleChars,
    Remove,
    Replace,
    Strip,
    Trim,
)

COMMON_CONVERTERS: list[BaseConverter] = [
    Replace(old="\n", new=" "),
    Strip(strip_char=" "),
    MultipleChars(char=" "),
]
TITLE_CONVERTERS: list[BaseConverter] = [Trim(max_length=128)]
LEAD_CONVERTERS: list[BaseConverter] = [
    Trim(max_length=512),
    HTMLLink(),
    HTMLBold(),
    HTMLItalic(),
    MultipleChars(char=" "),
]
TAGS_CONVERTERS: list[BaseConverter] = [
    Remove(remove_char=" "),
    ListTrim(max_length=32, split_char=","),
    ListLowercase(split_char=","),
]
CONTENT_CONVERTERS: list[BaseConverter] = [
    MultipleChars(char="\n"),
    Strip(strip_char=" \n"),
    Strip(strip_char="\n"),
]
CONTENT_HTML_CONVERTERS: list[BaseConverter] = [
    HTMLHeader(split_char="\n"),
    HTMLUnorderedList(split_char="\n"),
    HTMLOrderedList(split_char="\n"),
    ListStrip(strip_char=" ", split_char="\n"),
    HTMLImage(),
    HTMLParagraph(split_char="\n"),
    HTMLLink(),
    HTMLBold(),
    HTMLItalic(),
    MultipleChars(char=" "),
    HTMLTableOfContents(split_char="\n"),
]
