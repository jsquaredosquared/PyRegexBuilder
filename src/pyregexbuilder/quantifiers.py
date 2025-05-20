from enum import Enum

from .common import RegexComponent, RegexBuilderException


class Greed(Enum):
    GREEDY = ""
    EAGER = ""
    POSSESSIVE = "+"
    MINIMAL = "?"
    RELUCTANT = "?"


class One(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = rf"(?:{self.parse(*components)}){1}"


class Optionally(RegexComponent):
    def __init__(
        self, *components: str | RegexComponent, greed: Greed = Greed.GREEDY
    ) -> None:
        self.regex = rf"(?:{self.parse(*components)})?{greed.value}"


class ZeroOrMore(RegexComponent):
    def __init__(
        self, *components: str | RegexComponent, greed: Greed = Greed.GREEDY
    ) -> None:
        self.regex = rf"(?:{self.parse(*components)})*{greed.value}"


class OneOrMore(RegexComponent):
    def __init__(
        self, *components: str | RegexComponent, greed: Greed = Greed.GREEDY
    ) -> None:
        self.regex = rf"(?:{self.parse(*components)})+{greed.value}"


class Repeat(RegexComponent):
    def __init__(
        self,
        *components,
        count: int | None = None,
        minimum: int | None = None,
        maximum: int | None = None,
        greed: Greed = Greed.GREEDY,
    ) -> None:
        if (count and (minimum or maximum)) or not (any((count, minimum, maximum))):
            raise RegexBuilderException(
                "Must specify either `count` OR `minimum` and/or `maximum`."
            )

        if count:
            self.regex = rf"(?:{self.parse(*components)}{{{count}}})"
        else:
            m = minimum if minimum else ""
            n = maximum if maximum else ""
            self.regex = rf"(?:{self.parse(*components)}){{{m},{n}}}{greed.value}"
