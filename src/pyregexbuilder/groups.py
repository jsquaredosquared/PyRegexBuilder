from .common import RegexComponent


class Capture(RegexComponent):
    """
    A capture group. Can be named or unnamed.

    Regex: `(?P<name>...)` or `(...)`
    """

    def __init__(self, *components: str | RegexComponent, name: str | None = None):
        if name:
            self._regex = rf"(?P<{name}>{self.parse(*components)})"
        else:
            self._regex = rf"({self.parse(*components)})"


class Reference(RegexComponent):
    r"""
    A named or numbered reference to a previously captured group.

    Regex: `\g<...>`
    """

    def __init__(self, ref: str | int) -> None:
        self._regex = rf"\g<{ref}>"


class Atomic(RegexComponent):
    """
    An atomic group.
    """

    def __init__(self, *components: str | RegexComponent) -> None:
        self._regex = rf"(?>{self.parse(*components)})"


class BranchReset(RegexComponent):
    """
    A branch reset group.
    """

    def __init__(self, *components: str | RegexComponent) -> None:
        self._regex = rf"(?|{'|'.join(self.parse(*components))})"
