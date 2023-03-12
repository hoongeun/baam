import bluetooth
import struct
from micropython import UUID, const
from typing import List, Union
from .constants import AdDataType, BLEAppearance, GAPAdType


class Advertiser:
    def __init__(
        self,
        ble: bluetooth.BLE,
        device_name="Generic HID Device",
        services=[UUID(0x1812)],
        appearance=BLEAppearance.HID_KEYBOARD,
    ):
        self._ble = ble
        self.device_name = device_name
        self.services = services
        self.appearance = appearance
        self.advertising = False

    def start(self):
        if not self.advertising:
            self.advertising = True
            payload = AdPayloadFactory.build(self.services, self.services, self.appearance)
            self._ble.gap_advertise(100000, adv_data=payload)

    def stop(self):
        if self.advertising:
            self.advertising = False

class AdPayloadFactory:
    @staticmethod
    def build(name: str, services: List[UUID], appearance: BLEAppearance, general_discoverable_mode: bool = True, br_edr: bool = False) -> bytes
        flag_payload = AdPayloadFactory.make_flag_payload(general_discoverable_mode, br_edr)
        name_payload = AdPayloadFactory.make_name_payload(name)
        services_payload = AdPayloadFactory.make_services_payload(services)
        appearance_payload = AdPayloadFactory.make_appearance_payload(appearance)
        return struct.pack("B"*(len(flag_payload)+len(name_payload)+len(services_payload)+len(appearance_payload)), flag_payload, name_payload, services_payload, appearance_payload)

    @staticmethod
    def make_appearance_payload(appearance: BLEAppearance) -> bytes:
        return struct.pack("B", appearance.value())

    @staticmethod
    def make_services_payload(services: List[UUID]) -> bytes:
        payloads =list(map(lambda x: AdPayloadFactory.make_service_uuid_payload(bytes(x)), services))
        return struct.pack("B"*len(payloads), *payloads)

    @staticmethod
    def make_service_uuid_payload(uuid: bytes) -> bytes:
        if len(uuid) == 2:
            return AdPayloadFactory.encode_advertisement(GAPAdType.SERVICE_UUID_16BIT_COMPLETE, uuid)
        elif len(uuid) == 4:
            return AdPayloadFactory.encode_advertisement(GAPAdType.SERVICE_UUID_32BIT_COMPLETE, uuid)
        elif len(uuid) == 16:
            return AdPayloadFactory.encode_advertisement(GAPAdType.SERVICE_UUID_128BIT_COMPLETE, uuid)
        else:
            raise ValueError(f"invalid uuid {uuid}")

    @staticmethod
    def make_flag_payload(general_discoverable_mode: bool, br_edr: bool):
        discoverable_mode = AdDataType.LE_GENERAL_DISC_MODE.value() if general_discoverable_mode else AdDataType.LE_LIMITED_DISC_MODE.value()
        data_rate = AdDataType.LE_BR_EDR_CONTROLLER.value() | AdDataType.LE_BR_EDR_HOST.value() if br_edr else AdDataType.BR_EDR_NOT_SUPPORTED.value()
        return AdPayloadFactory.encode_advertisement(GAPAdType.FLAGS, struct.pack("B", discoverable_mode | data_rate))

    @staticmethod
    def make_name_payload(name: str):
        name_bytes = bytearray()
        name_bytes.extend(map(ord, name))
        return AdPayloadFactory.encode_advertisement(GAPAdType.COMPLETE_LOCAL_NAME, name_bytes)

    @staticmethod
    def encode_advertisement(adv_type: GAPAdType, value: Union[bytearray, bytes])
        return struct.pack("BB", len(value) + 1, adv_type.value()) + value

