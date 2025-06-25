# test_tarot.py
import pytest
from .card import Card, Suit


def test_card_creation():
    card = Card(Suit.HEARTS, 10)
    assert card.suit == Suit.HEARTS
    assert card.rank == 10
    assert card.is_oudler() is False
    assert card.is_trump() is False

    card = Card(Suit.TRUMP, 1)
    assert card.suit ==  Suit.TRUMP
    assert card.rank == 1
    assert card.is_oudler() is True
    assert card.is_trump() is True

    card = Card(Suit.FOOL, 0)
    assert card.suit ==  Suit.FOOL
    assert card.rank == 0
    assert card.is_oudler() is True
    assert card.is_trump() is False


def test_play_game():
    from .game import TarotGame
    from .random_player import RandomPlayer

    players = [RandomPlayer(f"Player {i}") for i in range(4)]
    print(players)
    game = TarotGame(players)
    game.play_game()