from typing import Literal, TypedDict, Protocol
import regex as re
from copy import deepcopy


class RegexBuilderException(Exception):
    pass


class RegexFlagsDict(TypedDict, total=False):
    ASCII: Literal[True]
    FULLCASE: bool
    IGNORECASE: bool
    LOCALE: Literal[True]
    MULTILINE: bool
    DOTALL: bool
    UNICODE: Literal[True]
    VERBOSE: bool
    WORD: bool


class RegexGlobalFlagsDict(TypedDict, total=False):
    BESTMATCH: Literal[True]
    ENHANCEMATCH: Literal[True]
    POSIX: Literal[True]
    REVERSE: Literal[True]
    VERSION0: Literal[True]
    VERSION1: Literal[True]


class RegexComponent(Protocol):
    _regex: str

    @property
    def regex(self):
        return self._regex

    @regex.setter
    def regex(self, expr: str):
        self._regex = expr

    def parse(self, *components: "str | RegexComponent") -> str:
        return "".join(
            re.escape(component) if isinstance(component, str) else component.regex
            for component in components
        )

    def with_flags(self, flags: RegexFlagsDict):
        flags_shorthand = {
            "ASCII": "a",
            "FULLCASE": "f",
            "IGNORECASE": "i",
            "LOCALE": "L",
            "MULTILINE": "m",
            "DOTALL": "s",
            "UNICODE": "u",
            "VERBOSE": "x",
            "WORD": "w",
        }

        flags_to_set = set(
            flags_shorthand[flag] for flag in filter(lambda f: flags[f], flags)
        )
        flags_to_remove = set(
            flags_shorthand[flag] for flag in filter(lambda f: not flags[f], flags)
        )

        updated_component = deepcopy(self)
        updated_component.regex = (
            rf"(?{''.join(flags_to_set)}"
            rf"{"-"+''.join(flags_to_remove) if flags_to_remove else ''}"
            rf":{self.regex})"
        )

        return updated_component

    def with_global_flags(self, flags: RegexGlobalFlagsDict):
        flags_shorthand = {
            "BESTMATCH": "b",
            "ENHANCEMATCH": "e",
            "POSIX": "p",
            "REVERSE": "r",
            "VERSION0": "V0",
            "VERSION1": "V1",
        }

        updated_component = deepcopy(self)

        updated_component.regex = (
            rf"(?{''.join(flags_shorthand[flag] for flag in flags)}){self.regex}"
        )

        return updated_component


class RegexString(RegexComponent):
    def __init__(self, string: str) -> None:
        self.regex = string


class Regex(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = self.parse(*components)

    def compile(self, *args, **kwargs):
        return re.compile(self.regex, *args, **kwargs)


class ChoiceOf(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = (
            rf"(?:{'|'.join(self.parse(component) for component in components)})"
        )
