# tarot/game.py

from .deck import Deck
from .player import Player
from .rules import RuleEngine
from .bid import Bid
from .card import Suit
from .scores import Scores
from .team import Team

class TarotGame:
    def __init__(self, players, dealer=0):
        self.players = players
        self.num_players = len(players)
        self.team1 = Team("Attack")
        self.team2 = Team("Defense")
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


    def finalize(self):
        # Check for fool exchanges required
        fool_needed = [player for player in self.players if player.Fool == 1 ]
        fool_return =  [player for player in self.players if player.Fool == -1]
        if len(fool_needed) > 1 or len(fool_return) > 1:
            raise ValueError("Invalid Fool exchange state at game end.")
        if len(fool_needed) == 1 and len(fool_return) == 1:
            fool_needed[0].give_fool_card(fool_return[0])
        tot = 0
        for player in self.players:
            tot += Scores.calculate_player_score(player)
            print(f"{player.name} score: {Scores.calculate_player_score(player)}")

        print(f"Total score: {tot}")

        if self.num_players ==  5:
            print(self.team1)
            print(self.team2)
            team1_score = sum(Scores.calculate_player_score(player) for player in self.team1)
            team2_score = sum(Scores.calculate_player_score(player) for player in self.team2)
            print(f"Team 1 score: {team1_score}")
            print(f"Team 2 score: {team2_score}")
            print(f"Noudlers team1: {self.team1.GetNoudlers()}")
            print(f"Noudlers team2: {self.team2.GetNoudlers()}")
        
    def call(self):
        print("Calling suit for the taker...")
        called_suit = self.taker.call_king()
        print(f"Called suit: {called_suit}")
        self.team1.add_player(self.taker)
        print(self.taker)
        print(id(self.team1))
        print(id(self.team2))
        for player in self.players:
            if player.has_king(called_suit):
                print("Ok")
                if player != self.taker:
                    self.team1.add_player(player)
                    print(self.team1)
                    print(self.team2)
            else:
                if player != self.taker:
                    self.team2.add_player(player)
                    print(self.team2)
                    print(self.team1)


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
        # print(self.leading)
        winning_player_name, _ = RuleEngine.trick_winner(self.trick, self.leading)
        winning_player = self.players[self.get_player_index(winning_player_name)]
        self.leading = winning_player.name
        for key, card in self.trick.items():
            if  card.suit != Suit.FOOL:
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
        if self.num_players == 5:
            self.call()
        self.discard_phase()

        while len(self.players[0].hand) > 0:
            self.play_trick()
            # print(f"Trick played: {self.trick}")
            # print(f"Winning player: {self.leading}")
            # print("Number of tricks played:", len(self.history))
            # print("Current hands:")
            # for player in self.players:
            #     print(f"{player.name}: {player.hand}")  
        
        self.finalize()

        