#!/usr/bin/env python3

# FYI this is a joke
# but it actually works LMFAO

import sys

if __name__ == "__main__":
    print(
        '\n\n'.join([
            '\n'.join([
                ' '.join([
                    (
                        ''.join([f':z_{letter}_{i}:' for i in range(4)][:2]),
                        ''.join([f':z_{letter}_{i}:' for i in range(4)][2:])
                    )[i] for letter in word
                ]) for i in range(2)
            ]) for word in sys.argv[1:]
        ])
    )
