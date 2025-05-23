"""
See:

- [POSIX character classes](https://github.com/mrabarnett/mrab-regex?tab=readme-ov-file#posix-character-classes)
- [Unicode codepoint properties](https://github.com/mrabarnett/mrab-regex?tab=readme-ov-file#unicode-codepoint-properties-including-scripts-and-blocks)
"""

from enum import Enum
from typing import Sequence, Protocol, overload
import regex as re
from .common import RegexComponent, RegexBuilderException


class Anchor(RegexComponent):
    """
    Static constants defining useful anchors.
    """

    START_OF_STRING = r"/^/"
    END_OF_STRING = r"/$/"
    WORD_BOUNDARY = r"/\b/"


class Character(RegexComponent):
    """
    Static constants defining useful characters.
    """

    ANY = r"/./"
    DIGIT = r"/\d/"
    NOT_DIGIT = r"/\D/"
    WHITESPACE = r"/\s/"
    NOT_WHITESPACE = r"/\S/"
    WORD = r"/\w/"
    NOT_WORD = r"/\W/"
    GRAPHEME = r"/\X/"


class SupportsBracketExpression(RegexComponent, Protocol):
    """
    A protocol for classes that support bracket expressions.
    """

    def _get_regex_complement(self) -> str:
        return re.sub(
            r"(?<=^\[)(?|\^|)", lambda m: "^" if m.group() == "" else "", self._regex
        )

    @property
    def inverted(self) -> "SupportsBracketExpression":
        """
        A class that matches any character that does NOT match this character class.
        """
        inverted_regex = self._get_regex_complement()
        return CharacterClass(rf"/{inverted_regex}/")

    def intersection(
        self, other: "SupportsBracketExpression"
    ) -> "SupportsBracketExpression":
        """
        Returns a class that is the intersection of `self` and `other`.
        """
        return CharacterClass(rf"/[{self.regex}&&{other.regex}]/")

    def subtracting(
        self, other: "SupportsBracketExpression"
    ) -> "SupportsBracketExpression":
        """
        Returns a class that is the result of subtracting `other` from `self`.
        """
        return CharacterClass(rf"/[{self.regex}--{other.regex}]/")

    def symmetric_difference(
        self, other: "SupportsBracketExpression"
    ) -> "SupportsBracketExpression":
        """
        Returns a class that is the symmetric difference of `self` and `other`.
        """
        return CharacterClass(rf"/[{self.regex}~~{other.regex}]/")

    def union(self, other: "SupportsBracketExpression") -> "SupportsBracketExpression":
        """
        Returns a class that is the union of `self` and `other`.
        """
        return CharacterClass(rf"/[{self.regex}||{other.regex}]/")


class CharacterClass(SupportsBracketExpression):
    """
    Creates a general character class.
    """

    def __init__(self, *character_set: "str | SupportsBracketExpression") -> None:
        str_args = filter(lambda s: isinstance(s, str), character_set)
        if any(not re.match(r"^/\[.*\]/$", arg) for arg in str_args):
            raise RegexBuilderException(
                "Strings passed to `CharacterClass` must be regex literals "
                "that create character classes (e.g., '/[A-Z]/'). "
                "To create a character class that matches A, -, and Z, "
                "use `CharacterClass.any_of('A-Z')`."
            )

        char_sets = [self.parse(component) for component in character_set]

        self._regex = rf"[{'||'.join(char_sets)}]"

    @staticmethod
    def any_of(character_sequence: Sequence) -> "CharacterClass":
        """
        Returns a character class that matches any of the characters in a sequence.
        """
        return CharacterClass(rf"/[{re.escape(''.join(character_sequence))}]/")


class UnicodeClass(SupportsBracketExpression):
    r"""
    Creates a Unicode character class.

    Regex: `\p{...}`
    """

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
    """
    Creates a POSIX character class.

    Regex: `[[:...:]]`
    """

    def __init__(self, posix_class: str) -> None:
        self._regex = rf"[[:{posix_class}:]]"

    def _get_regex_complement(self) -> str:
        return re.sub(
            r"(?<=^\[\[:)(?|\^|)", lambda m: "^" if m.group() == "" else "", self._regex
        )


class NamedCharacter(RegexComponent):
    r"""
    Creates a regex component that matches a named character.

    Regex: `\N{...}`
    """

    def __init__(self, name: str) -> None:
        self._regex = rf"\N{{{name}}}"
