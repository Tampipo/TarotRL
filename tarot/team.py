class Team:
    def __init__(self, name, players=None):
        self.name = name
        self.players = players if players is not None else []

    def add_player(self, player):
        self.players.append(player)

    def GetNoudlers(self):
        noudlers = 0 
        for player in self.players:
            for card in player.won_cards:
                if card.is_oudler():
                    noudlers += 1
        return noudlers

    def __iter__(self):
        return iter(self.players)
    
    def __len__(self):
        return len(self.players)
    
    def __str__(self):
        return ", ".join(player.name for player in self.players)
    
    def __repr__(self):
        return f"Team(players={self.players})"
