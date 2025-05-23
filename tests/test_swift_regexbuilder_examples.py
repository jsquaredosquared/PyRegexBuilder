from pyregexbuilder import Character, Regex, Capture, ZeroOrMore, OneOrMore
import regex as re


def test_homepage_example():
    word = OneOrMore(Character.WORD)
    email_pattern = Regex(
        Capture(
            ZeroOrMore(
                word,
                ".",
            ),
            word,
        ),
        "@",
        Capture(
            word,
            OneOrMore(
                ".",
                word,
            ),
        ),
    ).compile()

    text = "My email is my.name@example.com"

    if match := re.search(email_pattern, text):
        name, domain = match.groups()

    assert (name, domain) == ("my.name", "example.com")
