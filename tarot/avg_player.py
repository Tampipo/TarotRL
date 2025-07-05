import random
from .player import Player
from .card import Suit
from .rules import RuleEngine 
from .bid import Bid

class AvgPlayer(Player):
    def make_bid(self, current_highest_bid):
        bids = [Bid.PASS, Bid.PETITE, Bid.GARDE, Bid.GARDE_SANS, Bid.GARDE_CONTRE]
        n_strong_cards = 0
        for card in self.hand:
            if card.is_oudler():
                n_strong_cards += 1
            if not card.is_trump() and card.rank == 14: #king
                n_strong_cards += 1
        if n_strong_cards >= 3:
            for bid in bids:
                if bid > current_highest_bid:
                    return bid
        else:
            return Bid.PASS

    def make_discard(self, discard_count):
        # Try random discards until valid
        possible_cards = [card for card in self.hand if not (card.is_oudler() or card.is_trump() or card.is_king())]
        if len(possible_cards) < discard_count:
            possible_cards = [card for card in self.hand if not (card.is_oudler() or card.is_trump())]
        if len(possible_cards) < discard_count:
            possible_cards = [card for card in self.hand if not (card.is_oudler())]
        discard = sorted(possible_cards)[:discard_count]
        if RuleEngine.is_valid_discard(self.hand, discard):
            for card in discard:
                self.hand.remove(card)
            self.won_cards.extend(discard)
            return discard
        else:
            print(f"Invalid discard: {discard} from hand: {self.hand}, should not happen in NaivePlayer")
            return []
        
    def play_card(self, legal_cards):
        lowest_card = min(legal_cards)
        self.hand.remove(lowest_card)
        return lowest_card
    
    def call_king(self):
        # Call the king of the suit with the smallest number of cards in hand
        suit_counts = {suit: 0 for suit in Suit}
        for card in self.hand:
            if not card.is_oudler() and not card.is_trump():
                suit_counts[card.suit] += 1
        min_suit = min(suit_counts, key=suit_counts.get)
        return min_suit