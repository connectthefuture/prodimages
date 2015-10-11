import timeit

setup = """
import re
patterns = [".*abc", "123.*", "ab.*", "foo.*bar", "11010.*", "1[^o]*"]*10
strings = ["asdabc", "123awd2", "abasdae23", "fooasdabar", "111", "11010100101", "xxxx", "eeeeee", "dddddddddddddd", "ffffff"]*10
compiled_patterns = list(map(re.compile, patterns))

def matches_pattern(str, patterns):
    for pattern in patterns:
        if pattern.match(str):
            return True
    return False

def test0():
    for s in strings:
        matches_pattern(s, compiled_patterns)

def test1():
    for s in strings:
        any(p.match(s) for p in compiled_patterns)

def test2():
    for s in strings:
        re.match('|'.join('(?:%s)' % p for p in patterns), s)

def test3():
    r = re.compile('|'.join('(?:%s)' % p for p in patterns))
    for s in strings:
        r.match(s)
"""

import sys
print(timeit.timeit("test0()", setup=setup, number=1000))
print(timeit.timeit("test1()", setup=setup, number=1000))
print(timeit.timeit("test2()", setup=setup, number=1000))
print(timeit.timeit("test3()", setup=setup, number=1000))