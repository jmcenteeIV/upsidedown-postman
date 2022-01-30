import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_DOWN, K_UP, K_SPACE

from lib import resources, bullet, uitext

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):

    def __init__(self, image, height, width, acceleration, friction):
        super().__init__()
        self.friction = friction
        self.acceleration = acceleration
        self.width = width
        self.height = height
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.image = image
        self.rect = self.image.get_rect( center = (100, 420))

        self.pos = vec((width/2, height))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.read_to_fire = True
        self.num_shots = 0
        self.kills = 0

        self.ui_text = uitext.UIText()
        self.ui_text.get_data_callback = self.get_num_shots

    def update(self):
        self.move()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            if self.ready_to_fire:
                self.ready_to_fire = False
                self.player_fire()

        if not pressed_keys[K_SPACE]:
            self.ready_to_fire = True
    
    def move(self):
        self.acc = vec(0,0)

        pressed_keys = pygame.key.get_pressed()
        #  Horizontal movement        
        if pressed_keys[K_LEFT]:
            self.acc.x = -self.acceleration
        if pressed_keys[K_RIGHT]:
            self.acc.x = self.acceleration

        self.acc.x += self.vel.x * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > (self.width - (self.rect.width/2)):
            self.pos.x, self.acc.x = (self.width - (self.rect.width/2)), 0
        if self.pos.x < (self.rect.width/2):
            self.pos.x, self.acc.x = (self.rect.width/2) , 0

        #  Vertical movement
        if pressed_keys[K_DOWN]:
            self.acc.y = self.acceleration
        if pressed_keys[K_UP]:
            self.acc.y = -self.acceleration

        self.acc.y += self.vel.y * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.y > self.height:
            self.pos.y, self.acc.y = self.height, 0
        if self.pos.y < self.rect.height:
            self.pos.y, self.acc.y = (0 + self.rect.height), 0

        self.rect.midbottom = self.pos

    def player_fire(self):
        new_bullet = bullet.Bullet(self.height, 6, resources.Resources.instance().player.rect.midtop)
        new_bullet.parent = self
        resources.Resources.instance().update_groups["player_bullet"].add(new_bullet)
        resources.Resources.instance().draw_groups["render"].add(new_bullet)
        resources.Resources.instance().assets['sounds']['laser1'].play()
        self.num_shots = self.num_shots + 1
    
    def increment_kills(self):
        self.kills = self.kills + 1

    def get_num_shots(self):
        return self.num_shots