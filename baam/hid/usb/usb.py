from enum import Enum
from baam.hid import HID
import usb_hid


# REPORT_ID = 0x4
# REPORT_BYTES = 16
# keyboard_descriptor = bytes(
#     (
#         0x05,
#         0x01,  # Usage Page (Generic Desktop),
#         0x09,
#         0x06,  # Usage (Keyboard),
#         0xA1,
#         0x01,  # Collection (Application),
#         0x85,
#         REPORT_ID,  #   Report ID
#         # bitmap of modifiers
#         0x75,
#         0x01,  #   Report Size (1),
#         0x95,
#         0x08,  #   Report Count (8),
#         0x05,
#         0x07,  #   Usage Page (Key Codes),
#         0x19,
#         0xE0,  #   Usage Minimum (224),
#         0x29,
#         0xE7,  #   Usage Maximum (231),
#         0x15,
#         0x00,  #   Logical Minimum (0),
#         0x25,
#         0x01,  #   Logical Maximum (1),
#         0x81,
#         0x02,  #   Input (Data, Variable, Absolute), ;Modifier byte
#         # LED output report
#         0x95,
#         0x05,  #   Report Count (5),
#         0x75,
#         0x01,  #   Report Size (1),
#         0x05,
#         0x08,  #   Usage Page (LEDs),
#         0x19,
#         0x01,  #   Usage Minimum (1),
#         0x29,
#         0x05,  #   Usage Maximum (5),
#         0x91,
#         0x02,  #   Output (Data, Variable, Absolute),
#         0x95,
#         0x01,  #   Report Count (1),
#         0x75,
#         0x03,  #   Report Size (3),
#         0x91,
#         0x03,  #   Output (Constant),
#         # bitmap of keys
#         0x95,
#         (REPORT_BYTES - 1) * 8,  #   Report Count (),
#         0x75,
#         0x01,  #   Report Size (1),
#         0x15,
#         0x00,  #   Logical Minimum (0),
#         0x25,
#         0x01,  #   Logical Maximum(1),
#         0x05,
#         0x07,  #   Usage Page (Key Codes),
#         0x19,
#         0x00,  #   Usage Minimum (0),
#         0x29,
#         (REPORT_BYTES - 1) * 8 - 1,  #   Usage Maximum (),
#         0x81,
#         0x02,  #   Input (Data, Variable, Absolute),
#         0xC0,  # End Collection
#     )
# )

def lookup_device() -> usb_hid.Device:
    usage_page = 0x1
    usage = 0x06
    for device in usb_hid.devices:
        if (
            device.usage_page == usage_page
            and device.usage == usage
            and hasattr(device, "send_report")
        ):
            return device
    raise ValueError("Could not find matching HID device.")


class USBHIDMode(Enum):
    AUTO = 0
    NORMAL = 1
    NKRO = 2


class USB(HID):
    def __init__(self, device: usb_hid.Device):
        self.nkroable = False
        self.mode = USBHIDMode.NORMAL
        self.device = device


    async def connect(self):
        usb_hid.enable(
            (
                self.device,
                usb_hid.Device.MOUSE,
                usb_hid.Device.CONSUMER_CONTROL,
            )
        )

    def disconnect(self):
        usb_hid.disable()

    def try_nkro(self):
        try:
            report = bytearray(16)
            await self.send_report(report)
            self.mode = USBHIDMode.NKRO
            return True
        except ValueError:
            return False

    async def send_report(self, report: bytearray):
        await self.device.send_report(report)
