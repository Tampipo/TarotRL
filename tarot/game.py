# tarot/game.py

import uuid
import json
from .deck import Deck
from .player import Player
from .rules import RuleEngine
from .bid import Bid
from .card import Suit
from .scores import Scores
from .team import Team

class TarotGame:
    def __init__(self, players, deck, dealer=0):
        self.players = players
        self.num_players = len(players)
        self.team1 = Team("Attack")
        self.team2 = Team("Defense")
        if self.num_players not in [3, 4, 5]:
            raise ValueError("Only 3, 4, or 5 players are supported.")
        names = [player.name for player in players]
        if len(set(names)) != len(names):
            raise ValueError("Player names must be unique.")
        self.deck = deck
        self.chien = []
        self.dealer = self.players[dealer]
        self.taker = None
        self.discard = []
        self.trick = []
        self.history = []
        self.leading = self.players[(dealer + 1) % self.num_players].name
        self.rule_engine = RuleEngine()
        print(f"Starting Tarot game with players: {[player.name for player in players]}")

        self.game_log = {
            "game_id": str(uuid.uuid4()),
            "players": [{"name": p.name, "type": p.__class__.__name__} for p in players],
            "dealer": self.dealer.name,
            "initial_hands": {},
            "bid_phase": {"bids": []},
            "chien": [],
            "discard_phase": {},
            "tricks": [],
            "final_scores": {}
        }
    
    def initialize(self):
        if len(self.deck) == 0:
            self.deck.shuffle_new_session()
        hands, self.chien = self.deck.deal(len(self.players))
        for player, hand in zip(self.players, hands):
            player.receive_hand(hand)
            self.game_log["initial_hands"][player.name] = [str(card) for card in hand]
        self.game_log["chien"] = [str(card) for card in self.chien]



    def finalize(self):
        # Check for fool exchanges required
        fool_needed = [player for player in self.players if player.Fool == 1]
        fool_return = [player for player in self.players if player.Fool == -1]
        if len(fool_needed) > 1 or len(fool_return) > 1:
            raise ValueError("Invalid Fool exchange state at game end.")
        if len(fool_needed) == 1 and len(fool_return) == 1:
            fool_needed[0].give_fool_card(fool_return[0])

        team1_score = sum(Scores.calculate_player_score(player) for player in self.team1)
        team2_score = sum(Scores.calculate_player_score(player) for player in self.team2)

        # Add points from the chien for GARDE_CONTRE
        if self.bid == Bid.GARDE_CONTRE:
            chien_score = sum(Scores.calculate_score_card(card) for card in self.chien)
            team2_score += chien_score
            self.team2.get_player(0).win_cards(self.chien)

        oudlers_team1 = self.team1.GetNoudlers()
        required_points = {0: 56, 1: 51, 2: 41, 3: 36}[oudlers_team1]

        difference = team1_score - required_points
        
        if difference >= 0:
            final_score = 25 + difference
        else:
            final_score = -25 + difference

        print(f"Team 1 score: {team1_score}")
        print(f"Team 2 score: {team2_score}")
        print(f"Oudlers team1: {oudlers_team1}")
        print(f"Required points: {required_points}")
        print(f"Difference: {difference}")
        print(f"Final score: {final_score}")

        self.game_log["final_scores"] = {
            "team1_score": team1_score,
            "team2_score": team2_score,
            "oudlers_team1": oudlers_team1,
            "required_points": required_points,
            "difference": difference,
            "final_score": final_score
        }

        return final_score

    def get_game_data(self):
        return self.game_log

    def call(self):
        print("Bid:", self.bid)
        print("Calling suit for the taker...")
        called_suit = self.taker.call_king()
        print(f"Called suit: {called_suit}")
        self.team1.add_player(self.taker)
        for player in self.players:
            if player.has_king(called_suit):
                if player != self.taker:
                    self.team1.add_player(player)
            else:
                if player != self.taker:
                    self.team2.add_player(player)

        print(f"Team 1: {self.team1}")
        print(f"Team 2: {self.team2}")


    def bidding_phase(self):
        index = self.players.index(self.dealer)
        bidding_order = self.players[index:] + self.players[:index]
        self.bid = Bid.PASS
        for player in bidding_order:
            bid = player.make_bid(self.bid)
            self.game_log["bid_phase"]["bids"].append({"player": player.name, "bid": str(bid)})
            if bid > self.bid:
                self.bid = bid
                self.taker = player
        
        if self.taker:
            self.game_log["bid_phase"]["taker"] = self.taker.name
            self.game_log["bid_phase"]["final_bid"] = str(self.bid)
            if self.bid == Bid.GARDE_SANS:
                for card in self.chien:
                    self.taker.win_card(card)
            elif self.bid < Bid.GARDE_SANS:
                self.taker.receive_chien(self.chien)

        return self.bid
    
    def discard_phase(self):
        if self.bid < Bid.GARDE_SANS:
            discard_count = {3: 6, 4: 6, 5: 3}[len(self.players)]
            self.discard = self.taker.make_discard(discard_count)
            self.game_log["discard_phase"]["taker_discarded_cards"] = [str(card) for card in self.discard]

    def play_trick(self):
        self.trick = {}
        players_order = self.players[self.get_player_index(self.leading):] + self.players[:self.get_player_index(self.leading)]
        current_trick_log = {
            "trick_number": len(self.game_log["tricks"]) + 1,
            "leading_player": self.leading,
            "cards_played": []
        }
        for player in players_order:
            legal_cards = self.rule_engine.legal_moves(player.hand, self.trick, self.leading)
            played_card = player.play_card(legal_cards)
            self.trick[player.name] = played_card
            current_trick_log["cards_played"].append({"player": player.name, "card": str(played_card)})
        self.history.append(self.trick)
        winning_player_name, _ = RuleEngine.trick_winner(self.trick, self.leading)
        winning_player = self.players[self.get_player_index(winning_player_name)]
        self.leading = winning_player.name
        current_trick_log["winner"] = winning_player.name
        self.game_log["tricks"].append(current_trick_log)
        for key, card in self.trick.items():
            if card.suit != Suit.FOOL:
                winning_player.win_card(card)
            else:
                self.players[self.get_player_index(key)].win_card(card)
                self.players[self.get_player_index(key)].give_fool_card(winning_player)

    def get_player_index(self, player_name):
        for i, player in enumerate(self.players):
            if player.name == player_name:
                return i
        raise ValueError(f"Player {player_name} not found in game.")
    

    def play_game(self):
        self.initialize()
        self.bidding_phase()
        if not self.taker:
            print("No taker was selected. Ending game.")
            return self.finalize()
        if self.num_players == 5:
            self.call()
        self.discard_phase()
        k=0
        while len(self.players[0].hand) > 0:
            self.play_trick()
        
        return self.finalize()

    def get_deck_from_tricks(self):
        """Extract all cards played in tricks to form a new deck."""
        deck = Deck()
        print(len(deck))
        for player in self.players:
            for card in player.won_cards:
                deck.add_card(card)
        print("Deck extracted with:", len(deck.cards), "cards.")
        return deck

        