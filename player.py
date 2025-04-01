import pygame
from animate import Animation
from entity import Entity
from player_utilities.inventory import Inventory

class Player(Entity):
    def __init__(self, x, y, screen, game,music_manager):
        super().__init__(x,y,64,84,screen)
        self.music_manager = music_manager
        self.speed = 0
        self.gravity = 0
        self.walking = False
        self.jumping = False
        self.on_ground = True
        self.was_walking = self.walking
        self.health = 10
        self.game = game
        self.inventory = Inventory()
        
        #going right
        self.walking_frames = [
            pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha(),
            pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        ]
        self.walking_animation = Animation(self.walking_frames,10)
        self.jumping_frame = [pygame.image.load("graphics/Player/jump.png").convert_alpha()]
        self.jumping_animation = Animation(self.jumping_frame,10)

        #going left
        self.walking_backward_frames = [
            pygame.image.load("graphics/Player/player_walk_back_1.png").convert_alpha(),
            pygame.image.load("graphics/Player/player_walk_back_2.png").convert_alpha()
        ]
        self.walking_backward_animation = Animation(self.walking_backward_frames,10)
        self.jumping_back_frame = [pygame.image.load("graphics/Player/jump_back.png").convert_alpha()]
        self.jumping_backward_animation = Animation(self.jumping_back_frame,10)

        #facing forward
        self.holding_still_frame = [pygame.image.load("graphics/Player/player_stand.png").convert_alpha()]
        self.holding_still_animation = Animation(self.holding_still_frame,10)
        
    def update(self,items_group):
        
        super().update()
        item_touched = pygame.sprite.spritecollideany(self,items_group)
        if item_touched:
            self.inventory.add_item(item_touched)
            items_group.remove(item_touched)

        if not self.on_ground:
            self.gravity += 0.5  
            self.jumping_animation.update()

        if self.on_ground and not self.walking:
            self.holding_still_animation.update()

        if self.rect.bottom >= 701:
            self.rect.bottom = 700
            self.gravity = 0
            self.on_ground = True 

            if self.was_walking and self.speed != 0:
                self.walking = True

        if self.walking and self.on_ground:
            if self.speed > 0: #right
                self.walking_animation.update()
            elif self.speed < 0: #left
                self.walking_backward_animation.update()

        if self.rect.left < self.screen.get_width() // 2:
            
            self.rect.x += self.speed
        elif self.rect.left >= self.screen.get_width() // 2:
            
            if self.game.background_x == 0:
                
                self.rect.x += self.speed
            elif self.game.background_x == -2900:
                
                self.rect.x += self.speed
            else:
                self.rect.x = self.screen.get_width() // 2
        if self.rect.x <= 0 or self.rect.x >= 1000 and self.game.background_x <= -3100:
            self.speed = 0

        
        self.rect.y += self.gravity
        

    def jump(self):
        if self.on_ground:
            self.gravity = -15
            self.on_ground = False
            self.was_walking = self.walking
            self.walking = False
            self.music_manager.play_sfx('jump')
            print("Jumping!")

    def draw(self):
        if not self.on_ground:
            self.walking = False
            if self.speed > 0: #right
                self.image = self.jumping_animation.get_current_frame()
            elif self.speed < 0: #left
                self.image = self.jumping_backward_animation.get_current_frame()
        elif self.walking:
            if self.speed > 0: #right
                self.image = self.walking_animation.get_current_frame()
            elif self.speed < 0: #left
                self.image = self.walking_backward_animation.get_current_frame()
        else:
            self.image = self.holding_still_frame[0]
        super().draw()