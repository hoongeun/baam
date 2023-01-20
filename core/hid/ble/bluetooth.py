from enum import Enum
from micropython import const
import bluetooth
from hid.ble import Advertiser
from hid import HIDWriter

class BluetoothState(Enum):
    BLE_DISCONNECTED = const(0)
    BLE_ADVERTISING = const(1)
    BLE_CONNECTING = const(2)
    BLE_CONNECTED = const(3)

class Bluetooth(HIDWriter):
    def __init__(self) -> None:
        super().__init__()
        self._ble = bluetooth.BLE()
        self.advertiser = Advertiser(self._ble)
