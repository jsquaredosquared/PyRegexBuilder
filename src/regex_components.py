import re
from abc import ABC


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


class SpecialSequence(RegexComponent):
    def __init__(self, sequence: str) -> None:
        self.regex = sequence


class One(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = rf"(?:{self.parse(*components)}){1}"


class Optionally(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = rf"(?:{self.parse(*components)})?"


class ZeroOrMore(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = rf"(?:{self.parse(*components)})*"


class OneOrMore(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = rf"(?:{self.parse(*components)})+"


class Repeat(RegexComponent):
    def __init__(
        self,
        *components,
        count: int | None = None,
        minimum: int | None = None,
        maximum: int | None = None,
    ) -> None:
        if (count and (minimum or maximum)) or not (any((count, minimum, maximum))):
            raise RegexBuilderException()

        if count:
            self.regex = rf"(?:{self.parse(*components)}{{{count}}})"
        else:
            m = minimum if minimum else ""
            n = maximum if maximum else ""
            self.regex = rf"(?:{self.parse(*components)}){{{m},{n}}}"


class Capture(RegexComponent):
    def __init__(self, *components: str | RegexComponent, name: str | None = None):
        if name:
            self.regex = rf"(?P<{name}>{self.parse(*components)})"
        else:
            self.regex = rf"({self.parse(*components)})"


ANY = SpecialSequence(r".")
START_OF_STRING = SpecialSequence(r"^")
END_OF_STRING = SpecialSequence(r"$")
WORD = SpecialSequence(r"\w")
WORD_BOUNDARY = SpecialSequence(r"\b")
WHITESPACE = SpecialSequence(r"\s")
DIGIT = SpecialSequence(r"\d")


class ChoiceOf(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = rf"{'|'.join(self.parse(component) for component in components)}"


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
