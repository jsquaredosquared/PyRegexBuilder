from .common import RegexComponent


class Lookahead(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self._regex = rf"(?={self.parse(*components)})"


class NegativeLookahead(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self._regex = rf"(?!{self.parse(*components)})"


class PositiveLookbehind(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self._regex = rf"(?<={self.parse(*components)})"


class NegativeLookbehind(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self._regex = rf"(?<!{self.parse(*components)})"
