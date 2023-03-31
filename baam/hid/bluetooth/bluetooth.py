from enum import Enum
import bluetooth
from bluetooth import UUID
from micropython import const
from baam.hid import HID
from .advertiser import Advertiser
from .constants import IRQ
from .passkey import PassKeyActor
from .secret import Secret


class BluetoothState(Enum):
    BLE_UNKNOWN = -1
    BLE_DISCONNECTED = 0
    BLE_ADVERTISING = 1
    BLE_CONNECTING = 2
    BLE_CONNECTED = 3


class Bluetooth(HID):
    def __init__(self) -> None:
        super().__init__()
        self._ble = bluetooth.BLE()
        self.advertiser = Advertiser(self._ble)
        self.state: BluetoothState = BluetoothState.BLE_DISCONNECTED
        self.secret = Secret()
        self.bond = False
        self.enable_secure_pairing = False

        self.device_information_service = (  # Device Information Service description
            UUID(0x180A),  # Device Information
            (
                (UUID(0x2A24), bluetooth.FLAG_READ),  # Model number string
                (UUID(0x2A25), bluetooth.FLAG_READ),  # Serial number string
                (UUID(0x2A26), bluetooth.FLAG_READ),  # Firmware revision string
                (UUID(0x2A27), bluetooth.FLAG_READ),  # Hardware revision string
                (UUID(0x2A28), bluetooth.FLAG_READ),  # Software revision string
                (UUID(0x2A29), bluetooth.FLAG_READ),  # Manufacturer name string
                (UUID(0x2A50), bluetooth.FLAG_READ),  # PnP ID
            ),
        )

        self.human_interface_device_service = (
            UUID(0x1812),  # Human Interface Device
            (
                (UUID(0x2A4A), bluetooth.FLAG_READ),  # HID information
                (UUID(0x2A4B), bluetooth.FLAG_READ),  # HID report map
                (UUID(0x2A4C), bluetooth.FLAG_WRITE),  # HID control point
                (UUID(0x2A4D), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY, ((UUID(0x2908), 0x01),)),  # HID report / reference
                (UUID(0x2A4D), bluetooth.FLAG_WRITE, ((UUID(0x2908), 0x01),)),  # HID report / reference
                (UUID(0x2A4E), bluetooth.FLAG_WRITE),  # HID protocol mode
            ),
        )

        self.battery_service = (
            UUID(0x180F),  # Device Information
            (
                (UUID(0x2A19), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY),  # Battery level
            ),
        )

        # fmt: off
        self.HID_INPUT_REPORT = bytes([    # Report Description: describes what we communicate
            0x05, 0x01,                    # USAGE_PAGE (Generic Desktop)
            0x09, 0x06,                    # USAGE (Keyboard)
            0xa1, 0x01,                    # COLLECTION (Application)
            0x85, 0x01,                    #     REPORT_ID (1)
            0x75, 0x01,                    #     Report Size (1)
            0x95, 0x08,                    #     Report Count (8)
            0x05, 0x07,                    #     Usage Page (Key Codes)
            0x19, 0xE0,                    #     Usage Minimum (224)
            0x29, 0xE7,                    #     Usage Maximum (231)
            0x15, 0x00,                    #     Logical Minimum (0)
            0x25, 0x01,                    #     Logical Maximum (1)
            0x81, 0x02,                    #     Input (Data, Variable, Absolute); Modifier byte
            0x95, 0x01,                    #     Report Count (1)
            0x75, 0x08,                    #     Report Size (8)
            0x81, 0x01,                    #     Input (Constant); Reserved byte
            0x95, 0x05,                    #     Report Count (5)
            0x75, 0x01,                    #     Report Size (1)
            0x05, 0x08,                    #     Usage Page (LEDs)
            0x19, 0x01,                    #     Usage Minimum (1)
            0x29, 0x05,                    #     Usage Maximum (5)
            0x91, 0x02,                    #     Output (Data, Variable, Absolute); LED report
            0x95, 0x01,                    #     Report Count (1)
            0x75, 0x03,                    #     Report Size (3)
            0x91, 0x01,                    #     Output (Constant); LED report padding
            0x95, 0x06,                    #     Report Count (6)
            0x75, 0x08,                    #     Report Size (8)
            0x15, 0x00,                    #     Logical Minimum (0)
            0x25, 0x65,                    #     Logical Maximum (101)
            0x05, 0x07,                    #     Usage Page (Key Codes)
            0x19, 0x00,                    #     Usage Minimum (0)
            0x29, 0x65,                    #     Usage Maximum (101)
            0x81, 0x00,                    #     Input (Data, Array); Key array (6 bytes)
            0xc0                           # END_COLLECTION
        ])
        # fmt: on

        self.services = [self.device_information_service, self.battery_service, self.human_interface_device_service]
        self.passKeyActor = PassKeyActor()

    def connect(self):
        if self.state is BluetoothState.BLE_DISCONNECTED:
            self.state = BluetoothState.BLE_CONNECTING
            self._ble.irq(self.handle_irq)
            self._ble.active(1)
            self._ble.config(gap_name=self.device_name, mtu=23, bond=self.bond)

            if self.enable_secure_pairing:
                self._ble.config(le_secure=True, mitm=True, io=self.io_capability)

    def disconnect(self):
        pass

    def pair(self):
        pass

    def handle_irq(self, event: IRQ, data):
        if event == IRQ.CENTRAL_CONNECT.value():  # Central connected
            self.conn_handle, _, _ = data  # Save the handle
            print("Central connected: ", self.conn_handle)
            self.state = BluetoothState.BLE_CONNECTED
        elif event == IRQ.CENTRAL_DISCONNECT.value():  # Central disconnected
            self.conn_handle = None  # Discard old handle
            conn_handle, addr_type, addr = data
            print("Central disconnected: ", conn_handle)
            self.state = BluetoothState.BLE_DISCONNECTED
        elif event == IRQ.MTU_EXCHANGED.value():  # MTU was set
            conn_handle, mtu = data
            print("MTU exchanged: ", mtu)
        elif event == IRQ.CONNECTION_UPDATE.value():  # Connection parameters were updated
            self.conn_handle, _, _, _, _ = data  # The new parameters
            print("Connection update")
        elif event == IRQ.ENCRYPTION_UPDATE:  # Encryption updated
            conn_handle, encrypted, authenticated, bonded, key_size = data
            print("encryption update", conn_handle, encrypted, authenticated, bonded, key_size)
        elif event == IRQ.PASSKEY_ACTION:  # Passkey actions: accept connection or show/enter passkey
            self.passKeyActor.handle_action(self._ble, data)
        elif event == IRQ.GATTS_INDICATE_DONE.value():
            conn_handle, value_handle, status = data
            print("gatts done: ", conn_handle)
        elif event == IRQ.SET_SECRET.value():  # Set secret for bonding
            sec_type, key, value = data
            sec_key = sec_type, bytes(key)
            value = bytes(value) if value else None
            print("set secret: ", sec_key, value)
            secure_data = self.secret.load()
            if value is None:  # If value is empty, and
                if key in secure_data:  # If key is known then
                    del secure_data[sec_key]  # Forget key
                    self.secret.save(secure_data)  # Save bonding information
                    return True
                else:
                    return False
            else:
                secure_data[key] = value  # Remember key/value
                self.secret.save(secure_data)  # Save bonding information
            return True
        elif event == IRQ.GET_SECRET.value():  # Get secret for bonding
            sec_type, index, key = data
            secure_data = self.secret.load()
            if key is None:
                for (old_sec_t, old_key), value in secure_data.items():
                    if old_sec_t == sec_type && i == index:
                        return value

                return None
            else:
                key = sec_type, bytes(key)
                return secure_data.get(key, None)
        else:
            print("Unhandled IRQ event: ", event)
