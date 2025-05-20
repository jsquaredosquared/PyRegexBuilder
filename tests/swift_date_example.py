from src.pyregexbuilder import (
    Regex,
    Capture,
    ChoiceOf,
    OneOrMore,
    Repeat,
    RegexString,
    WHITESPACE,
    DIGIT,
)
import regex as re
import arrow

ledger = """
KIND      DATE          INSTITUTION                AMOUNT
----------------------------------------------------------------
CREDIT    03/01/2022    Payroll from employer      $200.23
CREDIT    03/03/2022    Suspect A                  $2,000,000.00
DEBIT     03/03/2022    Ted's Pet Rock Sanctuary   $2,000,000.00
DEBIT     03/05/2022    Doug's Dugout Dogs         $33.27
DEBIT     06/03/2022    Oxford Comma Supply Ltd.   £57.33
"""

field_separator = RegexString(r"\s{2,}|\t")

regex = re.compile(
    r"""
    (?<date>     \d{2} / \d{2} / \d{4})
    (?<middle>   \P{currencySymbol}+)
    (?<currency> \p{currencySymbol})
    """,
    re.VERBOSE,
)


def date_replace(regex_match: re.Match[str]) -> str:
    groups = regex_match.groupdict()
    new_date: str = ""
    match groups["currency"]:
        case "$":
            new_date = str(
                arrow.get(groups["date"], locale="en_US", tzinfo="GMT").date()
            )
        case "£":
            new_date = str(
                arrow.get(groups["date"], locale="en_UK", tzinfo="GMT").date()
            )
        case _:
            raise Exception("We found another one!")

    return new_date + groups["middle"] + groups["currency"]


print(re.sub(regex, date_replace, ledger))
