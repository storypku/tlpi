# -*- coding: utf-8 -*- 
from collections import namedtuple
import sys
import re

def combine(source, maxsize=4096):
    parts = []
    for part in source:
        parts.append(part)
        size += len(part)
        if size > maxsize:
            yield "".join(parts)
            parts = []
            size = 0
    yield "".join(parts)

class _safesub(dict):
    def __missing__(self, key):
        return "{" + key + "}"

def sub(text):  # P62, Python Cookbook, 3rd
    return text.format_map(_safesub(sys._getframe(1).f_locals))

_NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
_NUM = r'(?P<NUM>\d+)'
_PLUS = r'(?P<PLUS>\+)'
_TIMES = r'(?P<TIMES>\*)'
_GE = r'(?P<GE>\>=)'
_LE = r'(?P<LE><=)'
_GT = r'(?P<GT>\>)'
_LT = r'(?P<LT><)'
_EQ = r'(?P<EQ>=)'
_WS = r'(?P<WS>\s+)'

_regex = "|".join([_NAME, _NUM, _PLUS, _TIMES, _GE, _LE, _GT, _LT, _EQ, _WS])
ARITHMETIC_PAT = re.compile(_regex)

Token = namedtuple("Token", ["type_", "value"])

def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup, m.group())
        if tok.type_ != "WS": yield tok

text = "5 <= 3 >= 2 < 1 > 6"
for tok in generate_tokens(ARITHMETIC_PAT, text):
    print(tok)
