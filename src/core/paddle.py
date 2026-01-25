import pygame

class Paddle:
    def __init__(self, y, x, width, height):
        self.rect = pygame.Rect(x,y,width,height)
    
    def update_position(self, mouse_x, screen_width):
        new_x = mouse_x - (self.rect.width // 2)
        if new_x < 0:
            new_x = 0
        elif new_x > screen_width - self.rect.width:
            new_x = screen_width - self.rect.width
        self.rect.x = new_x