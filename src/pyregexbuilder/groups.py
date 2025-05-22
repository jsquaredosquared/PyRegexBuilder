from .common import RegexComponent


class Capture(RegexComponent):
    def __init__(self, *components: str | RegexComponent, name: str | None = None):
        if name:
            self._regex = rf"(?P<{name}>{self.parse(*components)})"
        else:
            self._regex = rf"({self.parse(*components)})"


class Reference(RegexComponent):
    def __init__(self, ref: str | int) -> None:
        self._regex = rf"\g<{ref}>"


class Atomic(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self._regex = rf"(?>{self.parse(*components)})"
