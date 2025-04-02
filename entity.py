import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self,screen, has_gravity=False, health=0):
        super().__init__()
        self.screen = screen

        # Physics
        self.has_gravity = has_gravity
        self.gravity = 0
        self.on_ground = False

        # Health
        self.max_health = health
        self.health = health if health > 0 else None  # Only entities that need health will use this.

        # Animation
        self.animations = {}
        self.current_animation = None

    def set_animation(self, state, animation):
        self.animations[state] = animation

    def play_animation(self, state):
        """Plays the assigned animation state."""
        if state in self.animations:
            self.current_animation = self.animations[state]
            self.current_animation.update()
            self.image = self.current_animation.get_current_frame()

    def apply_gravity(self):
        """Handles gravity effects if applicable."""
        if self.has_gravity:
            self.rect.y += self.gravity
            self.gravity += 0.5  # Simulating downward pull

            # Ground collision check
            if self.rect.bottom >= 700:  
                self.rect.bottom = 700
                self.gravity = 0
                self.on_ground = True
            else:
                self.on_ground = False

    def take_damage(self, amount):
        """Reduces health, removes entity if health reaches zero."""
        if self.health is not None:
            self.health -= amount
            if self.health <= 0:
                self.kill()  # Removes the entity from the game.

    def update(self):
        """Updates entity behavior."""
        self.apply_gravity()

    def draw(self):
        """Draws the entity on the screen."""
        self.screen.blit(self.image, self.rect)
