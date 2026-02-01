import pygame
import logging
from core.paddle import Paddle
from core.ball import Ball
from core.level import Level
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
        self.default_ball_color = config.get('game', {}).get('default_ball_color',[255,0,0])

        self.brick_color = config.get('game', {}).get('brick_color',[100,100,100])
        self.bricks = self.load_level(1)

    def check_collision_side(self, ball, brick):
        dr = abs(ball.right - brick.left)
        dl = abs(ball.left - brick.right)
        db = abs(ball.bottom - brick.top)
        dt = abs(ball.top - brick.bottom)

        min_overlap = min(dr, dl, db, dt)

        if min_overlap == dr:
            return "right"
        if min_overlap == dl:
            return "left"
        if min_overlap == db:
            return "bottom"
        if min_overlap == dt:
            return "top"

    def load_level(self, lev):
        self.current_level = lev
        level = Level(lev,self.screen_width,self.screen_height)
        return level.load_level()

    def init_ball(self, p_height, ball_radius):
        ball_start = (self.screen_width // 2, self.screen_height - (5 * p_height))
        return Ball(ball_start,(self.screen_width,self.screen_height),ball_radius,(0,0))
    
    def start_play(self):
        self.logger.debug("Starting first ball on the game board now...")
        self.balls[0].start_ball()
    
    def calculate_bounce_angle(self, ball, paddle, speed, max_angle_deg=70.0):
        paddle_center = float(paddle.centerx)
        relative_hit = (float(ball.centerx) - paddle_center) / (float(paddle.width) / 2)

        relative_hit = max(-1, min(1, relative_hit))
        if abs(relative_hit) < 0.25:
            relative_hit = 0
        elif abs(relative_hit) < 0.5:
            relative_hit = random.uniform(0.01, 0.1)
        elif abs(relative_hit) < 0.75:
            relative_hit = random.uniform(0.1, 0.25)

        max_angle_rad = math.radians(max_angle_deg)
        bounce_angle = relative_hit * max_angle_rad

        new_vel_x = -speed * math.sin(bounce_angle)
        new_vel_y = -speed * math.cos(bounce_angle)

        return (new_vel_x, new_vel_y)

    def run(self):
        running = True
        pygame.mouse.set_visible(False)
        self.logger.debug("Started the GameWindow successfully")
        while running:
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
                pygame.draw.circle(self.screen,self.default_ball_color,ball.rect.center, ball.radius)

            if ball.rect.colliderect(self.paddle.rect):
                self.logger.debug(f"Paddle Hit: p{self.paddle.rect.centerx}, b{ball.rect.centerx}, s{ball.speed}")
                v_new = self.calculate_bounce_angle(self.paddle.rect, ball.rect, ball.speed)
                self.logger.debug(f"New Velocity: {v_new}")
                ball.vel_x = v_new[0]
                ball.vel_y = v_new[1]
                ball.rect.bottom = self.paddle.rect.top

            new_bricks = []
            for brick in self.bricks:
                if ball.rect.colliderect(brick):
                    cside = self.check_collision_side(ball.rect, brick)
                    self.logger.debug(f"Brick hit on {cside}!")
                    if cside in ['left', 'right']:
                        ball.vel_x *= -1
                    if cside in ['top', 'bottom']:
                        ball.vel_y *= -1
                else:
                    new_bricks.append(brick)
                pygame.draw.rect(self.screen, self.brick_color, brick)
            self.bricks = new_bricks

            pygame.display.flip()

            self.balls = [b for b in self.balls if not b.handle_wall_collisions()]
            if not self.balls:
                running = False
            if not self.bricks:
                self.logger.info(f'Completed level {self.current_level}')
                self.current_level += 1
                self.logger.info(f"Loading level {self.current_level}")
                self.bricks = self.load_level(self.current_level)
                self.balls = [self.init_ball(self.p_height, self.ball_radius)]
        
        pygame.mouse.set_visible(True)
        return "menu"