import logging
import json
import pygame
import sys

from screens.menu import MainMenu
from screens.game_window import GameWindow
from screens.win_screen import WinScreen

CONFIG_FILE_PATH = "app_config.json"
logger = None

def configure_logging(config):
    l = logging.getLevelName(logging._nameToLevel.get(config.get("level","DEBUG").upper(), logging.DEBUG))

    file = config.get("file",None)

    handlerz = [logging.StreamHandler(sys.stdout)]

    if file:
        handlerz.append(logging.FileHandler(file, mode='a'))

    logging.basicConfig(
        level=l,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlerz
    )

def load_app_config(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def main_menu_screen(screen, config):
    """
    Creates the Menu instance and waits for a choice.
    """
    menu = MainMenu(screen, config)
    response = menu.run() # This blocks until a choice is made
    return response

def play_game_screen(screen, config):
    """
    Creates the game play screen and allows the player to play.
    """
    game = GameWindow(screen, config)
    response = game.run() # This blocks until the game ends, either via save or game-over
    return response

def show_win_screen(screen, config):
    win = WinScreen(screen, config)
    response = win.run()
    return response

def main():
    game_playing = True

    config = load_app_config(CONFIG_FILE_PATH)
    configure_logging(config.get("logging"))

    logger = logging.getLogger("main")
    logger.info("Config loaded and logging initialized.")
    logger.debug(config.get("logging"))

    pygame.init()
    swidth = config.get('app',{}).get('screen_width',400)
    sheight = config.get('app',{}).get('screen_height',400)
    screen = pygame.display.set_mode((swidth, sheight))
    pygame.display.set_caption(config.get('app',{}).get('name'))
    while game_playing:
        logger.debug("Game loop started.")
        menu_selection = main_menu_screen(screen, config)
        logger.debug(f"Menu Selection: {menu_selection}")

        match menu_selection:
            case 'new':
                logger.debug("Matched 'new'")
                response = play_game_screen(screen, config)
                if 'WIN' in response:
                    show_win_screen(screen, config)
            case 'quit':
                logger.debug("Matched 'quit'")
                game_playing = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()