


class Scores:

    @staticmethod
    def calculate_scores(game):
        """
        Calculate scores for all players based on the game state.
        This method should be called at the end of a game round.
        """
        scores = {}
        for player in game.players:
            scores[player.name] = Scores.calculate_player_score(player, game)
        return scores
    
    @staticmethod
    def calculate_player_score(player):
        """
        Calculate the score for a single player based on their won cards and the game rules.
        """
        score = 0
        for card in player.won_cards:
            score += Scores.calculate_score_card(card)
        return score
    
    @staticmethod
    def calculate_score_card(card):
        """
        Calculate the score for a single card based on its type.
        """
        if card.is_oudler():
            return 4.5
        elif card.is_trump() or card.is_low():
            return 0.5
        elif card.rank == 11:
            return 1.5
        elif card.rank == 12:
            return 2.5
        elif card.rank == 13:
            return 3.5
        elif card.rank == 14:
            return 4.5
        else:
            return 0.5
        
    def calculate_team_score(team):
        """
        Calculate the score for a team based on the scores of its players.
        """
        total_score = 0
        for player in team.players:
            total_score += Scores.calculate_player_score(player)
        return total_score