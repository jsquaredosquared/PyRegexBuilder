from common import RegexComponent


class Capture(RegexComponent):
    def __init__(self, *components: str | RegexComponent, name: str | None = None):
        if name:
            self.regex = rf"(?P<{name}>{self.parse(*components)})"
        else:
            self.regex = rf"({self.parse(*components)})"


class Reference(RegexComponent):
    def __init__(self, name: str) -> None:
        self.regex = rf"(?P={name})"


class Atomic(RegexComponent):
    def __init__(self, *components: str | RegexComponent) -> None:
        self.regex = rf"(?>{self.parse(*components)})"
