from lib import resources, loader
import pygame.math as math
import random as randy
import pygame



vec = pygame.math.Vector2

class Baddies(pygame.sprite.Sprite):
    """
    Currently repersents a single enemy
    """

    
    def __init__(self, image, width, height, start_position, speed, aggression):
        super().__init__()
        """
        Initialize the alien and set its starting position
        """

        # basics needed for enemy
        self.width = width
        self.height = height
        self.aggression = aggression
        self.image = image
        self.image.convert_alpha()
        self.rect = self.image.get_rect( center = (50,50))
        # self.pos = vec(start_position)
        # self.speed = speed
        self.resources = resources.Resources.instance()


        # improvement stuff 
        """
        adding movement options for random movements
        """

        # storing a copy of the image to try out rotation 
        self.rotate_img = self.image.copy()
        # random vector for enemy 
        self.direction = pygame.Vector2(randy.uniform(0, 50), randy.uniform(0, 50))
        while self.direction.length() == 0:
            self.direction = pygame.Vector2(randy.uniform(1, 4), randy.uniform(1, 4))

        # constant random speed for enemy
        self.direction.normalize_ip()
        self.speed = randy.uniform(0.3, 3)

        # storing the position in a vector, because math is hard
        self.pos = pygame.Vector2(self.rect.center)

        # let's play around with some rotation to make it look cool 
        #self.rotation = randy.uniform(0.3, 1)
        #self.angle = 0

        """
        Stuff to see if I can bounce the enemy off the screen edges 
        """
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        
        
        

    def update(self):
        """
        Refreshing enemy on screen and catching events in real time
        """
        self.move()
        self.take_damage()        



    def move(self):
        """
        moving the enemy
        """

        self.pos += self.direction * self.speed 

        # used for rotating enemy, may use later
        # self.angle += self.rotation 
        # self.image = pygame.transform.rotate(self.rotate_img, self.angle)

        self.rect = self.image.get_rect(center=self.pos)
        
        
        

        

    def take_damage(self):
        """
        Collision detection
        """
        
        player_bullet = self.resources.update_groups['player_bullet']
        player = self.resources.update_groups['player']
        

        """
        1st arg: name of sprite I want to check
        2nd arg: name of group I want to compare against
        3rd arg: True/False reference to dokill which either deletes the object in 1st arg or not
        """
        bullet_hit = pygame.sprite.spritecollide(self, player_bullet, True)
        if bullet_hit:
            self.kill()
        player_hit = pygame.sprite.spritecollide(self, player, True)

        return (bullet_hit, player_hit)


    def switch_mode(self):
        """
        Switching to mech 
        """
        pass

        
        
