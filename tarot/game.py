# tarot/game.py

from .deck import Deck
from .player import Player
from .rules import RuleEngine
from .bid import Bid
from .card import Suit

class TarotGame:
    def __init__(self, players, dealer=0):
        self.players = players
        self.num_players = len(players)
        if self.num_players not in [3, 4, 5]:
            raise ValueError("Only 3, 4, or 5 players are supported.")
        names = [player.name for player in players]
        if len(set(names)) != len(names):
            raise ValueError("Player names must be unique.")
        self.deck = Deck()
        self.dealer = 0
        self.chien = []
        self.dealer = players[dealer].name
        self.taker = None
        self.discard = []
        self.trick = []
        self.history = []
        self.leading = self.players[0].name
        self.rule_engine = RuleEngine()
        print(f"Starting Tarot game with players: {[player.name for player in players]}")
    
    def initialize(self):
        if len(self.deck) == 0:
            self.deck.shuffle_new_session()
        hands, self.chien = self.deck.deal(len(self.players))
        for player, hand in zip(self.players, hands):
            player.receive_hand(hand)
        print(f"Chien cards: {self.chien}")
        print(f"Dealer: {self.dealer}")
        print("Initial hands:")
        for player in self.players:
            print(f"{player.name}: {player.hand}")
    

    def bidding_phase(self):
        current_highest_bid = Bid.PASS
        for player in self.players:
            bid = player.make_bid(current_highest_bid)
            if bid > current_highest_bid:
                current_highest_bid = bid
                self.taker = player
        self.taker.receive_chien(self.chien)
        return current_highest_bid
    
    def discard_phase(self):
        discard_count = {3: 6, 4: 6, 5: 3}[len(self.players)]
        self.discard = self.taker.make_discard(discard_count)

    def play_trick(self):
        self.trick = {}
        for player in self.players:
            legal_cards = self.rule_engine.legal_moves(player.hand, list(self.trick.values()))
            played_card = player.play_card(legal_cards)
            self.trick[player.name] = played_card
        self.history.append(self.trick)
        print(self.leading)
        winning_player_name, _ = RuleEngine.trick_winner(self.trick, self.leading)
        winning_player = self.players[self.get_player_index(winning_player_name)]
        self.leading = winning_player.name
        for key, card in self.trick.items():
            if  card.suit != Suit.FOOL:
                winning_player.win_card(card)
            else:
                self.players[self.get_player_index(key)].win_card(card)
                # Need to implement method to give another card than the fool

    def get_player_index(self, player_name):
        for i, player in enumerate(self.players):
            if player.name == player_name:
                return i
        raise ValueError(f"Player {player_name} not found in game.")
    

    def play_game(self):
        self.initialize()
        self.bidding_phase()
        self.discard_phase()

        while len(self.players[0].hand) > 0:
            self.play_trick()
            print(f"Trick played: {self.trick}")
            print(f"Winning player: {self.leading}")
            print("Number of tricks played:", len(self.history))
            print("Current hands:")
            for player in self.players:
                print(f"{player.name}: {player.hand}")  

        