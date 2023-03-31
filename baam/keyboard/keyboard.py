import asyncio
from typing import List, Tuple, Dict, Optional, Callable, Set
from dataclasses import dataclass, field
from baam.hid.hid import HID
from baam.hid.bluetooth import Bluetooth, BLEReportBuilder
from baam.hid.usb import USB, USBReportBuilder
from baam.keyboard.constants import KC, _______, is_modifier
from baam.keyboard.matrix import KeyMatrix
from baam.keyboard.layer import KeyLayer


KeyEvent = Tuple[KC, Set[KC]]
KeyEventHandler = Callable[[KeyEvent], None]


def is_valid_matrix(layer: KeyLayer, key_matrix: KeyMatrix) -> bool:
    return key_matrix.shape() == (layer.rows, layer.cols)


async def get_keycode(layer: KeyLayer, matrix: KeyMatrix) -> Tuple[Set[KC], Set[KC], Set[KC]]:
    hardware: Set[KC] = set()  # reserved keycodes like firmware upgrade, restart
    normals: Set[KC] = set()
    modifiers: Set[KC] = set()
    coords = matrix.scan()
    for kc in map(lambda coord: layer.get_keycode(coord), coords):
        modifiers.add(kc) if is_modifier(kc.value()) else normals.add(kc)
    return normals, modifiers, hardware


@dataclass
class KeyState:
    norm: Set[KC] = field(default_factory=set)
    mod: Set[KC] = field(default_factory=set)
    hw: Set[KC] = field(default_factory=set)


class Keyboard:
    def __init__(self, matrix: KeyMatrix, layers: Optional[Dict[str, KeyLayer]]=None, ble: Optional[HID]=None, usb: Optional[HID]=None) -> None:
        self.matrix: KeyMatrix = matrix
        self.ble: Optional[HID] = ble
        self.usb: Optional[HID] = usb
        self.key_down_handlers: List[KeyEventHandler] = []
        self.key_up_handlers: List[KeyEventHandler] = []
        self.layers: Dict[str, KeyLayer] = {} if layers is None else layers
        self.current_layer = self.layers.get("default")
        self.active_hid: Optional[HID] = None
        self.key_state = KeyState()
        self.is_running = False

    def start(self):
        self.is_running = True
        while self.is_running:
            norm_kc, mod_kc, hw_kc = await get_keycode(self.current_layer, self.matrix)
            await asyncio.gather([self.send_keys(norm_kc, mod_kc), self.handle_events(norm_kc, mod_kc, hw_kc)])
            self.key_state = KeyState(norm_kc, mod_kc, hw_kc)

    def stop(self):
        self.is_running = False

    async def send_keys(self, norm_keys: Set[KC], mod_keys: Set[KC]):
        if isinstance(self.active_hid, USB):
            report = USBReportBuilder().set_normals(norm_keys).set_modifier(mod_keys).build()
            await self.active_hid.send_report(report)
        elif isinstance(self.active_hid, Bluetooth):
            report = BLEReportBuilder().set_normals(norm_keys).set_modifier(mod_keys).build()
            await self.active_hid.send_report(report)
        else:
            ValueError(f"failed to send keys, {self.active_hid}, {norm_keys}")

    async def handle_events(self, norm_kc: Set[KC], mod_kc: Set[KC], hw_kc: Set[KC]):
        key_down, pressing, key_up = self.diff_state(KeyState(norm_kc, mod_kc, hw_kc))
        for key in key_down[0].union(pressing[0]):
            for handler in self.key_down_handlers:
                handler((key, mod_kc))
        for key in key_up[0]:
            for handler in self.key_up_handlers:
                handler((key, mod_kc))

    def diff_state(self, new_state: KeyState) -> Tuple[Tuple[Set[KC], Set[KC], Set[KC]], Tuple[Set[KC], Set[KC], Set[KC]], Tuple[Set[KC], Set[KC], Set[KC]]]:
        norm_key_up = self.key_state.norm.difference(new_state.norm)
        norm_key_down = new_state.norm.difference(self.key_state.norm)
        norm_pressing = new_state.norm.intersection(self.key_state.norm)
        mod_key_up = self.key_state.mod.difference(new_state.mod)
        mod_key_down = new_state.mod.difference(self.key_state.mod)
        mod_pressing = new_state.norm.intersection(self.key_state.mod)
        hw_key_up = self.key_state.norm.difference(new_state.hw)
        hw_key_down = new_state.hw.difference(self.key_state.hw)
        hw_pressing = new_state.hw.intersection(self.key_state.hw)
        return (norm_key_down, mod_key_down, hw_key_down), (norm_pressing, mod_pressing, hw_pressing), (norm_key_up, mod_key_up, hw_key_up)
