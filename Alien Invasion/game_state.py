class GameState:
    def __init__(self,ai_game,high_score):
        self.settings=ai_game.settings
        self.ai_game=ai_game
        self.high_score=high_score # high_score可能有值 从类外传进来 而不是设置为0
        self.reset_stats()
    
    def reset_stats(self):
        """每次重新启动游戏的时候都重新初始化以下数值"""
        self.ships_left=self.settings.ship_lim
        self.score=0
        self.level=1
        self.ai_game.ship.shield=True
        try:
            self.ai_game.sb.prep_shield() # 运行的时候 scoreboard依赖game_state game_state依赖scoreboard
            # 在运行这个的时候 可能score_board还没定义 此时就不需要再去更新主界面shield的值
            # 因为当score_board定义的时候 会自我初始化 此时shield也会被初始化
        except:
            return