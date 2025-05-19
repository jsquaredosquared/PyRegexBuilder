import regex as re
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


class RegexString(RegexComponent):
    def __init__(self, string: str) -> None:
        self.regex = string


class Regex(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = self.parse(*components)

    def compile(self, flags=0):
        return re.compile(self.regex, flags)


class ChoiceOf(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = (
            rf"(?:{'|'.join(self.parse(component) for component in components)})"
        )
