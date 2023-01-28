from core.hid import HID
import usb_hid

class USB(HID):
    def __init__(self, device: usb_hid.Device):
        self.device = device

    async def check_device(self):
        self.device.send_report([b'\0'] * 16)

    async def connect(self):
        pass

    async def disconnect(self):
        pass