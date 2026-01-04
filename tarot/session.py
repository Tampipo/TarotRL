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
        self.N_players = len(players)
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
        final_score = new_game.final_score
        if final_score == 0:
            with open("test.txt", "w") as f:
                f.write(str(final_score))
        

        if new_game.taker is None:
            return  # No score update if no taker

        if self.N_players == 3:
            # The taker wins twice as much
            self.scores[new_game.taker.name] += final_score * 2
            for player in self.players:
                if player.name != new_game.taker.name:
                    self.scores[player.name] -= final_score
        if self.N_players == 4:
            # The taker wins three times as much
            self.scores[new_game.taker.name] += final_score * 3
            for player in self.players:
                if player.name != new_game.taker.name:
                    self.scores[player.name] -= final_score
        if self.N_players == 5:
            # Two cases, if the taker is alone he wins 4 times as much, if he is with a teammate the team mate wins 1, he wins 2
            if len(new_game.team1.players) == 1:
                self.scores[new_game.taker.name] += final_score * 4
                for player in self.players:
                    if player.name != new_game.taker.name:
                        self.scores[player.name] -= final_score
            else:
                for player in new_game.team1.players:
                    if player.name == new_game.taker.name:
                        self.scores[player.name] += final_score * 2
                    else:
                        self.scores[player.name] += final_score
                for player in new_game.team2.players:
                    self.scores[player.name] -= final_score

            

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

