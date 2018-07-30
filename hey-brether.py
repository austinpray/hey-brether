#!/usr/bin/env python3

import sys
from typing import List

def form_letter(letter: str) -> tuple:
    parts = [f':z_{letter}_{i}:' for i in range(4)]
    return ''.join(parts[:2]), ''.join(parts[2:])


def form_word(word: str) -> str:
    lines = [' '.join([form_letter(s)[i] for s in word]) for i in range(2)]
    return '\n'.join(lines)


def hey_brether(words: List[str]) -> str:
    return '\n\n'.join([form_word(w) for w in words])


if __name__ == "__main__":
    print(hey_brether(sys.argv[1:]))
