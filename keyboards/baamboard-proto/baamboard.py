from baam.keyboard.constants import KC
from baam.hid import HID
from typing import Dict, List, Tuple, Optional
from baam.keyboard.keyboard import Keyboard
from .hw import KeyMatrix


class BaamBoard(Keyboard):
    def __init__(
        self,
        matrix: KeyMatrix,
        layers: Dict[str, Tuple[Tuple[KC]]] = {},
        ble: Optional[HID] = None,
        usb: Optional[HID] = None,
    ) -> None:
        super().__init__(matrix, layers, ble, usb)
        self.active_hid = usb

    def switch_hid(
        self,
    ):
        self.active_hid = self.ble
