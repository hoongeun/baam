from enum import Enum
from micropython import const


class BLEAppearance(Enum):
    GENERIC_HID = const(960)
    HID_KEYBOARD = const(961)
    HID_MOUSE = const(962)
    HID_JOYSTICK = const(963)
    HID_GAMEPAD = const(964)
    HID_DIGITIZERSUBTYPE = const(965)
    HID_CARD_READER = const(966)
    HID_DIGITAL_PEN = const(967)
    HID_BARCODE = const(968)


class GAPAdType(Enum):
    FLAGS = const(0x01)  # Flags for discoverability.
    SERVICE_UUID_16BIT_MORE_AVAILABLE = const(
        0x02
    )  # Partial list of 16 bit service UUIDs.
    SERVICE_UUID_16BIT_COMPLETE = const(0x03)  # Complete list of 16 bit service UUIDs.
    SERVICE_UUID_32BIT_MORE_AVAILABLE = const(
        0x04
    )  # Partial list of 32 bit service UUIDs.
    SERVICE_UUID_32BIT_COMPLETE = const(0x05)  # Complete list of 32 bit service UUIDs.
    SERVICE_UUID_128BIT_MORE_AVAILABLE = const(
        0x06
    )  # Partial list of 128 bit service UUIDs.
    SERVICE_UUID_128BIT_COMPLETE = const(
        0x07
    )  # Complete list of 128 bit service UUIDs.
    SHORT_LOCAL_NAME = const(0x08)  # Short local device name.
    COMPLETE_LOCAL_NAME = const(0x09)  # Complete local device name.
    TX_POWER_LEVEL = const(0x0A)  # Transmit power level.
    CLASS_OF_DEVICE = const(0x0D)  # Class of device.
    SIMPLE_PAIRING_HASH_C = const(0x0E)  # Simple Pairing Hash C.
    SIMPLE_PAIRING_RANDOMIZER_R = const(0x0F)  # Simple Pairing Randomizer R.
    SECURITY_MANAGER_TK_VALUE = const(0x10)  # Security Manager TK Value.
    SECURITY_MANAGER_OOB_FLAGS = const(0x11)  # Security Manager Out Of Band Flags.
    SLAVE_CONNECTION_INTERVAL_RANGE = const(0x12)  # Slave Connection Interval Range.
    SOLICITED_SERVICE_UUIDS_16BIT = const(
        0x14
    )  # List of 16-bit Service Solicitation UUIDs.
    SOLICITED_SERVICE_UUIDS_128BIT = const(
        0x15
    )  # List of 128-bit Service Solicitation UUIDs.
    SERVICE_DATA = const(0x16)  # Service Data - 16-bit UUID.
    PUBLIC_TARGET_ADDRESS = const(0x17)  # Public Target Address.
    RANDOM_TARGET_ADDRESS = const(0x18)  # Random Target Address.
    APPEARANCE = const(0x19)  # Appearance.
    ADVERTISING_INTERVAL = const(0x1A)  # Advertising Interval.
    LE_BLUETOOTH_DEVICE_ADDRESS = const(0x1B)  # LE Bluetooth Device Address.
    LE_ROLE = const(0x1C)  # LE Role.
    SIMPLE_PAIRING_HASH_C256 = const(0x1D)  # Simple Pairing Hash C-256.
    SIMPLE_PAIRING_RANDOMIZER_R256 = const(0x1E)  # Simple Pairing Randomizer R-256.
    SERVICE_DATA_32BIT_UUID = const(0x20)  # Service Data - 32-bit UUID.
    SERVICE_DATA_128BIT_UUID = const(0x21)  # Service Data - 128-bit UUID.
    URI = const(0x24)  # URI
    THREE_DEMENTION_INFORMATION_DATA = const(0x3D)  # 3D Information Data.
    MANUFACTURER_SPECIFIC_DATA = const(0xFF)  # Manufacturer Specific Data.


class AdDataType(Enum):
    LE_LIMITED_DISC_MODE = const(0x01)
    LE_GENERAL_DISC_MODE = const(0x02)
    BR_EDR_NOT_SUPPORTED = const(0x04)
    LE_BR_EDR_CONTROLLER = const(0x08)
    LE_BR_EDR_HOST = const(0x10)
    LE_ONLY_LIMITED_DISC_MODE = const(0x05)
    FLAGS_LE_ONLY_GENERAL_DISC_MODE = const(0x06)


class IRQ(Enum):
    # IRQ peripheral role event codes
    CENTRAL_CONNECT = const(1)
    CENTRAL_DISCONNECT = const(2)
    GATTS_WRITE = const(3)
    GATTS_READ_REQUEST = const(4)
    SCAN_RESULT = const(5)
    SCAN_DONE = const(6)
    PERIPHERAL_CONNECT = const(7)
    PERIPHERAL_DISCONNECT = const(8)
    GATTC_SERVICE_RESULT = const(9)
    GATTC_SERVICE_DONE = const(10)
    GATTC_CHARACTERISTIC_RESULT = const(11)
    GATTC_CHARACTERISTIC_DONE = const(12)
    GATTC_DESCRIPTOR_RESULT = const(13)
    GATTC_DESCRIPTOR_DONE = const(14)
    GATTC_READ_RESULT = const(15)
    GATTC_READ_DONE = const(16)
    GATTC_WRITE_DONE = const(17)
    GATTC_NOTIFY = const(18)
    GATTC_INDICATE = const(19)
    GATTS_INDICATE_DONE = const(20)
    MTU_EXCHANGED = const(21)
    L2CAP_ACCEPT = const(22)
    L2CAP_CONNECT = const(23)
    L2CAP_DISCONNECT = const(24)
    L2CAP_RECV = const(25)
    L2CAP_SEND_READY = const(26)
    CONNECTION_UPDATE = const(27)
    ENCRYPTION_UPDATE = const(28)
    GET_SECRET = const(29)
    SET_SECRET = const(30)
    PASSKEY_ACTION = const(31)
