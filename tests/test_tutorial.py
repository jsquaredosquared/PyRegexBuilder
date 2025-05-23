from pyregexbuilder import (
    Regex,
    PositiveLookbehind,
    Repeat,
    Capture,
    PosixClass,
    UnicodeClass,
)
import regex as re


def test_tutorial():
    text = "ウثイا月εЗ人水جИ山γבИЖㄱتאEイЖבИBДE人ججイEㄷجاجㄷアЗاجاㄴACㄴDAエβエЖאג月水水ㄹجAㅁDبエα山הبتウИג月Aاイب山αثㄴاИδㄹ水ア人ㄹتεדβE山ㄴבㅁEאЙエㄷ山אباγجウㄹثㅁEЗИ日山イ日ثاㄷβBAㅁЖ水ㅁ山日水ㅁ人Иオבㄴγב月ت月اβアהγبβㄱبИㄱبオتㅁエ水αEتㄷAアדㄱبדDדㄱエㄹ水ثД山ㄱباイβاイ水δㄹЗㄹ月γB山ЗAアイαEИبДجЖεتИγㅁאاオㄷDЙアEεイㄹAثЖדD日山日δδDИCب月ЗבαتγウЖדبج日גBبהイㄱㅁ月月月ЖجBㄱגエבДجבㄱㅁㄱ人"
    greek_or_latin = PosixClass("IsGreek").union(UnicodeClass("IsLatin"))

    expression = Regex(
        PositiveLookbehind(
            greek_or_latin.inverted,
            Repeat(
                greek_or_latin,
                count=2,
            ),
        ),
        Capture(PosixClass("IsCyrillic"), name="character"),
    ).compile()

    match = re.search(expression, text)

    letter = match.groupdict()["character"]

    assert letter == "\u0418"
