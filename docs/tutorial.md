# Tutorial

Here is a demo to showcase the use of PyRegexBuilder.

## Problem

Hidden in the `text` below is a Cyrillic letter that is preceded by no more or less than 2 Greek or Latin letters.

```python
text = "ウثイا月εЗ人水جИ山γבИЖㄱتאEイЖבИBДE人ججイEㄷجاجㄷアЗاجاㄴACㄴDAエβエЖאג月水水ㄹجAㅁDبエα山הبتウИג月Aاイب山αثㄴاИδㄹ水ア人ㄹتεדβE山ㄴבㅁEאЙエㄷ山אباγجウㄹثㅁEЗИ日山イ日ثاㄷβBAㅁЖ水ㅁ山日水ㅁ人Иオבㄴγב月ت月اβアהγبβㄱبИㄱبオتㅁエ水αEتㄷAアדㄱبדDדㄱエㄹ水ثД山ㄱباイβاイ水δㄹЗㄹ月γB山ЗAアイαEИبДجЖεتИγㅁאاオㄷDЙアEεイㄹAثЖדD日山日δδDИCب月ЗבαتγウЖדبج日גBبהイㄱㅁ月月月ЖجBㄱגエבДجבㄱㅁㄱ人"
```

Which letter is it? Can you find it using a regular expression?

## Solution

Let's see how we would go about coming up with a solution using PyRegexBuilder.

1. Import the required modules.

    ```python
    from pyregexbuilder import *
    import regex as re
    ```

2. Create a character set that will match Greek or Latin letters.

    ```python
    greek_or_latin = PosixClass("IsGreek").union(UnicodeClass("IsLatin"))
    ```

3. Now let's start constructing the regular expression.

    ```python
    greek_or_latin = PosixClass("IsGreek").union(UnicodeClass("IsLatin"))

    expression = (
        Regex(
            ...
        )
    )
    ```

4. Create an assertion to check that only the previous 2 characters are Greek or Latin letters.

    ```python
    greek_or_latin = PosixClass("IsGreek").union(UnicodeClass("IsLatin"))

    expression = (
        Regex(
            PositiveLookbehind(
                greek_or_latin.inverted,
                Repeat(greek_or_latin, count=2)
            )
        )
    )
    ```

5. After looking behind, capture the current letter if it is part of the Cyrillic alphabet.

    ```python
    greek_or_latin = PosixClass("IsGreek").union(UnicodeClass("IsLatin"))

    expression = (
        Regex(
            PositiveLookbehind(
                ...
            ),
            Capture(PosixClass("IsCyrillic"), name="character"),
        )
    )
    ```

6. Set the flags for the regular expression and compile.

    ```python
    greek_or_latin = PosixClass("IsGreek").union(UnicodeClass("IsLatin"))

    expression = (
        Regex(
            ...
        )
        .with_global_flags({"VERSION1": True})
        .compile()
    )
    ```

7. Now you can use the regular expression. Here is the full code:

    ```python
    from pyregexbuilder import *
    import regex as re

    text = "ウثイا月εЗ人水جИ山γבИЖㄱتאEイЖבИBДE人ججイEㄷجاجㄷアЗاجاㄴACㄴDAエβエЖאג月水水ㄹجAㅁDبエα山הبتウИג月Aاイب山αثㄴاИδㄹ水ア人ㄹتεדβE山ㄴבㅁEאЙエㄷ山אباγجウㄹثㅁEЗИ日山イ日ثاㄷβBAㅁЖ水ㅁ山日水ㅁ人Иオבㄴγב月ت月اβアהγبβㄱبИㄱبオتㅁエ水αEتㄷAアדㄱبדDדㄱエㄹ水ثД山ㄱباイβاイ水δㄹЗㄹ月γB山ЗAアイαEИبДجЖεتИγㅁאاオㄷDЙアEεイㄹAثЖדD日山日δδDИCب月ЗבαتγウЖדبج日גBبהイㄱㅁ月月月ЖجBㄱגエבДجבㄱㅁㄱ人"

    greek_or_latin = PosixClass("IsGreek").union(UnicodeClass("IsLatin"))

    expression = (
        Regex(
            PositiveLookbehind(
                greek_or_latin.inverted,
                Repeat(
                    greek_or_latin,
                    count=2,
                )
            ),
            Capture(PosixClass("IsCyrillic"), name="character"),
        )
        .with_global_flags({"VERSION1": True})
        .compile()
    )

    match = re.search(expression, text)

    letter = match.groupdict()["character"]
    ```
