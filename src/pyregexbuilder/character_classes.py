# https://www.regular-expressions.info/posixbrackets.html

from copy import deepcopy
from enum import Enum
from typing import overload
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


class CharacterClass(RegexComponent):
    def __init__(self, *character_set: "str | CharacterClass") -> None:
        self.char_sets = []
        for char_set in character_set:
            if isinstance(char_set, str):
                self.char_sets.append(rf"[{char_set}]")
            elif isinstance(char_set, CharacterClass):
                self.char_sets.append(char_set.regex)

        self.regex = rf"[{'||'.join(self.char_sets)}]"
        self.complement = re.sub(r"(?<=^\[)", "^", self.regex)

    @property
    def inverted(self) -> "CharacterClass":
        updated_class = deepcopy(self)
        updated_class.regex = self.complement
        updated_class.complement = self.regex
        return updated_class

    def intersection(self, other: "CharacterClass") -> "CharacterClass":
        updated_class = deepcopy(self)
        updated_class.regex = rf"[{self.regex}&&{other.regex}]"
        return updated_class

    def subtracting(self, other: "CharacterClass") -> "CharacterClass":
        updated_class = deepcopy(self)
        updated_class.regex = rf"[{self.regex}--{other.regex}]"
        return updated_class

    def symmetric_difference(self, other: "CharacterClass") -> "CharacterClass":
        updated_class = deepcopy(self)
        updated_class.regex = rf"[{self.regex}~~{other.regex}]"
        return updated_class

    def union(self, other: "CharacterClass") -> "CharacterClass":
        updated_class = deepcopy(self)
        updated_class.regex = rf"[{self.regex}||{other.regex}]"
        return updated_class


class UnicodeProperty(CharacterClass):
    @overload
    def __init__(self, *, key: str, value: str) -> None: ...

    @overload
    def __init__(self, value: str) -> None: ...

    def __init__(self, *args, **kwargs) -> None:
        if len(args) == 1:
            self.regex = rf"\p{{{args[0]}}}"
        if len(set(["key", "value"]).intersection(kwargs.keys())) == 2:
            self.regex = rf"\p{{{kwargs["key"]}={kwargs["value"]}}}"

        self.complement = self.regex.replace("p", "P")


class PosixClass(CharacterClass):
    def __init__(self, posix_class) -> None:
        self.regex = rf"[[:{posix_class}:]]"
        self.complement = rf"[[:^{posix_class}]]"


class NamedChar(RegexComponent):
    def __init__(self, name) -> None:
        self.regex = rf"\N{{{name}}}"
