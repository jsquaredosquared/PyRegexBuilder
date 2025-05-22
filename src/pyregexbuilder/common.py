from typing import Literal, TypedDict, Protocol
import regex as re


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

    # @regex.setter
    # def regex(self, expr: str):
    #     self._regex = expr

    def parse(self, *components: "str | RegexComponent") -> str:
        patterns = []

        for component in components:
            if isinstance(component, str):
                if re.match(r"^/.*/$", component):
                    patterns.append(component[1:-1])
                else:
                    patterns.append(re.escape(component))
            else:
                patterns.append(component.regex)

        return "".join(patterns)

    def with_flags(self, flags: RegexFlagsDict) -> "Regex":
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

        return Regex(
            rf"/(?{''.join(flags_to_set)}"
            rf"{"-"+''.join(flags_to_remove) if flags_to_remove else ''}"
            rf":{self._regex})/"
        )

    def with_global_flags(self, flags: RegexGlobalFlagsDict) -> "Regex":
        flags_shorthand = {
            "BESTMATCH": "b",
            "ENHANCEMATCH": "e",
            "POSIX": "p",
            "REVERSE": "r",
            "VERSION0": "V0",
            "VERSION1": "V1",
        }

        return Regex(
            rf"/(?{''.join(flags_shorthand[flag] for flag in flags)}){self._regex}/"
        )


class RegexString(RegexComponent):
    def __init__(self, string: str) -> None:
        self._regex = string


class Regex(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self._regex = self.parse(*components)

    def compile(self, *args, **kwargs):
        return re.compile(self._regex, *args, **kwargs)


class ChoiceOf(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self._regex = (
            rf"(?:{'|'.join(self.parse(component) for component in components)})"
        )
