import pygame.font
from pygame.sprite import Group
from ship import Ship

class ScoreBoard:
    def __init__(self,ai_game):
        self.ai_game=ai_game
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.settings=ai_game.settings
        self.stats=ai_game.stats
        self.text_color=(30,30,30)
        self.font=pygame.font.SysFont(None,48)
        self.prep_high_score()
        self.prep_score()
        self.prep_ships()
        self.prep_level()
        self.prep_shield()

    def prep_score(self):
        """更新得分到界面板上"""
        rounded_score=round(self.stats.score,-1)
        score_str=f"{rounded_score:,}"
        self.score_img=self.font.render(score_str,True,
                                        self.text_color,self.settings.bg_color)
        self.score_rect=self.score_img.get_rect()
        self.score_rect.right=self.screen_rect.right-20
        self.score_rect.top=20

    def show_score(self):
        """展示界面上所有信息"""
        self.screen.blit(self.score_img,self.score_rect)
        self.screen.blit(self.high_score_img,self.high_score_rect)
        self.screen.blit(self.level_img,self.level_rect)
        self.screen.blit(self.shield_img,self.shield_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """更新最高分数到界面板上"""
        high_score=round(self.stats.high_score,-1)
        high_score_str=f"{high_score:,}"
        self.high_score_img=self.font.render(high_score_str,True,
                                             self.text_color,self.settings.bg_color)
        self.high_score_rect=self.high_score_img.get_rect()
        self.high_score_rect.centerx=self.screen_rect.centerx
        self.high_score_rect.top=self.high_score_rect.top

    def check_high_score(self):
        """如果此时分数比最高分高 更新最高分数"""
        if self.stats.score>self.stats.high_score:
            self.stats.high_score=self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """更新目前的等级到界面板上去"""
        level_str=str(self.stats.level)
        self.level_img=self.font.render(level_str,True,
                                        self.text_color,self.settings.bg_color)
        self.level_rect=self.level_img.get_rect()
        self.level_rect.right=self.score_rect.right
        self.level_rect.top=self.score_rect.bottom+10

    def prep_ships(self):
        """更新船只到界面板上去"""
        self.ships=Group()
        for ship_num in range(self.stats.ships_left):
            ship=Ship(self.ai_game)
            ship.rect.x=10+ship_num*ship.rect.width
            ship.rect.y=10
            self.ships.add(ship)

    def prep_shield(self):
        """准备shield信息并更新到界面板上去"""
        txt="Shield: "
        if self.ai_game.ship.shield:
            txt+="Open"
        else:
            txt+="Close"
        self.shield_img=self.font.render(txt,True,self.text_color,self.settings.bg_color)
        self.shield_rect=self.shield_img.get_rect()
        self.shield_rect.y+=70
        self.shield_rect.x=0