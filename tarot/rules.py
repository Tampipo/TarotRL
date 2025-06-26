# tarot/rules.py
from .card import Suit

class RuleEngine:
    @staticmethod    
    def legal_moves(player_hand, trick_so_far, leading_player_name):
        # Find all Fool cards in hand (adjust attribute as needed)
        fools = [c for c in player_hand if c.suit == Suit.FOOL]  
        if list(trick_so_far.values()) == []:
            # At start of trick, all cards including fool are legal
            return player_hand

        lead_card = trick_so_far[leading_player_name]
        lead_suit = lead_card.suit

        trumps = [c for c in player_hand if c.suit == Suit.TRUMP]
        follow_suit = [c for c in player_hand if c.suit == lead_suit]

        if follow_suit:
            legal = follow_suit
        elif trumps:
            trumps_in_trick = [c for c in list(trick_so_far.values()) if c.suit == Suit.TRUMP]
            if trumps_in_trick:
                highest_trump = max(c.rank for c in trumps_in_trick)
                overtrump = [c for c in trumps if c.rank > highest_trump]
                legal = overtrump if overtrump else trumps
            else:
                legal = trumps
        else:
            legal = player_hand

        # Always include Fool cards if any, even if not in legal by rules
        if fools:
            # Add fools to legal moves if not already present
            for fool_card in fools:
                if fool_card not in legal:
                    legal.append(fool_card)

        return legal

    @staticmethod
    def is_valid_discard(hand, discard):
        if len(discard) == 0:
            return False  # Must discard something

        discard_set = set(discard)
        if not discard_set.issubset(set(hand)):
            return False  # Can't discard cards you don't have

        # Separate suits
        trumps = [c for c in hand if c.suit == Suit.TRUMP]
        non_trumps = [c for c in hand if c.suit not in {Suit.TRUMP, Suit.FOOL}]

        # Check for forbidden discards
        for card in discard:
            # Never discard a King
            if card.rank == 14 and card.suit in {
                Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES
            }:
                return False
            # Never discard 21 or 1 of trump
            if (card.suit == Suit.TRUMP and card.rank in {1, 21}) or card.suit == Suit.FOOL:
                return False
            # (Excuse is allowed)

        # Check if trumps (except Excuse) were discarded while having non-trumps
        non_excuse_trumps_discarded = [
            c for c in discard if c.suit == Suit.TRUMP and c.rank not in {1, 21}
        ]
        if non_trumps and non_excuse_trumps_discarded:
            return False  # You had non-trumps, so cannot discard trumps

        return True
    
    @staticmethod
    def trick_winner(trick, leading_player):
        leading_card = trick[leading_player]
        winning_card = leading_card
        winning_player = leading_player
        for key, value in trick.items():
            if value.suit == winning_card.suit:
                if value.rank > winning_card.rank:
                    winning_card = value
                    winning_player = key
            elif value.suit == Suit.TRUMP:
                if value.rank > winning_card.rank:
                    winning_card = value
                    winning_player = key
        return winning_player, winning_card
            
    
