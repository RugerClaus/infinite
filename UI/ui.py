class UI:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.font = self.game.window.button_font
        self.prompt_surface = None

    def show_prompt(self, text,item_image,is_swapping):
        # Create surface for the prompt
        self.prompt_surface = self.font.render(text, True, (255, 255, 255))
        self.prompt_rect = self.prompt_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(self.prompt_surface, self.prompt_rect)
        if not is_swapping:
            self.screen.blit(item_image,(700,375))
        else:
            self.screen.blit(item_image,(750,375))

    def hide_prompt(self):
        # Hide the prompt
        self.prompt_surface = None
