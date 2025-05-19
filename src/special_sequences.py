from common import RegexString

ANY = RegexString(r".")

START_OF_STRING = RegexString(r"^")
END_OF_STRING = RegexString(r"$")
WORD_BOUNDARY = RegexString(r"\b")

DIGIT = RegexString(r"\d")
NOT_DIGIT = RegexString(r"\D")
WHITESPACE = RegexString(r"\s")
NOT_WHITESPACE = RegexString(r"\S")
WORD = RegexString(r"\w")
NOT_WORD = RegexString(r"\W")
