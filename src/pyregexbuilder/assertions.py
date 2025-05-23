from .common import RegexComponent


class Lookahead(RegexComponent):
    """
    Creates a lookahead assertion.

    Regex: `(?=...)`
    """

    def __init__(self, *components: str | RegexComponent) -> None:
        self._regex = rf"(?={self.parse(*components)})"


class NegativeLookahead(RegexComponent):
    """
    Creates a negative lookahead assertion.

    Regex: `(?!...)`
    """

    def __init__(self, *components: str | RegexComponent) -> None:
        self._regex = rf"(?!{self.parse(*components)})"


class PositiveLookbehind(RegexComponent):
    """
    Creates a positive lookbehind assertion.

    Regex: `(?<=...)`
    """

    def __init__(self, *components: str | RegexComponent) -> None:
        self._regex = rf"(?<={self.parse(*components)})"


class NegativeLookbehind(RegexComponent):
    """
    Creates a negative lookbehind assertion.

    Regex: `(?<!...)`
    """

    def __init__(self, *components: str | RegexComponent) -> None:
        self._regex = rf"(?<!{self.parse(*components)})"
