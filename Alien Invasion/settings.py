class Settings:
    def __init__(self):
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(173,216,230)
        self.ship_lim=3
        self.bullet_width=3
        self.bullet_height=15
        self.alien_bullet_width=3
        self.alien_bullet_height=15
        self.bullet_color=(60,60,60)
        self.alien_bullet_color=(255,0,0)
        self.bullet_allowed=3
        self.fleet_drop_speed=10
        self.fleet_direction=1
        self.speedup_scale=1.1
        self.score_scale=1.5
        self.alien_bullet_tr_up=200
        self.alien_bullet_tr_down=2000
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed=1.5
        self.bullet_speed=10.0
        self.alien_bullet_speed=10.0
        self.alien_speed_up=50
        self.alien_speed_down=5
        self.alien_points=50

    def increase_speed(self):
        """每次按一定份额给游戏加速"""
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        # 因为随机数我用的是randint 所以这里的边界必须是int
        self.alien_speed_up=int(self.speedup_scale*self.alien_speed_up)
        self.alien_speed_down=int(self.speedup_scale*self.alien_speed_down)
        self.alien_bullet_speed*=self.speedup_scale
        self.alien_points=int(self.alien_points*self.score_scale)