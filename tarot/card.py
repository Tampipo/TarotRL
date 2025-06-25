# tarot/card.py

from enum import Enum

class Suit(Enum):
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"
    TRUMP = "Trump"
    FOOL = "Fool"

class Card:
    def __init__(self, suit: Suit, rank: int):
        self.suit = suit
        self.rank = rank  # 1-14 for suits, 1-21 for trumps, 0 for Fool

    def is_trump(self):
        return self.suit == Suit.TRUMP

    def is_oudler(self):
        return (
            self.suit == Suit.FOOL or
            (self.suit == Suit.TRUMP and self.rank in [1, 21])
        )

    def __repr__(self):
        if self.suit == Suit.FOOL:
            return "Fool"
        return f"{self.rank} of {self.suit.value}"

    def __str__(self):
        # e.g., "11 of Hearts" or "1 of Trump"
        return f"{self.rank} of {self.suit.name.capitalize()}"