import pygame

class WinScreen:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config

        self.bg_color = config.get('menu', {}).get('bg_color',[0,0,0])
        self.text_color = config.get('menu', {}).get('text_color',[0,0,0])
        raw_font_size = config.get('menu', {}).get('font_size',60)
        self.font_size = raw_font_size if isinstance(raw_font_size, int) else 60
        self.font = pygame.font.Font(config.get('menu', {}).get('font','assets/fonts/Blox2.ttf'), self.font_size)

        self.screen_width = config.get('app', {}).get('screen_width',800)
        self.screen_height = config.get('app', {}).get('screen_height',800)
        
        self.menu_items = [
            {"label": "Click to continue", "action":"menu"}
        ]

        self.buttons = []
        self._setup_buttons()

    def _setup_buttons(self):
        start_y = 200
        padding = 75
    
        for i, item in enumerate(self.menu_items):
            text_surf = self.font.render(item['label'],True,self.text_color)
            rect = text_surf.get_rect(center=(self.screen_width // 2, start_y + (i * padding)))

            self.buttons.append({'rect': rect, 'action': item['action'], 'label': item['label']})

    def _draw(self):
        self.screen.fill(self.bg_color)

        title_font = pygame.font.Font(self.config.get('menu',{}).get('font','assets/fonts/Blox2.ttf'), self.font_size + 20)
        title_surf = title_font.render("Congratulations You Win", True, self.text_color)
        title_rect = title_surf.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title_surf,title_rect)

        for btn in self.buttons:
            text_surf = self.font.render(btn['label'], True, self.text_color)
            self.screen.blit(text_surf, btn['rect'])

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        return 'menu'
            
            self._draw()