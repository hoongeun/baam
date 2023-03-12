from typing import Dict, Tuple
from baam.keyboard.constants import KC

class KeyLayer:
    def __init__(self, layer: Dict[Tuple[int, int], KC]):
        self.layer = layer
        self.rows = max(map(lambda x: x[0], self.layer.keys())) + 1
        self.cols = max(map(lambda x: x[1], self.layer.keys())) + 1

    def get_keycode(self, coord: Tuple[int, int]) -> KC:
        return self.layer[coord]


