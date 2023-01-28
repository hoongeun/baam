import bluetooth
import struct
from micropython import UUID, const

class Advertiser:
    def __init__(self, ble: bluetooth.BLE, device_name="Generic HID Device", services=[UUID(0x1812)], appearance=const(960), ):
        self._ble = ble

    # Start advertising at 100000 interval
    def start(self):
        if not self.advertising:
            self._ble.gap_advertise(100000, adv_data=self._payload)

    