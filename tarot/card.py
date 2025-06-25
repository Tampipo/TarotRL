# tarot/card.py

from enum import Enum
from functools import total_ordering

class Suit(Enum):
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"
    TRUMP = "Trump"
    FOOL = "Fool"

@total_ordering
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
    
    def is_fool(self):
        return self.suit == Suit.FOOL

    def is_king(self):
        return self.rank == 14 and self.suit in {Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES}

    def __repr__(self):
        if self.suit == Suit.FOOL:
            return "Fool"
        return f"{self.rank} of {self.suit.value}"

    def __str__(self):
        # e.g., "11 of Hearts" or "1 of Trump"
        return f"{self.rank} of {self.suit.name.capitalize()}"
    
    def is_low(self):
        # Low cards are 1-10 for suits
        return self.rank <= 10 and self.suit in {Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES}
    
    def __eq__(self, other):
        return isinstance(other, Card) and (self.suit, self.rank) == (other.suit, other.rank)

    def __hash__(self):
        return hash((self.suit, self.rank))
    
    def __lt__(self, other):
        if self.suit == Suit.FOOL:
            return True  # Fool is always lowest
        if other.suit == Suit.FOOL:
            return False

        if self.suit == Suit.TRUMP and other.suit == Suit.TRUMP:
            return self.rank < other.rank
        if self.suit == Suit.TRUMP:
            return False  # Trumps are higher than suits
        if other.suit == Suit.TRUMP:
            return True

        if self.suit == other.suit:
            return self.rank < other.rank

        # Arbitrary suit ranking: Hearts < Diamonds < Clubs < Spades
        suit_order = {
            Suit.HEARTS: 0,
            Suit.DIAMONDS: 1,
            Suit.CLUBS: 2,
            Suit.SPADES: 3,
        }
        return suit_order[self.suit] < suit_order[other.suit]