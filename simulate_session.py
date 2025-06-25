from tarot.session import TarotSession
from tarot.random_player import RandomPlayer
from tarot.naive_player import NaivePlayer

def simulate_session():
    players = [NaivePlayer(f"Player {i}") for i in range(3)]
    players.extend([RandomPlayer(f"Random Player {i}") for i in range(3,5)])
    session = TarotSession(players, ngames=1000)
    
    session.run()
    
    print("Session simulation completed successfully.")
    print(f"Final scores: {session.scores}")

if __name__ == "__main__":
    simulate_session()
    print("Session simulation completed successfully.")