from enum import Enum
from micropython import const
from typing import List, Tuple, Dict, Optional, Callable, Set
from dataclasses import dataclass
from baam.hid.hid import HID
from baam.keyboard.constants import KC, _______
from baam.keyboard.matrix import KeyMatrix, is_modifier
from baam.keyboard.layer import KeyLayer


class KeyEventType(Enum):
    Unknown = const(0)
    Press = const(1)
    Release = const(2)


KeyEvent = Tuple[KC, bool, bool, bool, bool, bool, bool, bool]
KeyEventHandler = Callable[KeyEvent, None]


def is_valid_matrix(layer: KeyLayer, key_matrix: KeyMatrix) -> bool:
    return key_matrix.shape() == (layer.rows, layer.cols)


async def get_keycode(layer: KeyLayer, matrix: KeyMatrix) -> Tuple[Set[KC], Set[KC], Set[KC]]:
    hardware: Set[KC] = set()  # reserved keycodes like firmware upgrade, restart
    normals: Set[KC] = set()
    modifiers: Set[KC] = set()
    coords = await matrix.scan()
    for kc in map(lambda coord: layer.get_keycode(coord), coords):
        modifiers.add(kc) if is_modifier(kc.value()) else normals.add(kc)
    return normals, modifiers, hardware


@dataclass
class KeyState:
    norm: Set[KC] = set()
    mod: Set[KC] = set()
    hw: Set[KC] = set()


class Keyboard:
    def __init__(self, matrix: KeyMatrix, layers: Dict[str, KeyLayer] = {}, ble: Optional[HID]=None, usb: Optional[HID]=None) -> None:
        self.matrix: KeyMatrix = matrix
        self.ble: Optional[HID] = ble
        self.usb: Optional[HID] = usb
        self.key_press_handlers: List[KeyEventHandler] = []
        self.key_release_handlers: List[KeyEventHandler] = []
        self.layers: Dict[str, KeyLayer] = layers
        self.current_layer = layers["default"]
        self.active_hid: Optional[HID] = None
        self.key_state = KeyState()

    def on_key_press(self, event: KeyEvent):
        for handler in self.key_press_handlers:
            handler(*event)

    def on_key_release(self, event: KeyEvent):
        for handler in self.key_release_handlers:
            handler(*event)

    def send_string(self, string_to_send: str):
        pass

    async def start(self):
        while True:
            norm_kc, mod_kc, hw_kc = await get_keycode(self.current_layer, self.matrix)
            if len(hw_kc) > 0:
                raise NotImplementedError("hardware keycode isn't implemented")
            key_down, pressing, key_up = self.change_state(KeyState(norm_kc, mod_kc, hw_kc))

            if ev is not None:
                if ev.pressed:
                    kbd.press(key)
                else:
                    kbd.release(key)
            else

            self.on_key_event

    def change_state(self, new_state: KeyState) -> Tuple[Tuple[Set[KC], Set[KC], Set[KC]], Tuple[Set[KC], Set[KC], Set[KC]], Tuple[Set[KC], Set[KC], Set[KC]]]:
        norm_key_up = self.key_state.norm.difference(new_state.norm)
        norm_key_down = new_state.norm.difference(self.key_state.norm)
        norm_pressing = new_state.norm.intersection(self.key_state.norm)
        mod_key_up = self.key_state.mod.difference(new_state.mod)
        mod_key_down = new_state.mod.difference(self.key_state.mod)
        mod_pressing = new_state.norm.intersection(self.key_state.mod)
        hw_key_up = self.key_state.norm.difference(new_state.hw)
        hw_key_down = new_state.hw.difference(self.key_state.hw)
        hw_pressing = new_state.hw.intersection(self.key_state.hw)
        self.key_state = new_state
        return (norm_key_down, mod_key_down, hw_key_down), (norm_pressing, mod_pressing, hw_pressing), (norm_key_up, mod_key_up, hw_key_up)


