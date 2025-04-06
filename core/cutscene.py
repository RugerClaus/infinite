import pygame

class Cutscene:
    def __init__(self, game):
        self.game = game
        self.cutscene_images = [pygame.image.load('graphics/start_of_game.png'),
                                pygame.image.load('graphics/title_card_1.png'),
                                pygame.image.load('graphics/title_card_2.jpg')]  # List of images for the crash scene
        self.fade_duration = 2  # Seconds to fade in/out
    def fade_to_black(self):
        fade_surface = pygame.Surface(self.game.screen.get_size())
        fade_surface.fill((0, 0, 0))
        clock = pygame.time.Clock()
        
        for alpha in range(0, 255, 5):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            fade_surface.set_alpha(alpha)
            self.game.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            clock.tick(60)  # 60 FPS

    def fade_in(self):
        fade_surface = pygame.Surface(self.game.screen.get_size())
        fade_surface.fill((0, 0, 0))
        clock = pygame.time.Clock()

        for alpha in range(255, 0, -5):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            fade_surface.set_alpha(alpha)
            self.game.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            clock.tick(60)


    def play_cutscene(self):
        self.fade_to_black()

        for image in self.cutscene_images:
            start_time = pygame.time.get_ticks()
            duration = 5000  # 3 seconds

            while pygame.time.get_ticks() - start_time < duration:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                self.game.screen.blit(image, (0, 0))
                pygame.display.update()
                self.game.clock.tick(60)

            self.fade_to_black()
            self.fade_in()

        self.game.cutscene_played = True
