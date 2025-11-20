class GameState:
    def __init__(self,ai_game,high_score):
        self.settings=ai_game.settings
        self.ai_game=ai_game
        self.high_score=high_score
        self.reset_stats()
    
    def reset_stats(self):
        self.ships_left=self.settings.ship_lim
        self.score=0
        self.level=1
        self.ai_game.ship.shield=True
        try:
            self.ai_game.sb.prep_shield()
        except:
            return