from regex_components import *
import re

test_text = """
KIND      DATE          INSTITUTION                AMOUNT
----------------------------------------------------------------
CREDIT    03/01/2022    Payroll from employer      $200.23
CREDIT    03/03/2022    Suspect A                  $2,000,000.00
DEBIT     03/03/2022    Ted's Pet Rock Sanctuary   $2,000,000.00
DEBIT     03/05/2022    Doug's Dugout Dogs         $33.27
DEBIT     06/03/2022    Oxford Comma Supply Ltd.   £57.33
"""

regex = Regex(
    Capture(
        ChoiceOf(
            "CREDIT",
            "DEBIT",
        ),
        name="payment_type",
    ),
    OneOrMore(WHITESPACE),
    Capture(
        Regex(
            Repeat(DIGIT, minimum=1, maximum=2),
            "/",
            Repeat(DIGIT, minimum=1, maximum=2),
            "/",
            Repeat(DIGIT, count=4),
        ),
        name="date",
    ),
).compile()

result = re.findall(regex, test_text)
print(result)

field_separator = Regex(RegexString(r"\s{2,}|\t")).compile()
replaced_with_tabs = re.sub(field_separator, r"\t", test_text)
print(replaced_with_tabs)