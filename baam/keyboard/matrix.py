from typing import List, Set, Tuple
import microcontroller


class KeyMatrix:
    def __init__(
        self, row_pins: List[microcontroller.Pin], col_pins: List[microcontroller.Pin]
    ):
        self.row_pins = row_pins
        self.col_pins = col_pins

    def shape(self) -> Tuple[int, int]:
        return len(self.row_pins), len(self.col_pins)

    def scan(self) -> Set[Tuple[int, int]]:
        result = set()
        for i, rp in enumerate(self.row_pins):
            if rp.enabled:
                for j, cp in enumerate(self.col_pins):
                    if cp.enabled:
                        result.add((i, j))
        return result



