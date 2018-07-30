#!/usr/bin/env python3
import sys

print((lambda builder:
       lambda words:
       '\n\n'.join([
           '\n'.join([
               ''.join([
                   builder(c, i)
                   for c in word for i in iA])
               for iA in [[0, 1], [2, 3]]])
           for word in words])
       )(lambda c, i: f':z_{c}_{i}:')(sys.argv[1:]))
