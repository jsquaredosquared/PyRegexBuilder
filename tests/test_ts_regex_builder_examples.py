from pyregexbuilder import (
    CharacterClass,
    Regex,
    Optionally,
    OneOrMore,
    ZeroOrMore,
    ChoiceOf,
    Anchor,
    Character,
)
import regex as re


def test_javascript_number_validation():
    sign = CharacterClass.any_of("+-")
    exponent = Regex(
        CharacterClass.any_of("eE"), Optionally(sign), OneOrMore(Character.DIGIT)
    )

    regex = Regex(
        Anchor.START_OF_STRING,
        Optionally(sign),
        ChoiceOf(
            Regex(
                OneOrMore(Character.DIGIT),
                Optionally(".", ZeroOrMore(Character.DIGIT)),
            ),
            Regex(".", OneOrMore(Character.DIGIT)),
        ),
        Optionally(exponent),
        Anchor.END_OF_STRING,
    ).compile()

    assert re.match(regex, "1.0e+27")
