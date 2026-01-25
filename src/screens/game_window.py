import pygame
import logging
import math
import random

class GameWindow:
    def __init__(self, screen, config):
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self):
        running = True

        while running:
            self.logger.debug("Started the GameWindow successfully")
            running = False
    
        return "menu"