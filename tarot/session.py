from tarot.game import TarotGame
from tarot.deck import Deck


class TarotSession:
    def __init__(self, players, ngames=5):
        self.players = players
        self.deck = Deck()
        self.dealer = 0  # Default dealer index, can be changed later
        self.ngames = ngames
        self.current_game = 0
        self.games = []
        self.scores = {player.name: 0 for player in players}
        print(f"Starting Tarot session with {ngames} games and players: {[player.name for player in players]}")

    def update_deck(self):
        if len(self.games) > 0:
            last_game = self.games[-1]
            if last_game.deck:
                self.deck = last_game.get_deck_from_tricks()
        elif len(self.deck) == 0:
            self.deck.shuffle_new_session()
    
    def reset_players_states(self):
        for player in self.players:
            player.reset()

    
    def play_game(self):
        new_game = TarotGame(self.players, self.deck, dealer=self.dealer)
        new_game.play_game()
        self.games.append(new_game)
        self.current_game += 1
        self.dealer = (self.dealer + 1) % len(self.players)
        print(f"Game {self.current_game} played. Current scores: {self.scores}")

    def run(self):
        for _ in range(self.ngames):
            self.update_deck()
            self.reset_players_states()
            self.play_game()


        print("Session completed successfully.")
        print(f"Final scores: {self.scores}")

