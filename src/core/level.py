import logging
from pathlib import Path
from pygame import Rect

class Level:
    def __init__(self, level, screen_width, screen_height):
        self.logger = logging.getLogger(__class__.__name__)
        current_file = Path(__file__).resolve()
        self.project_root = current_file.parents[2]
        self.levels_dir = self.project_root / "assets" / "levels"
        self.level_file = self.levels_dir / f"level-{level}.txt"
        self.width = screen_width
        self.height = screen_height
    
    def load_level(self):
        rects = []
        data = []
        with open(self.level_file, 'r', encoding='utf-8') as f:
            for line in f:
                row = line.strip().split(',')
                data.append(row)
        self.logger.debug(f"Loaded {data}")

        brick_width = self.width // len(data[0])
        brick_height = (self.height // 2) // len(data)

        for i,row in enumerate(data):
            for j,col in enumerate(row):
                if col == '1':
                    new_rect = Rect(j * brick_width, i * brick_height, brick_width - 2, brick_height - 2)
                    rects.append(new_rect)
        return rects