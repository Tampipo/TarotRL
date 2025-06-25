import random
from .player import Player
from .card import Suit
from .rules import RuleEngine 
from .bid import Bid

class RandomPlayer(Player):
    def make_bid(self, current_highest_bid):
        # Randomly choose a bid, respecting the rules
        bids = [Bid.PASS, Bid.PETITE, Bid.GARDE]
        if random.random() < 0.1:
            bids.append(Bid.PASS)
        return random.choice(bids)

    def make_discard(self, discard_count):
        # Try random discards until valid
        while True:
            discard = random.sample(self.hand, discard_count)
            if RuleEngine.is_valid_discard(self.hand, discard):
                for card in discard:
                    self.hand.remove(card)
                self.won_cards.extend(discard)
                return discard

    def play_card(self, legal_cards):
        played_card = random.choice(legal_cards)
        self.hand.remove(played_card)
        return played_card


    def call_king(self):
        suits = [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]
        return random.choice(suits)