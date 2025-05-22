# https://www.regular-expressions.info/posixbrackets.html

from copy import deepcopy
from enum import Enum
from typing import Protocol, overload
import regex as re
from .common import RegexComponent, RegexString

ANY = RegexString(r".")


class Anchor(Enum):
    START_OF_STRING = RegexString(r"^")
    END_OF_STRING = RegexString(r"$")
    WORD_BOUNDARY = RegexString(r"\b")


DIGIT = RegexString(r"\d")
NOT_DIGIT = RegexString(r"\D")
WHITESPACE = RegexString(r"\s")
NOT_WHITESPACE = RegexString(r"\S")
WORD = RegexString(r"\w")
NOT_WORD = RegexString(r"\W")
GRAPHEME = RegexString(r"\X")


class SupportsBracketExpression(RegexComponent, Protocol):
    def _get_regex_complement(self) -> str:
        return re.sub(
            r"(?<=^\[)(?|\^|)", lambda m: "^" if m.group() == "" else "", self._regex
        )

    @property
    def inverted(self) -> "SupportsBracketExpression":
        updated_class = deepcopy(self)
        updated_class._regex = self._get_regex_complement()
        return updated_class

    def intersection(
        self, other: "SupportsBracketExpression"
    ) -> "SupportsBracketExpression":
        updated_class = deepcopy(self)
        updated_class._regex = rf"[{self._regex}&&{other._regex}]"
        return updated_class

    def subtracting(
        self, other: "SupportsBracketExpression"
    ) -> "SupportsBracketExpression":
        updated_class = deepcopy(self)
        updated_class._regex = rf"[{self._regex}--{other._regex}]"
        return updated_class

    def symmetric_difference(
        self, other: "SupportsBracketExpression"
    ) -> "SupportsBracketExpression":
        updated_class = deepcopy(self)
        updated_class._regex = rf"[{self._regex}~~{other._regex}]"
        return updated_class

    def union(self, other: "SupportsBracketExpression") -> "SupportsBracketExpression":
        updated_class = deepcopy(self)
        updated_class._regex = rf"[{self._regex}||{other._regex}]"
        return updated_class


class CharacterClass(SupportsBracketExpression):
    def __init__(self, *character_set: "str | SupportsBracketExpression") -> None:
        char_sets = []
        for char_set in character_set:
            if isinstance(char_set, str):
                if re.match(r"^\[.+\]$", char_set):
                    char_sets.append(char_set)
                else:
                    char_sets.append(rf"[{re.escape(char_set)}]")
            else:
                char_sets.append(char_set.regex)

        self._regex = rf"[{'||'.join(char_sets)}]"


class UnicodeProperty(SupportsBracketExpression):
    @overload
    def __init__(self, *, key: str, value: str) -> None: ...

    @overload
    def __init__(self, value: str) -> None: ...

    def __init__(self, *args, **kwargs) -> None:
        if len(args) == 1:
            self._regex = rf"\p{{{args[0]}}}"
        if len(set(["key", "value"]).intersection(kwargs.keys())) == 2:
            self._regex = rf"\p{{{kwargs["key"]}={kwargs["value"]}}}"

    def _get_regex_complement(self) -> str:
        return re.sub(
            r"(?<=^\\)[pP]", lambda m: "P" if m.group() == "p" else "p", self._regex
        )


class PosixClass(SupportsBracketExpression):
    def __init__(self, posix_class) -> None:
        self._regex = rf"[[:{posix_class}:]]"

    def _get_regex_complement(self) -> str:
        return re.sub(
            r"(?<=^\[\[:)(?|\^|)", lambda m: "^" if m.group() == "" else "", self._regex
        )


class NamedChar(RegexComponent):
    def __init__(self, name) -> None:
        self._regex = rf"\N{{{name}}}"
