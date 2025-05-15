import re
from abc import ABC


class RegexBuilderException(Exception):
    pass


class Component(ABC):
    regex: str

    def parse(self, *components):
        return "".join(
            (
                component.regex
                if isinstance(component, Component)
                else re.escape(component)
            )
            for component in components
        )


class SpecialSequence(Component):
    def __init__(self, sequence):
        self.regex = sequence


class One(Component):
    def __init__(self, *components):
        self.regex = rf"(?:{self.parse(*components)}){1}"


class ZeroOrOne(Component):
    def __init__(self, *components):
        self.regex = rf"(?:{self.parse(*components)})?"


class ZeroOrMore(Component):
    def __init__(self, *components) -> None:
        self.regex = rf"(?:{self.parse(*components)})*"


class OneOrMore(Component):
    def __init__(self, *components) -> None:
        self.regex = rf"(?:{self.parse(*components)})+"


class Repeat(Component):
    def __init__(
        self,
        *components,
        number: int | None = None,
        minimum: int | None = None,
        maximum: int | None = None,
    ):
        if (number and (minimum or maximum)) or not (any((number, minimum, maximum))):
            raise RegexBuilderException()

        if number:
            self.regex = rf"(?:{self.parse(*components)}{{{number}}})"
        else:
            m = minimum if minimum else ""
            n = maximum if maximum else ""
            self.regex = rf"(?:{self.parse(*components)}){{{m},{n}}}"


class Capture(Component):
    def __init__(self, *components, name: str | None = None):
        if name:
            self.regex = rf"(?<{name}>{self.parse(*components)})"
        else:
            self.regex = rf"({self.parse(*components)})"


WORD = SpecialSequence(r"\w")


class Regex(Component):
    def __init__(self, *components) -> None:
        self.regex = self.parse(*components)

    def compile(self):
        return re.compile(self.regex)


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
        Capture(word, OneOrMore(".", word)),
    ).compile()

    print(email_pattern.pattern)

    name, domain = re.search(email_pattern, "my.name@example.com").groups()
    print(name, domain)


if __name__ == "__main__":
    main()
