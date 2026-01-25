import logging
import json
import pygame
import sys

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

def main():
    game_playing = True

    config = load_app_config(CONFIG_FILE_PATH)
    configure_logging(config.get("logging"))

    logger = logging.getLogger("main")
    logger.info("Config loaded and logging initialized.")
    logger.debug(config.get("logging"))

    pygame.init()

    while game_playing:
        logger.debug("Game loop started.")
        game_playing = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()