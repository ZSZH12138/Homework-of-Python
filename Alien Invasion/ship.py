import pygame
from pygame.sprite import Sprite
import pygame.font

class Ship(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.settings=ai_game.settings
        self.image=pygame.image.load("images/ship.bmp")
        self.rect=self.image.get_rect()
        self.rect.midbottom=self.screen_rect.midbottom
        self.shield=True
        # 本处因为ship_speed是一个浮点数 但是rect.x只能是整数
        # 直接用rect.x会导致小数位消失 所以使用x来进行计算
        # 最后将整数位返回给rect.x
        self.x=float(self.rect.x)
        self.moving_right=False
        self.moving_left=False

    def update(self):
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.x+=self.settings.ship_speed
        if self.moving_left and self.rect.left>0:
            self.x-=self.settings.ship_speed
        self.rect.x=self.x

    def blitme(self):
        self.screen.blit(self.image,self.rect)
    
    def center_ship(self):
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)