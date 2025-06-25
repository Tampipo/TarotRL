# tarot/player.py
from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.won_cards = []

    def receive_hand(self, hand):
        self.hand = hand

    def receive_chien(self, chien):
        self.hand.extend(chien)

    def win_card(self, card):
        self.won_cards.append(card)

    @abstractmethod
    def make_bid(self, current_highest_bid):
        pass

    @abstractmethod
    def make_discard(self, discard_count):
        pass

    @abstractmethod
    def play_card(self, trick, legal_cards):
        pass
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Player(name={self.name}, hand={self.hand}, won_cards={self.won_cards})"