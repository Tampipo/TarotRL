import json
from tarot.game import TarotGame
from tarot.random_player import RandomPlayer
from tarot.deck import Deck

def test_play_game():
    players = [RandomPlayer(f"Player {i}") for i in range(4)]
    print(players)
    deck = Deck()
    game = TarotGame(players, deck)
    game.play_game()
    game_data = game.get_game_data()

    with open('web_visualization/game_log.json', 'w') as f:
        json.dump(game_data, f, indent=4)

if __name__ == "__main__":
    test_play_game()
    print("Game simulation completed successfully. Game data saved to game_log.json")
    import os
    import subprocess
    # Open the visualization HTML file in the default web browser
    html_file_path = os.path.join(os.path.dirname(__file__), 'web_visualization', 'visualization.html')
    try:
        subprocess.run(['xdg-open', html_file_path], check=True)
        print(f"Opened {html_file_path} in default browser.")
    except FileNotFoundError:
        print("xdg-open command not found. Please open visualization.html manually.")
    except Exception as e:
        print(f"Error opening visualization.html: {e}")