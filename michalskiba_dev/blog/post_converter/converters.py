import os.path
import re

from django.conf import settings
from django.templatetags.static import static
from slugify import slugify

from blog.constants import (
    MARKDOWN_BOLD_REGEX,
    MARKDOWN_IMAGES_REGEX,
    MARKDOWN_ITALIC_REGEX,
    MARKDOWN_LINK_REGEX,
)


class BaseConverter:
    def apply(self, text: str) -> str:  # pragma: no cover
        return text


class Replace(BaseConverter):
    def __init__(self, old: str, new: str):
        self._old = old
        self._new = new

    def apply(self, text: str) -> str:
        return text.replace(self._old, self._new)


class Strip(BaseConverter):
    def __init__(self, strip_char: str = " "):
        self._strip_char = strip_char

    def apply(self, text: str) -> str:
        return text.strip(self._strip_char)


class ListStrip(Strip):
    def __init__(self, strip_char: str = " ", split_char: str = ","):
        super(ListStrip, self).__init__(strip_char)
        self._split_char = split_char

    def apply(self, text: str) -> str:
        lines: list[str] = text.split(self._split_char)
        return_lines = []
        for line in lines:
            line = super(ListStrip, self).apply(line)
            if line:
                return_lines.append(line)
        return f"{self._split_char}".join(return_lines)


class MultipleChars(BaseConverter):
    def __init__(self, char: str = " "):
        self._char = char

    def apply(self, text: str) -> str:
        result = re.sub(f"{self._char}+", f"{self._char}", text)
        return str(result)


class Trim(BaseConverter):
    def __init__(self, max_length: int):
        self._max_length = max_length

    def apply(self, text: str) -> str:
        return text[: self._max_length]


class ListTrim(Trim):
    def __init__(self, max_length: int, split_char: str = " "):
        super(ListTrim, self).__init__(max_length)
        self._split_char = split_char

    def apply(self, text: str) -> str:
        lines: list[str] = text.split(self._split_char)
        return_lines = []
        for line in lines:
            line = super(ListTrim, self).apply(line)
            return_lines.append(line)
        return f"{self._split_char}".join(return_lines)


class ListLowercase(BaseConverter):
    def __init__(self, split_char: str = " "):
        self._split_char = split_char

    def apply(self, text: str) -> str:
        lines: list[str] = text.split(self._split_char)
        return_lines = []
        for line in lines:
            line = line.lower()
            return_lines.append(line)
        return f"{self._split_char}".join(return_lines)


class Remove(BaseConverter):
    def __init__(self, remove_char: str = " "):
        self._remove_char = remove_char

    def apply(self, text: str) -> str:
        return text.replace(self._remove_char, "")


class HTMLHeader(BaseConverter):
    def __init__(self, split_char: str = "\n", strip_char: str = " "):
        self._split_char = split_char
        self._strip_char = strip_char

    def apply(self, text: str) -> str:
        lines: list[str] = text.split(self._split_char)
        return_lines = []
        for line in lines:
            for header_index in range(5, 0, -1):
                if line.startswith(header_index * "#"):
                    line = line[header_index:]
                    line = line.strip(self._strip_char)
                    line = f"<h{header_index + 1}>{line}</h{header_index + 1}>"
                    return_lines.append(line)
                    break
            else:
                return_lines.append(line)
        return f"{self._split_char}".join(return_lines)


