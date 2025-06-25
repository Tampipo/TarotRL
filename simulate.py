from tarot.game import TarotGame
from tarot.random_player import RandomPlayer

def test_play_game():
    players = [RandomPlayer(f"Player {i}") for i in range(5)]
    print(players)
    game = TarotGame(players)
    game.play_game()

if __name__ == "__main__":
    test_play_game()
    print("Game simulation completed successfully.")