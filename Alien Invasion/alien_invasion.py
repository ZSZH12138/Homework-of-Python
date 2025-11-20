import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_state import GameState
from time import sleep
from button import Button
from scoreboard import ScoreBoard
import pickle
import os

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.game_active=False
        self.clock=pygame.time.Clock()
        self.settings=Settings()
        self.screen=pygame.display.set_mode(
            (0,0),
            pygame.FULLSCREEN
        )
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height
        pygame.display.set_caption("Alian Invasion")
        self.play_button=Button(self,"Play")
        if os.path.exists(r".\high_score.txt"):
            with open(".\high_score.txt","rb") as f:
                high_score=pickle.load(f)
        else:
            high_score=0
        self.ship=Ship(self)
        self.stats=GameState(self,high_score)
        self.sb=ScoreBoard(self)
        # 相当于创建了一个子弹的空数组
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                

    def _check_keydown_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        # 注意在使用键盘按键时要使用英文的输入法
        # 特别是在变成全屏的时候很有可能自动切换为中文输入法
        elif event.key==pygame.K_q:
            self.store_high_score()
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()
        elif (event.key==pygame.K_LSHIFT or event.key==pygame.K_RSHIFT) and self.game_active:
            self.ship.shield=True
            self.sb.prep_shield()

    def _check_keyup_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for alien in self.aliens.sprites():
            for bullet in alien.bullets.sprites():
                bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _fire_bullet(self):
        if len(self.bullets)<self.settings.bullet_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for alien in self.aliens.sprites():
            alien.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        for alien in self.aliens.sprites():
            for bullet in alien.bullets.sprites():
                if bullet.rect.top>=self.ship.rect.bottom:
                    alien.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        self._check_bullet_ship_collisions()

    def _create_fleet(self):
        alien=Alien(self)
        alien_width,alien_height=alien.rect.width,alien.rect.height
        current_x,current_y=alien_width,alien_height
        while current_y<(self.settings.screen_height-3*alien_height):
            while current_x<(self.settings.screen_width-2*alien_width):
                self._create_alien(current_x,current_y)
                current_x+=2*alien_width
            current_x=alien_width
            current_y+=2*alien_height
    
    def _create_alien(self,x_pos,y_pos):
        alien=Alien(self)
        alien.x=x_pos
        alien.rect.x=x_pos
        alien.y=y_pos
        alien.rect.y=y_pos
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction(alien)
    
    def _change_fleet_direction(self,alien):
        alien.rect.y+=self.settings.fleet_drop_speed
        alien.direction*=-1

    def _check_bullet_alien_collisions(self):
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score+=self.settings.alien_points*len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level+=1
            self.sb.prep_level()

    def _check_bullet_ship_collisions(self):
        for alien in self.aliens:
            collisions=pygame.sprite.spritecollide(self.ship,alien.bullets,True)
            if collisions:
                break
        if collisions and not self.ship.shield:
            self._ship_hit()
        elif collisions:
            self.ship.shield=False
            self.sb.prep_shield()
    
    def _ship_hit(self):
        if self.stats.ships_left>0:
            self.stats.ships_left-=1
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active=False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=self.settings.screen_height:
                self._ship_hit()
                break   
    
    def _check_play_button(self,mouse_pos):
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active=True
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def store_high_score(self):
        with open(r".\high_score.txt","wb") as f:
            pickle.dump(self.stats.high_score,f)

if __name__=="__main__":
    ai=AlienInvasion()
    ai.run_game()