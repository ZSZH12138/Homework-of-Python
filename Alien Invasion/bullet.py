import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.color=self.settings.bullet_color
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,
                              self.settings.bullet_height)
        # 这样子弹上部的中央将和飞船上部中央对齐
        self.rect.midtop=ai_game.ship.rect.midtop
        self.y=float(self.rect.y)
    
    def update(self):
        """根据子弹的速度对飞船发射的子弹进行移位"""
        self.y-=self.settings.bullet_speed
        self.rect.y=self.y
    
    def draw_bullet(self):
        """画出子弹"""
        pygame.draw.rect(self.screen,self.color,self.rect)
        