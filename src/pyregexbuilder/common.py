from typing import Literal, TypedDict
from abc import ABC
import regex as re


class RegexBuilderException(Exception):
    pass


class RegexFlagsDict(TypedDict, total=False):
    ASCII: Literal[True]
    IGNORECASE: bool
    LOCAL: Literal[True]
    MULTILINE: bool
    DOTALL: bool
    UNICODE: Literal[True]
    VERBOSE: bool


class RegexComponent(ABC):
    regex: str

    def parse(self, *components: "str | RegexComponent") -> str:
        return "".join(
            (
                component.regex
                if isinstance(component, RegexComponent)
                else re.escape(component)
            )
            for component in components
        )

    def with_flags(self, flags: RegexFlagsDict):
        flags_shorthand = {
            "ASCII": "a",
            "IGNORECASE": "i",
            "LOCAL": "L",
            "MULTILINE": "m",
            "DOTALL": "s",
            "UNICODE": "u",
            "VERBOSE": "x",
        }

        if sum((flag in flags for flag in ["ASCII", "LOCAL", "UNICODE"])) > 1:
            raise RegexBuilderException(
                "The flags ASCII, LOCAL, and UNICODE are mutually exclusive. "
                "Specify only one of them."
            )

        flags_to_set = set(
            flags_shorthand[flag] for flag in filter(lambda f: flags[f], flags)
        )
        flags_to_remove = set(
            flags_shorthand[flag] for flag in filter(lambda f: not flags[f], flags)
        )

        self.regex = rf"(?{''.join(flags_to_set)}{"-"+''.join(flags_to_remove) if flags_to_remove else ''}:{self.regex})"

        return self


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
