import ctypes
from typing import List, Tuple, Callable, Dict, Optional
from core.hid.hid import HID
from core.keyboard.constants import KC, ______
from core.keyboard.hw import KeyMatrix


class Keyboard:
    def __init__(self, matrix: KeyMatrix, layers: Dict[str, List[List[ctypes.c_ubyte]]] = {}, ble: Optional[HID]=None, usb: Optional[HID]=None) -> None:
        self.matrix: KeyMatrix = matrix
        self.ble: Optional[HID] = ble
        self.usb: Optional[HID] = usb
        self.key_down_listeners: List[Callable[[ctypes.c_ubyte, bool, bool, bool, bool]], None] = []
        self.key_up_listeners: List[Callable[[ctypes.c_ubyte, bool, bool, bool, bool]], None] = []
        self.key_up_listeners: List[Callable[[ctypes.c_ubyte, bool, bool, bool, bool]], None] = []
        self.layers = layers
        self.active_hid: Optional[HID] = None

    async def on_key_event_raw(self, keycodes: List[ctypes.c_ubyte]):
        self.on_key_event_raw(keycodes)


    def on_key_down(self, keycode: ctypes.c_ubyte, primary: bool=False, shift: bool=False, alt: bool=False, meta: bool=False):

    def on_key_down_raw(self, keycodes: List[ctypes.c_ubyte]):
        return self.on_key_down()

    def on_key_press(self, keycode: ctypes.c_ubyte, primary: bool=False, shift: bool=False, alt: bool=False, meta: bool=False):

    def on_key_press_raw(self, keycodes: List[ctypes.c_ubyte]):

    def on_key_up(self, keycode: ctypes.c_ubyte, primary: bool=False, shift: bool=False, alt: bool=False, meta: bool=False):

    def on_key_up_raw(self, keycode: List[ctypes.c_ubyte]):

    def send_string(self, string: str):

    def add_event_listener(self, event_listener):

    async def start(self):
        while True:
            ev = await self.matrix.pop()
            if ev is not None:
                key = matrix[ev.key_number]
                if ev.pressed:
                    kbd.press(key)
                else:
                    kbd.release(key)
            else
            key = (kc, mods[KC.LCtrl] or mods[KC.RCtrl], mods[KC.LShift] or mods[KC.RShift], mods[KC.LAlt] or mods[KC.RAlt], mods[KC.LGui] or mods[KC.RGui]) # KC, Ctrl, Shift, Alt, Meta
            self.on_key_even

    def scan_matrix(self) -> Tuple[KC, Dict[KC, bool]]:
        kc = KC.No
        modifiers = {
            KC.LAlt: False,
            KC.RAlt: False,
            KC.LShift: False,
            KC.RShift: False,
            KC.LCtrl: False,
            KC.RCtrl: False,
            KC.LGui: False,
            KC.RGui: False,
        }
        for row in self.layout:
            for cell in row:
                if kc == KC.No:
                    kc = cell
                elif cell in [KC.LAlt, KC.RAlt, KC.LShift, KC.RShift, KC.LCtrl, KC.RCtrl, KC.LGui, KC.RGui]:
                    modifiers[cell]
        return modifiers