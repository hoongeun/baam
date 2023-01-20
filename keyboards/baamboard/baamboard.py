from core.keyboard.keyboard import Keyboard

class BaamBoard(Keyboard):
    def __init__(self, matrix: KeyMatrix, layers: Dict[str, List[List[ctypes.c_ubyte]]] = {}, ble: Optional[HID]=None, usb: Optional[HID]=None) -> None:
        super().__init__(matrix, layers, ble, usb)
        self.active_hid = usb

    def switch_hid(self, ):
        self.active_hid = self.ble