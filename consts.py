"""
A list of 64 lists, following a specific pattern of spaced repetitions.
Each index contains a subset of the 7 levels a byte can progress through.
Every day accesses a subsequent index in the levelRing (as determined by
the difference between 'today' and the constant ZERODAY), so every day
you will be quizzed on the active bytes whose levels correspond to that day's index.

i.e. if today's index is 3, you will only see bytes with levels 4 and 1.
"""
from datetime import date

level_rings = [
    [2, 1],
    [3, 1],
    [2, 1],
    [4, 1],
    [2, 1],
    [3, 1],
    [2, 1],
    [1],
    [2, 1],
    [3, 1],
    [2, 1],
    [5, 1],
    [4, 2, 1],
    [3, 1],
    [2, 1],
    [1],
    [2, 1],
    [3, 1],
    [2, 1],
    [4, 1],
    [2, 1],
    [3, 1],
    [2, 1],
    [6, 1],
    [2, 1],
    [3, 1],
    [2, 1],
    [5, 1],
    [4, 2, 1],
    [3, 1],
    [2, 1],
    [1],
    [2, 1],
    [3, 1],
    [2, 1],
    [4, 1],
    [2, 1],
    [3, 1],
    [2, 1],
    [1],
    [2, 1],
    [3, 1],
    [2, 1],
    [5, 1],
    [4, 2, 1],
    [3, 1],
    [2, 1],
    [1],
    [2, 1],
    [3, 1],
    [2, 1],
    [4, 1],
    [2, 1],
    [3, 1],
    [2, 1],
    [7, 1],
    [2, 1],
    [3, 1],
    [6, 2, 1],
    [5, 1],
    [4, 2, 1],
    [3, 1],
    [2, 1],
    [1],
]

ZERODAY = date(2019, 4, 1)
LEVEL = 'level'
QUESTION = 'question'
ANSWER = 'answer'
LAST_SEEN = 'last_seen'
