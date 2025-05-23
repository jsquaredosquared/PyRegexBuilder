from typing import Literal, TypedDict, Protocol
import regex as re


class RegexBuilderException(Exception):
    """
    General exception thrown if problems arise during the building of a regular expression.
    """

    pass


class RegexFlagsDict(TypedDict, total=False):
    """
    A mapping of scoped flags that can apply to only part of regular expression.
    """

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
    """
    A mapping of flags that apply to the entire regular expression.
    """

    BESTMATCH: Literal[True]
    ENHANCEMATCH: Literal[True]
    POSIX: Literal[True]
    REVERSE: Literal[True]
    VERSION0: Literal[True]
    VERSION1: Literal[True]


class RegexComponent(Protocol):
    """
    A protocol for classes that can be used as components in the regex builder.
    """

    _regex: str

    @property
    def regex(self) -> str:
        """
        The string corresponding to the regular expression returned by a RegexComponent.
        """
        return self._regex

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
        """
        Returns a copy of the `Regex` object with the corresponding scoped flags set.
        """
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
        """
        Returns a copy of the `Regex` object with the corresponding global flags set.
        """
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


class Regex(RegexComponent):
    """
    The entry point for building a regular expression.
    """

    def __init__(self, *components: str | RegexComponent) -> None:
        self._regex = self.parse(*components)

    def compile(self, *args, **kwargs):
        return re.compile(self._regex, *args, **kwargs)


class ChoiceOf(RegexComponent):
    """
    A regex component that matches any of the supplied regex components.

    Regex: `|`
    """

    def __init__(self, *components: str | RegexComponent) -> None:
        self._regex = (
            rf"(?:{'|'.join(self.parse(component) for component in components)})"
        )
