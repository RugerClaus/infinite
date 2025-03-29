import pygame

class Button:
    def __init__(self, text, x, y, width, height, font, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.action = action  # Action to perform when clicked

        # Create surface for button and its text
        self.surface = pygame.Surface((self.width, self.height))
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))

    def draw(self, screen, mouse_pos):
        # Change color when mouse hovers over
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (0, 255, 0), self.rect)  # Hover color (green)
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)  # Normal color (red)

        # Draw the button text
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, mouse_pos, mouse_click):
        """Check if the button is clicked."""
        if self.rect.collidepoint(mouse_pos) and mouse_click:
            if self.action:
                self.action()

class Window:
    def __init__(self, width, height, title="Game"):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)  # Font for UI text

        # Initialize state
        self.game_active = False
        self.score = 0
        self.snail_rect = pygame.Rect(800, 300, 50, 50)
        self.player_rect = pygame.Rect(20, 300, 50, 50)

    def reset_game(self):
        """Reset the game variables."""
        self.score = 0
        self.snail_rect.x = 800
        self.player_rect.x = 20
        self.game_active = True

    def render_main_menu(self):
        """Render the main menu screen."""
        play_button = Button("Play", 350, 200, 100, 50, self.font, self.start_game)
        quit_button = Button("Quit", 350, 300, 100, 50, self.font, self.quit_game)

        self.screen.fill((255, 128, 0))  # Background color (orange)
        play_button.draw(self.screen, pygame.mouse.get_pos())
        quit_button.draw(self.screen, pygame.mouse.get_pos())

        pygame.display.flip()

        # Event loop for menu screen
        self.handle_ui_events([play_button, quit_button])

    def render_game_over(self):
        """Render the game over screen."""
        try_again_button = Button("Try Again", 350, 200, 200, 50, self.font, self.reset_game)
        quit_button = Button("Quit", 350, 300, 200, 50, self.font, self.quit_game)

        self.screen.fill((0, 0, 0))  # Background color (black)
        try_again_button.draw(self.screen, pygame.mouse.get_pos())
        quit_button.draw(self.screen, pygame.mouse.get_pos())

        # Game over text
        game_over_text = self.font.render("Game Over!", True, (255, 0, 0))
        self.screen.blit(game_over_text, (350, 100))

        pygame.display.flip()

        # Event loop for game over screen
        self.handle_ui_events([try_again_button, quit_button])

    def handle_ui_events(self, buttons):
        """Handle UI events (clicks)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any button is clicked
                for button in buttons:
                    button.is_clicked(pygame.mouse.get_pos(), event.button == 1)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()

    def start_game(self):
        """Start the game."""
        self.reset_game()
        while self.game_active:
            self.screen.fill((255, 255, 255))  # Background color (white)

            # Game logic and drawing
            self.score += 1
            score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
            self.screen.blit(score_text, (650, 5))

            # Simulating player movement and interactions (e.g., player rectangle)
            self.player_rect.x += 2
            self.snail_rect.x -= 3
            if self.snail_rect.right <= 0:
                self.snail_rect.left = 800

            # Render the player and snail (just rectangles for now)
            pygame.draw.rect(self.screen, (0, 0, 255), self.player_rect)
            pygame.draw.rect(self.screen, (255, 0, 0), self.snail_rect)

            pygame.display.flip()
            self.handle_ui_events([])  # No buttons during gameplay

            self.clock.tick(60)

    def quit_game(self):
        """Quit the game."""
        self.running = False
        pygame.quit()
        exit()

    def main_loop(self):
        """Main loop to handle UI states."""
        while self.running:
            if not self.game_active:
                self.render_main_menu()
            else:
                self.render_game_over()

            self.clock.tick(60)

# Main code
if __name__ == "__main__":
    window = Window(800, 600, "Game UI")
    window.main_loop()
s