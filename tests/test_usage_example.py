from .context import (
    Regex,
    Lookahead,
    NegativeLookbehind,
    NegativeLookahead,
    PositiveLookbehind,
    RegexString,
    Capture,
    Reference,
    Lookahead,
)

import regex as re

TEXT = """
αβγ$X$δζηk7x!Ωλℵ7x~€X£@x!好x坏,1234x5678;©x®₩X₩ΔxΣ¶x∞—x—£X£¥X¥
åxøπ€X£ç8x9αβxδ 123?!x,$X$ℵ?x~£X¥ µxnΔξτ:-x;5678😃x😉♠♣♦♤♥♫‼x@
ТxЖ☼x♫$X£w0x2!!x??##x##∑xπ7x€X$abcxdef09x87!!?x??!!♣x♥z1xY2q
mmxnn₩X₩opqrx☹x☻123x456€X£abcd?x!imxop!!44¥X₩lmnoqrstu123459
xyxz$X$ñáçö*x,7890€X£ABCD⟨x⟩12x34!!₩X₩qrstuvxw0-9€X$mnopqrst
😎x😄¹x²abc$X$Δλξ--x--%%x%%ΩΩxΩ1234€X£MNop!x?uvwxy₩X₩z9!!abc!?
pqrsx🌟x🌙£X$lmno!?xx€X£abcd789:-x:;uvw987qxz!!%%%x%%stuvwx123
0987xабвxгд₩X¥OPQRstxuv??%%lx!!12345zxyx…x…XYZ$X€abcd1234!@#
"""

# Find those x's surrounded by 2 different currency symbols

regex = Regex(
    PositiveLookbehind(Capture(RegexString("[[:currencySymbol:]]"))),
    RegexString("[Xx]"),
    Lookahead(RegexString(r"\p{Sc}")),
    NegativeLookahead(Reference(1)),
)

# re.findall()
