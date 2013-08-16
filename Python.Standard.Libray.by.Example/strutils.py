# -*- coding: utf-8 -*- 
import sys
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





