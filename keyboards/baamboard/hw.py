from typing import List, Optional
import keypad
import microcontroller


class KeyMatrix:
    def __init__(
        self, rows_pin: List[microcontroller.Pin], cols_pin: List[microcontroller.Pin]
    ):
        self._matrix = keypad.KeyMatrix(rows_pin, cols_pin)

    async def pop(self) -> Optional[keypad.Event]:
        return self._matrix.events.get()
