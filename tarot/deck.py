# tarot/deck.py

import random
from .card import Card, Suit

class Deck:
    def __init__(self):
        self.cards = []

    def _create_deck(self):
        cards = []
        for suit in [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]:
            for rank in range(1, 15):
                cards.append(Card(suit, rank))
        for rank in range(1, 22):
            cards.append(Card(Suit.TRUMP, rank))
        cards.append(Card(Suit.FOOL, 0))
        return cards

    def shuffle_new_session(self, seed=None):
        """Start a new training session with a fresh, shuffled deck."""
        self.cards = self._create_deck()
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.cards)

    def cut(self, num_players):
        """Simulate cutting the remaining deck."""
        cut_point = random.randint(num_players, len(self.cards) - num_players)
        self.cards = self.cards[cut_point:] + self.cards[:cut_point]

    def deal(self, num_players=4):
        """Deal one game with proper cut and randomly assigned chien cards."""
        if num_players not in [3, 4, 5]:
            raise ValueError("Only 3, 4, or 5 players are supported.")

        chien_size = {3: 6, 4: 6, 5: 3}[num_players]
        deal_size = {3: 4, 4: 3, 5: 3}[num_players]
        self.cut(num_players)

        deck = self.cards.copy()
        chien_indices = set(random.sample(range(78), chien_size))
        chien = []
        hands = [[] for _ in range(num_players)]

        player = 0
        i = 0  # Index in deck
        while i < 78:
            k = 0
            packet = []
            while k < deal_size and i < 78:
                if i in chien_indices:
                    chien.append(deck[i])
                else:
                    packet.append(deck[i])
                    k += 1
                i += 1
            hands[player].extend(packet)
            player = (player + 1) % num_players

        assert sum(len(h) for h in hands) + len(chien) == 78
        assert len(chien) == chien_size

        return hands, chien
    
    def __repr__(self):
        rep = "Deck:\n"
        for i, card in enumerate(self.cards):
            rep += f"{i + 1}: {card}\n"
        return rep
    
    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self.cards)
    
    def add_card(self, card):
        """Add a card to the deck."""
        self.cards.append(card)