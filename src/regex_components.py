import re
from abc import ABC
from enum import Enum


class RegexBuilderException(Exception):
    pass


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


class RegexString(RegexComponent):
    def __init__(self, string: str) -> None:
        self.regex = string


class Greed(Enum):
    GREEDY = ""
    POSSESSIVE = "+"
    MINIMAL = "?"


class One(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = rf"(?:{self.parse(*components)}){1}"


class Optionally(RegexComponent):
    def __init__(
        self, *components: str | RegexComponent, greed: Greed = Greed.GREEDY
    ) -> None:
        self.regex = rf"(?:{self.parse(*components)})?{greed}"


class ZeroOrMore(RegexComponent):
    def __init__(
        self, *components: str | RegexComponent, greed: Greed = Greed.GREEDY
    ) -> None:
        self.regex = rf"(?:{self.parse(*components)})*{greed}"


class OneOrMore(RegexComponent):
    def __init__(
        self, *components: str | RegexComponent, greed: Greed = Greed.GREEDY
    ) -> None:
        self.regex = rf"(?:{self.parse(*components)})+{greed}"


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
            raise RegexBuilderException()

        if count:
            self.regex = rf"(?:{self.parse(*components)}{{{count}}})"
        else:
            m = minimum if minimum else ""
            n = maximum if maximum else ""
            self.regex = rf"(?:{self.parse(*components)}){{{m},{n}}}{greed}"


class Capture(RegexComponent):
    def __init__(self, *components: str | RegexComponent, name: str | None = None):
        if name:
            self.regex = rf"(?P<{name}>{self.parse(*components)})"
        else:
            self.regex = rf"({self.parse(*components)})"


class Atomic(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = rf"(?>{self.parse(*components)})"


ANY = RegexString(r".")
START_OF_STRING = RegexString(r"^")
END_OF_STRING = RegexString(r"$")
WORD = RegexString(r"\w")
WORD_BOUNDARY = RegexString(r"\b")
WHITESPACE = RegexString(r"\s")
DIGIT = RegexString(r"\d")


class ChoiceOf(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = (
            rf"(?:{'|'.join(self.parse(component) for component in components)})"
        )


class Lookahead(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = rf"(?={self.parse(*components)})"


class NegativeLookahead(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = rf"(?!{self.parse(*components)})"


class PostitiveLookbehind(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = rf"(?<={self.parse(*components)})"


class NegativeLookbehind(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = rf"(?<!{self.parse(*components)})"


class Reference(RegexComponent):
    def __init__(self, name: str) -> None:
        self.regex = rf"(?P={name})"


class Regex(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = self.parse(*components)

    def compile(self, flags=0):
        return re.compile(self.regex, flags)


def main():

    word = OneOrMore(WORD)

    email_pattern = Regex(
        Capture(
            ZeroOrMore(
                word,
                ".",
            ),
            word,
        ),
        "@",
        Capture(word, OneOrMore(".", word), name="domain"),
    ).compile(re.IGNORECASE)

    print(email_pattern.pattern)

    name, domain = re.search(email_pattern, "my.name@example.com").groups()
    print(name, domain)


if __name__ == "__main__":
    main()
