import pygame

class Brick:
    def __init__(self, brick_type, config):
        match brick_type:
            case "2": #Ball splitter
                self.brick_type = "splitter"
                self.brick_color = config.get('game', {}).get('split_color', [180,0,180])
            case _:
                self.brick_type = "regular"
                self.brick_color = config.get('game', {}).get('brick_color', [180,0,180])
        self.rect = None
    
    def place_brick(self, rect):
        self.rect = rect