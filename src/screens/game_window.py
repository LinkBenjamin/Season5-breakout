import pygame
import logging
from core.paddle import Paddle
from core.ball import Ball
import math
import random

class GameWindow:
    def __init__(self, screen, config):
        self.screen = screen
        self.logger = logging.getLogger(self.__class__.__name__)
        self.background_color = config.get('game',{}).get('background_color',[0,0,0])
        self.screen_width = config.get('app',{}).get('screen_width',100)
        self.screen_height = config.get('app',{}).get('screen_height',100)
        self.paddle_color = config.get('app',{}).get('paddle_color',[255,255,255])

        self.p_height = self.screen_height // 20
        p_width = self.screen_width // 6

        p_y = self.screen_height - (2 * self.p_height)
        
        self.paddle = Paddle(p_y, self.screen_width // 2, p_width, self.p_height)
        self.balls = []
        self.ball_radius = config.get('game',{}).get('default_ball_radius',10)
        self.balls.append(self.init_ball(self.p_height,self.ball_radius))

    def init_ball(self, p_height, ball_radius):
        ball_start = (self.screen_width // 2, self.screen_height - (5 * p_height))
        return Ball(ball_start,(self.screen_width,self.screen_height),ball_radius,(0,0))
    
    def start_play(self):
        self.logger.debug("Starting first ball on the game board now...")
        self.balls[0].start_ball()
    
    def run(self):
        running = True
        pygame.mouse.set_visible(False)
            
        while running:
            self.logger.debug("Started the GameWindow successfully")
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.logger.debug(f"Detected Mouse UP: len(self.balls)={len(self.balls)}, vel_x={self.balls[0].vel_x}, vel_y={self.balls[0].vel_y}")
                    if len(self.balls) == 1 and self.balls[0].vel_x == 0 and self.balls[0].vel_y == 0:
                        self.start_play()
                if event.type == pygame.QUIT:
                    running = False

            # Paddle update
            mouse_x, _ = pygame.mouse.get_pos()
            self.screen.fill(self.background_color)
            self.paddle.update_position(mouse_x, self.screen_width)
            pygame.draw.rect(self.screen, self.paddle_color, self.paddle.rect)

            # Ball update
            for ball in self.balls:
                ball.update_position()
                pygame.draw.circle(self.screen,[255,0,0],ball.rect.center, ball.radius)

            pygame.display.flip()

            self.balls = [b for b in self.balls if not b.handle_wall_collisions()]
            if not self.balls:
                running = False
        
        pygame.mouse.set_visible(True)
        return "menu"