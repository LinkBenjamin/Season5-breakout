import pygame

class Ball:
    def __init__(self, location, boundaries, radius, velocities):
        self.radius = radius
        self.x = float(location[0])
        self.y = float(location[1])
        self.rect = pygame.Rect(location[0] - radius, location[1]-radius, radius * 2, radius * 2)
        self.speed = 10

        self.vel_x = float(velocities[0])
        self.vel_y = float(velocities[1])

        self.screen_width = boundaries[0]
        self.screen_height = boundaries[1]
    
    def start_ball(self):
        self.vel_y = self.speed

    def update_position(self):
        self.x += self.vel_x
        self.y += self.vel_y

        self.rect.x = self.x
        self.rect.y = self.y

    def bounce_x(self):
        self.vel_x = -self.vel_x

    def bounce_y(self):
        self.vel_y = -self.vel_y

    def handle_wall_collisions(self):
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.bounce_x()
        
        if self.rect.top <= 0:
            self.bounce_y()
    
        if self.rect.bottom >= self.screen_height:
            return True
        
        return False