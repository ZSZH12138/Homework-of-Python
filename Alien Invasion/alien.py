import pygame
from pygame.sprite import Sprite,Group
from alien_bullet import AlienBullet
import random

class Alien(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.ai_game=ai_game
        self.screen=ai_game.screen
        self.shoot_time=0 # 上次发射子弹的时间
        self.image=pygame.image.load("images/alien.bmp")
        self.rect=self.image.get_rect()
        self.rect.x=self.rect.width
        self.bullets=Group()
        self.rect.y=self.rect.height
        self.x=float(self.rect.x)
        self.settings=ai_game.settings
        self.direction=self.settings.fleet_direction
        # 随机出一个子弹发射的时间间隔
        self.bullet_tr=random.randint(self.settings.alien_bullet_tr_up,self.settings.alien_bullet_tr_down)
        # 随机出一个外星人的速度
        self.speed=random.randint(self.settings.alien_speed_down,self.settings.alien_speed_up)
    
    def update(self):
        """外星人移动且检测时间是否已经达到了发射的时间间隔 如果达到了则发射子弹"""
        if pygame.time.get_ticks()-self.shoot_time>self.bullet_tr:
            ab=AlienBullet(self.ai_game,self.rect.midbottom)
            self.bullets.add(ab)
            self.shoot_time=pygame.time.get_ticks()
        self.x+=self.speed*self.direction
        self.rect.x=self.x
    
    def check_edges(self):
        """检测外星人是否已经到达左右边界"""
        screen_rect=self.screen.get_rect()
        return self.rect.right>=screen_rect.right or self.rect.left<=0