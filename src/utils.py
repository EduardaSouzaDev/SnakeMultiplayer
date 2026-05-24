import random
from config import GRID_WIDTH, GRID_HEIGHT

def random_position():
    return (
        random.randint(0, GRID_WIDTH - 1),
        random.randint(0, GRID_HEIGHT - 1)
    )