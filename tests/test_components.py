from .context import Capture, Reference, Atomic, ChoiceOf, Regex
import regex as re


TEST_TEXT = """
KIND      DATE          INSTITUTION                AMOUNT
----------------------------------------------------------------
CREDIT    03/01/2022    Payroll from employer      $200.23
CREDIT    03/03/2022    Suspect A                  $2,000,000.00
DEBIT     03/03/2022    Ted's Pet Rock Sanctuary   $2,000,000.00
DEBIT     03/05/2022    Doug's Dugout Dogs         $33.27
DEBIT     06/03/2022    Oxford Comma Supply Ltd.   £57.33
"""


class TestGroups:
    def test_capture(self):
        regex = Regex(Capture(ChoiceOf("CREDIT", "DEBIT")))
        result = re.findall(regex.compile(), TEST_TEXT)

        assert result == ["CREDIT", "CREDIT", "DEBIT", "DEBIT", "DEBIT"]

    def test_named_capture(self):
        regex = Regex(Capture(ChoiceOf("CREDIT", "DEBIT"), name="payment_type"))
        result = re.search(regex.compile(), TEST_TEXT)

        assert result.capturesdict() == {"payment_type": ["CREDIT"]}

    def test_reference(self):
        pass

    def test_atomic(self):
        pass


class TestCharacterClasses:
    pass
