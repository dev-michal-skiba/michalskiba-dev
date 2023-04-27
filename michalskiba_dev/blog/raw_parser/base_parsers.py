import os.path
import re

from django.conf import settings

from blog.constants import (
    MARKDOWN_BOLD_REGEX,
    MARKDOWN_IMAGES_REGEX,
    MARKDOWN_ITALIC_REGEX,
    MARKDOWN_LINK_REGEX,
)


class BaseParser:
    def parse(self, text: str) -> str:  # pragma: no cover
        return text


class ReplaceParser(BaseParser):
    def __init__(self, old: str, new: str):
        self._old = old
        self._new = new

    def parse(self, text: str) -> str:
        return text.replace(self._old, self._new)


class StripParser(BaseParser):
    def __init__(self, strip_char: str = " "):
        self._strip_char = strip_char

    def parse(self, text: str) -> str:
        return text.strip(self._strip_char)


class ListStripParser(StripParser):
    def __init__(self, strip_char: str = " ", split_char: str = ","):
        super(ListStripParser, self).__init__(strip_char)
        self._split_char = split_char

    def parse(self, text: str) -> str:
        elements: list[str] = text.split(self._split_char)
        parsed_elements = []
        for element in elements:
            parsed_element = super(ListStripParser, self).parse(element)
            if parsed_element:
                parsed_elements.append(parsed_element)
        return f"{self._split_char}".join(parsed_elements)


class MultipleCharsParser(BaseParser):
    def __init__(self, char: str = " "):
        self._char = char

    def parse(self, text: str) -> str:
        result = re.sub(f"{self._char}+", f"{self._char}", text)
        return str(result)


class TrimParser(BaseParser):
    def __init__(self, max_length: int):
        self._max_length = max_length

    def parse(self, text: str) -> str:
        return text[: self._max_length]


class ListTrimParser(TrimParser):
    def __init__(self, max_length: int, split_char: str = " "):
        super(ListTrimParser, self).__init__(max_length)
        self._split_char = split_char

    def parse(self, text: str) -> str:
        elements: list[str] = text.split(self._split_char)
        for i in range(len(elements)):
            elements[i] = super(ListTrimParser, self).parse(elements[i])
        return f"{self._split_char}".join(elements)


class ListLowercaseParser(BaseParser):
    def __init__(self, split_char: str = " "):
        self._split_char = split_char

    def parse(self, text: str) -> str:
        elements: list[str] = text.split(self._split_char)
        for i in range(len(elements)):
            elements[i] = elements[i].lower()
        return f"{self._split_char}".join(elements)


class RemoveParser(BaseParser):
    def __init__(self, remove_char: str = " "):
        self._remove_char = remove_char

    def parse(self, text: str) -> str:
        return text.replace(self._remove_char, "")


class HTMLHeaderParser(BaseParser):
    def __init__(self, split_char: str = "\n", strip_char: str = " "):
        self._split_char = split_char
        self._strip_char = strip_char

    def parse(self, text: str) -> str:
        elements: list[str] = text.split(self._split_char)
        for index in range(len(elements)):
            for header_index in range(5, 0, -1):
                if elements[index].startswith(header_index * "#"):
                    elements[index] = elements[index][header_index:]
                    elements[index] = elements[index].strip(self._strip_char)
                    elements[
                        index
                    ] = f"<h{header_index + 1}>{elements[index]}</h{header_index + 1}>"
                    break
        return f"{self._split_char}".join(elements)