class HTMLUnorderedList(BaseConverter):
    def __init__(self, split_char: str = "\n", strip_char: str = " "):
        self._split_char = split_char
        self._strip_char = strip_char

    def apply(self, text: str) -> str:
        current_list_level = 0
        lines: list[str] = text.split(self._split_char)
        return_lines: list[str] = []
        for line in lines:
            if current_list_level:
                current_list_level, partial_return_lines = self._apply_for_list_started(
                    line, current_list_level
                )
            else:
                current_list_level, partial_return_lines = self._apply_for_list_not_started(
                    line, current_list_level
                )
            return_lines.extend(partial_return_lines)
        partial_return_lines = self._close_remaining_list(
            current_list_level, last_line=return_lines[-1]
        )
        return_lines.extend(partial_return_lines)
        return f"{self._split_char}".join(return_lines)

    def _apply_for_list_started(self, line: str, current_list_level: int) -> tuple[int, list[str]]:
        return_lines: list[str] = []
        if current_list_level >= 2:
            current_list_level, return_lines = self._apply_for_deeply_nested_line(
                line, current_list_level
            )
            if return_lines:
                return current_list_level, return_lines
        is_list_continued_with_the_same_level = line.startswith(
            (current_list_level - 1) * "  " + "-"
        )
        if is_list_continued_with_the_same_level:
            return_lines.append(f"<li>{line.strip(self._strip_char)[2:]}</li>")
            return current_list_level, return_lines
        is_list_continued_with_the_deeper_level = line.startswith(current_list_level * "  " + "-")
        if is_list_continued_with_the_deeper_level:
            return_lines.append("<ul>")
            return_lines.append(f"<li>{line.strip(self._strip_char)[2:]}</li>")
            current_list_level += 1
            return current_list_level, return_lines
        for _ in range(current_list_level):
            return_lines.append("</ul>")
        current_list_level = 0
        return_lines.append(line)
        return current_list_level, return_lines

    def _apply_for_deeply_nested_line(
        self, line: str, current_list_level: int
    ) -> tuple[int, list[str]]:
        return_lines = []
        for i in range(2, current_list_level + 1):
            is_deeply_nested_list_finished = line.startswith((current_list_level - i) * "  " + "-")
            if is_deeply_nested_list_finished:
                for _ in range(i - 1):
                    return_lines.append("</ul>")
                    current_list_level -= 1
                return_lines.append(f"<li>{line.strip(self._strip_char)[2:]}</li>")
                break
        return current_list_level, return_lines

    def _apply_for_list_not_started(
        self, line: str, current_list_level: int
    ) -> tuple[int, list[str]]:
        return_lines = []
        is_list_started = line.startswith("-")
        if is_list_started:
            return_lines.append("<ul>")
            return_lines.append(f"<li>{line.strip(self._strip_char)[2:]}</li>")
            current_list_level += 1
        else:
            return_lines.append(line)
        return current_list_level, return_lines

    @staticmethod
    def _close_remaining_list(current_list_level: int, last_line: str) -> list[str]:
        return_lines = []
        if current_list_level and last_line.startswith("<li>"):
            for _ in range(current_list_level):
                return_lines.append("</ul>")
        return return_lines


class HTMLOrderedList(BaseConverter):
    def __init__(self, split_char: str = "\n", strip_char: str = " "):
        self._split_char = split_char
        self._strip_char = strip_char

    def apply(self, text: str) -> str:
        line_counter = 0
        lines: list[str] = text.split(self._split_char)
        return_lines: list[str] = []
        for line in lines:
            if line_counter:
                line_counter, partial_return_lines = self._apply_for_list_started(
                    line, line_counter
                )
                return_lines.extend(partial_return_lines)
            if not line_counter:
                line_counter, partial_return_lines = self._apply_for_list_not_started(
                    line, line_counter
                )
                return_lines.extend(partial_return_lines)
        if line_counter:
            return_lines.append("</ol>")
        return f"{self._split_char}".join(return_lines)

    def _apply_for_list_started(self, line: str, line_counter: int) -> tuple[int, list[str]]:
        return_lines: list[str] = []
        expected_starting_char = f"{line_counter + 1}. "
        if line.startswith(expected_starting_char):
            return_lines.append(
                f"<li>{line[len(expected_starting_char):].strip(self._strip_char)}</li>"
            )
            line_counter += 1
        else:
            return_lines.append("</ol>")
            line_counter = 0
        return line_counter, return_lines

    def _apply_for_list_not_started(self, line: str, line_counter: int) -> tuple[int, list[str]]:
        return_lines: list[str] = []
        if line.startswith("1. "):
            return_lines.append("<ol>")
            return_lines.append(f"<li>{line[3:].strip(self._strip_char)}</li>")
            line_counter += 1
        else:
            return_lines.append(line)
        return line_counter, return_lines


