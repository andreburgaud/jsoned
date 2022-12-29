"""JSON Lexer to faciliate color syntax"""

from dataclasses import dataclass
from enum import Enum, auto
import re


class TokenID(Enum):
    COLON = auto()
    COMMA = auto()
    LEFT_SQ_BRACKET = auto()
    RIGHT_SQ_BRACKET = auto()
    LEFT_CURL_BRACKET = auto()
    RIGHT_CURL_BRACKET = auto()
    KEY = auto()
    STRING = auto()
    INT = auto()
    BOOL = auto()
    NULL = auto()
    SPACE = auto


@dataclass
class Token:
    ID: TokenID
    pattern: re.Pattern


tokens = (
    Token(TokenID.COLON, re.compile(':')),
    Token(TokenID.COMMA, re.compile(',')),
    Token(TokenID.LEFT_SQ_BRACKET, re.compile(r'\[')),
    Token(TokenID.RIGHT_SQ_BRACKET, re.compile(']')),
    Token(TokenID.LEFT_CURL_BRACKET, re.compile(r'\{')),
    Token(TokenID.RIGHT_CURL_BRACKET, re.compile(r'}')),
    Token(TokenID.SPACE, re.compile(r'(\t|\n|\s|\r)+')),
    Token(TokenID.KEY, re.compile(r'"[^"\\]*(?:\\.[^"\\]*)*"(?=\s*:)')),
    Token(TokenID.STRING, re.compile(r'"[^"\\]*(?:\\.[^"\\]*)*"')),
    Token(TokenID.INT, re.compile(r'[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?')),
    Token(TokenID.BOOL, re.compile(r"true|false")),
    Token(TokenID.NULL, re.compile(r"null"))
)


def lexer(json_text) -> (TokenID, int, int):
    start = 0
    print(f"{len(json_text)=}")
    while start < len(json_text):
        print(f"{start=}")
        for token in tokens:
            if mo := token.pattern.match(json_text, start):
                end = mo.end(0)
                print(f"{mo.group(0)=}")
                yield token.ID, start, end
                start = end
                break
        else:
            print(f"{start=}")
            print(f"{json_text[start]=} NOT FOUND")
            start += 1
    else:
        yield None, 0, 0