class HTMLUnorderedListParser(BaseParser):
    def __init__(self, split_char: str = "\n", strip_char: str = " "):
        self._split_char = split_char
        self._strip_char = strip_char

    def parse(self, text: str) -> str:
        current_list_level = 0
        elements: list[str] = text.split(self._split_char)
        return_elements: list[str] = []
        for element in elements:
            if current_list_level:
                should_continue = False
                if current_list_level >= 2:
                    for i in range(2, current_list_level + 1):
                        if element.startswith((current_list_level - i) * "  " + "-"):
                            for _ in range(i - 1):
                                return_elements.append("</ul>")
                                current_list_level -= 1
                            return_elements.append(
                                f"<li>{element.strip(self._strip_char)[2:]}</li>"
                            )
                            should_continue = True
                            break
                if should_continue:
                    continue
                if element.startswith((current_list_level - 1) * "  " + "-"):
                    return_elements.append(f"<li>{element.strip(self._strip_char)[2:]}</li>")
                elif element.startswith(current_list_level * "  " + "-"):
                    return_elements.append("<ul>")
                    return_elements.append(f"<li>{element.strip(self._strip_char)[2:]}</li>")
                    current_list_level += 1
                else:
                    for _ in range(current_list_level):
                        return_elements.append("</ul>")
                    current_list_level = 0
                    return_elements.append(element)
            else:
                if element.startswith("-"):
                    return_elements.append("<ul>")
                    return_elements.append(f"<li>{element.strip(self._strip_char)[2:]}</li>")
                    current_list_level += 1
                else:
                    return_elements.append(element)
        if current_list_level and return_elements[-1].startswith("<li>"):
            for _ in range(current_list_level):
                return_elements.append("</ul>")
        return f"{self._split_char}".join(return_elements)


class HTMLOrderedListParser(BaseParser):
    def __init__(self, split_char: str = "\n", strip_char: str = " "):
        self._split_char = split_char
        self._strip_char = strip_char

    def parse(self, text: str) -> str:
        element_counter = 0
        elements: list[str] = text.split(self._split_char)
        return_elements: list[str] = []
        for element in elements:
            if element_counter:
                expected_starting_chars = f"{element_counter + 1}. "
                if element.startswith(expected_starting_chars):
                    return_elements.append(
                        f"<li>{element[len(expected_starting_chars):].strip(self._strip_char)}</li>"
                    )
                    element_counter += 1
                else:
                    return_elements.append("</ol>")
                    element_counter = 0
            if not element_counter:
                if element.startswith("1. "):
                    return_elements.append("<ol>")
                    return_elements.append(f"<li>{element[3:].strip(self._strip_char)}</li>")
                    element_counter += 1
                else:
                    return_elements.append(element)
        if element_counter:
            return_elements.append("</ol>")
        return f"{self._split_char}".join(return_elements)


class HTMLImageParser(BaseParser):
    def parse(self, text: str) -> str:
        matches = MARKDOWN_IMAGES_REGEX.findall(text)
        for match in matches:
            alternative_text, relative_path = match
            absolute_path = settings.BLOG_POSTS_RAW_PATH / relative_path
            absolute_path = os.path.normpath(absolute_path)
            path = os.path.relpath(absolute_path, settings.BASE_STATIC_PATH)
            static_path_tag = f"{{% static '{path}' %}}"
            text = text.replace(
                f"![{alternative_text}]({relative_path})",
                f'<img src="{static_path_tag}" alt="{alternative_text}">',
            )
        return text


class HTMLParagraphParser(BaseParser):
    def __init__(self, split_char: str = "\n", strip_char: str = " "):
        self._split_char = split_char
        self._strip_char = strip_char

    def parse(self, text: str) -> str:
        current_text = []
        elements: list[str] = text.split(self._split_char)
        return_elements: list[str] = []
        for element in elements:
            if not element.startswith("<"):
                current_text.append(element.strip(self._strip_char))
                continue
            elif current_text:
                paragraph_text = " ".join(current_text)
                return_elements.append(f"<p>{paragraph_text}</p>")
                current_text = []
            return_elements.append(element)
        if current_text:
            paragraph_text = " ".join(current_text)
            return_elements.append(f"<p>{paragraph_text}</p>")
        return f"{self._split_char}".join(return_elements)


class HTMLLinkParser(BaseParser):
    def parse(self, text: str) -> str:
        matches = MARKDOWN_LINK_REGEX.findall(text)
        for match in matches:
            _, link_text, link = match
            text = text.replace(
                f"[{link_text}]({link})",
                f'<a href="{link}">{link_text}</a>',
            )
        return text


class HTMLBoldParser(BaseParser):
    def parse(self, text: str) -> str:
        matches = MARKDOWN_BOLD_REGEX.findall(text)
        for match in matches:
            text = text.replace(
                f"**{match}**",
                f"<b>{match}</b>",
            )
        return text


class HTMLItalicParser(BaseParser):
    def parse(self, text: str) -> str:
        matches = MARKDOWN_ITALIC_REGEX.findall(text)
        for match in matches:
            text = text.replace(
                f"*{match}*",
                f"<i>{match}</i>",
            )
        return text