class HTMLImage(BaseConverter):
    def apply(self, text: str) -> str:
        matches = MARKDOWN_IMAGES_REGEX.findall(text)
        for match in matches:
            alternative_text, relative_path = match
            absolute_path = settings.BLOG_POSTS_RAW_PATH / relative_path
            absolute_path = os.path.normpath(absolute_path)
            path = os.path.relpath(absolute_path, settings.BASE_STATIC_PATH)
            static_path = static(path)
            text = text.replace(
                f"![{alternative_text}]({relative_path})",
                f'<img class="img-fluid post-img" src="{static_path}" alt="{alternative_text}">',
            )
        return text


class HTMLParagraph(BaseConverter):
    def __init__(self, split_char: str = "\n", strip_char: str = " "):
        self._split_char = split_char
        self._strip_char = strip_char

    def apply(self, text: str) -> str:
        current_text = []
        lines: list[str] = text.split(self._split_char)
        return_lines: list[str] = []
        for line in lines:
            if not line.startswith("<"):
                current_text.append(line.strip(self._strip_char))
                continue
            elif current_text:
                paragraph_text = " ".join(current_text)
                return_lines.append(f"<p>{paragraph_text}</p>")
                current_text = []
            return_lines.append(line)
        if current_text:
            paragraph_text = " ".join(current_text)
            return_lines.append(f"<p>{paragraph_text}</p>")
        return f"{self._split_char}".join(return_lines)


class HTMLLink(BaseConverter):
    def apply(self, text: str) -> str:
        matches = MARKDOWN_LINK_REGEX.findall(text)
        for match in matches:
            _, link_text, link = match
            text = text.replace(
                f"[{link_text}]({link})",
                f'<a class="link" target="_blank" href="{link}">{link_text}</a>',
            )
        return text


class HTMLBold(BaseConverter):
    def apply(self, text: str) -> str:
        matches = MARKDOWN_BOLD_REGEX.findall(text)
        for match in matches:
            text = text.replace(
                f"**{match}**",
                f"<b>{match}</b>",
            )
        return text


class HTMLItalic(BaseConverter):
    def apply(self, text: str) -> str:
        matches = MARKDOWN_ITALIC_REGEX.findall(text)
        for match in matches:
            text = text.replace(
                f"*{match}*",
                f"<i>{match}</i>",
            )
        return text


class HTMLTableOfContents(BaseConverter):
    def __init__(self, split_char: str = "\n"):
        self._split_char = split_char

    def apply(self, text: str) -> str:
        lines: list[str] = text.split(self._split_char)
        return_lines: list[str] = []
        table_of_contents_lines: list[str] = []
        for line in lines:
            if not line.startswith("<h2>"):
                return_lines.append(line)
                continue
            section_text = line[4:-5]
            identifier = slugify(section_text)
            new_line = line.replace("<h2>", f'<h2 id="{identifier}">')
            return_lines.append(new_line)
            table_of_contents_lines.append(
                f'<li><a class="link" href="#{identifier}">{section_text}</a></li>'
            )
        table_of_contents_list_elements_text = f"{self._split_char}".join(table_of_contents_lines)
        table_of_contents_text = (
            f'<div class="toc_container">\n'
            f'<p class="toc_title">Table of Contents</p>\n'
            f'<ol class="toc_list">\n'
            f"{table_of_contents_list_elements_text}\n"
            f"</ol>\n"
            f"</div>\n"
        )
        content_text = f"{self._split_char}".join(return_lines)
        return table_of_contents_text + content_text
