# tarot/player.py
from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.won_cards = []
        self.Fool = 0 # flag to indicate if the excuse needs to be given back at the end of the game 0 isn't -1 means it needs to give a card back, 1 needs it needs to get a card

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

    @abstractmethod
    def call_king(self):
        pass
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Player(name={self.name}, hand={self.hand}, won_cards={self.won_cards})"
    
    def give_fool_card(self, player):
        if len(self.won_cards) == 0:
            self.Fool = -1  # No cards to give back
            player.Fool = 1
        elif len(self.won_cards) > 0:
            card_given = False
            for card in self.won_cards:
                if card.is_low():
                    self.won_cards.remove(card)
                    player.won_cards.append(card)
                    card_given = True
                    break
            if not card_given:
                self.Fool = -1
                player.Fool = 1

    def has_king(self, suit):
        return any(card.suit == suit and card.rank == 14 for card in self.hand)

