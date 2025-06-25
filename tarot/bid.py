# tarot/bid.py

from enum import IntEnum

class Bid(IntEnum):
    PASS = 0
    PETITE = 1
    GARDE = 2
    # Optional: GARDE_SANS = 3, GARDE_CONTRE = 4

    def __str__(self):
        return self.name.capitalize()
