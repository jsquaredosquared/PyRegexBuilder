# https://www.regular-expressions.info/posixbrackets.html

from enum import Enum
from typing import Iterable, Protocol, overload
import regex as re
from .common import RegexComponent, RegexString, RegexBuilderException


class Anchor(Enum):
    START_OF_STRING = RegexString(r"^")
    END_OF_STRING = RegexString(r"$")
    WORD_BOUNDARY = RegexString(r"\b")


class Character(Enum):
    ANY = RegexString(r".")
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
        inverted_regex = self._get_regex_complement()
        return CharacterClass(rf"/{inverted_regex}/")

    def intersection(
        self, other: "SupportsBracketExpression"
    ) -> "SupportsBracketExpression":
        return CharacterClass(rf"/[{self.regex}&&{other.regex}]/")

    def subtracting(
        self, other: "SupportsBracketExpression"
    ) -> "SupportsBracketExpression":
        return CharacterClass(rf"/[{self.regex}--{other.regex}]/")

    def symmetric_difference(
        self, other: "SupportsBracketExpression"
    ) -> "SupportsBracketExpression":
        return CharacterClass(rf"/[{self.regex}~~{other.regex}]/")

    def union(self, other: "SupportsBracketExpression") -> "SupportsBracketExpression":
        return CharacterClass(rf"/[{self.regex}||{other.regex}]/")


class CharacterClass(SupportsBracketExpression):
    def __init__(self, *character_set: "str | SupportsBracketExpression") -> None:
        str_args = filter(lambda s: isinstance(s, str), character_set)
        if any(not re.match(r"^/[.*]/$", arg) for arg in str_args):
            raise RegexBuilderException()

        char_sets = [self.parse(component) for component in character_set]

        self._regex = rf"[{'||'.join(char_sets)}]"

    @staticmethod
    def any_of(character_sequence: Iterable) -> "CharacterClass":
        return CharacterClass(rf"/[{re.escape(''.join(character_sequence))}]/")


class UnicodeProperty(SupportsBracketExpression):
    @overload
    def __init__(self, *, key: str, value: str) -> None: ...

    @overload
    def __init__(self, value: str) -> None: ...

    def __init__(self, *args, **kwargs) -> None:
        if len(args) == 1:
            self._regex = rf"\p{{{args[0]}}}"
        elif len(set(["key", "value"]).intersection(kwargs.keys())) == 2:
            self._regex = rf"\p{{{kwargs["key"]}={kwargs["value"]}}}"
        else:
            raise RegexBuilderException()

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
