from typing_extensions import TypeVar
import bluetooth
import struct
from micropython import UUID
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
            payload = (AdPayloadFactory(self.device_name)
                .set_services(self.services)
                .set_appearance(self.appearance)
                .build())
            self._ble.gap_advertise(100000, adv_data=payload)

    def stop(self):
        if self.advertising:
            self.advertising = False

class AdPayloadFactory:
    def __init__(self, name: str) -> None:
        self.name = name
        self.services: List[UUID] = []
        self.appearance: BLEAppearance = BLEAppearance.HID_KEYBOARD
        self.discoverable_mode: int = AdDataType.LE_GENERAL_DISC_MODE.value()
        self.data_rate: int = AdDataType.LE_BR_EDR_CONTROLLER.value() | AdDataType.LE_BR_EDR_HOST.value()

    def build(self) -> bytes:
        flag_payload = self._make_flag_payload(self.discoverable_mode, self.data_rate)
        name_payload = self._make_name_payload(self.name)
        services_payload = self._make_services_payload(self.services)
        appearance_payload = self._make_appearance_payload(self.appearance)
        return struct.pack("B"*(len(flag_payload)+len(name_payload)+len(services_payload)+len(appearance_payload)), flag_payload, name_payload, services_payload, appearance_payload)

    def set_services(self, services: List[UUID]):
        self.services = services
        return self

    def set_appearance(self, appearance: BLEAppearance):
        self.appearance = appearance
        return self

    def set_discoverable_mode(self, discoverable_mode: AdDataType):
        self.discoverable_mode = discoverable_mode.value()
        return self

    def set_br_edr(self, data_rate: AdDataType):
        self.data_rate = data_rate.value()
        return self

    def _make_appearance_payload(self, appearance: BLEAppearance) -> bytes:
        return struct.pack("B", appearance.value())

    def _make_services_payload(self, services: List[UUID]) -> bytes:
        payloads =list(map(lambda uuid: self._make_service_uuid_payload(uuid), services))
        return struct.pack("B"*len(payloads), *payloads)

    def _make_service_uuid_payload(self, uuid: UUID) -> bytes:
        b_uuid = bytes(uuid)
        if len(b_uuid) == 2:
            return self._encode_advertisement(GAPAdType.SERVICE_UUID_16BIT_COMPLETE, b_uuid)
        elif len(b_uuid) == 4:
            return self._encode_advertisement(GAPAdType.SERVICE_UUID_32BIT_COMPLETE, b_uuid)
        elif len(b_uuid) == 16:
            return self._encode_advertisement(GAPAdType.SERVICE_UUID_128BIT_COMPLETE, b_uuid)
        else:
            raise ValueError(f"invalid uuid {b_uuid}")

    def _make_flag_payload(self, discoverable_mode: int, data_rate: int):
        # discoverable_mode = AdDataType.LE_GENERAL_DISC_MODE.value() if general_discoverable_mode else AdDataType.LE_LIMITED_DISC_MODE.value()
        # data_rate = AdDataType.LE_BR_EDR_CONTROLLER.value() | AdDataType.LE_BR_EDR_HOST.value() if br_edr else AdDataType.BR_EDR_NOT_SUPPORTED.value()
        return self._encode_advertisement(GAPAdType.FLAGS, struct.pack("B", discoverable_mode | data_rate))

    def _make_name_payload(self, name: str):
        name_bytes = bytearray()
        name_bytes.extend(map(ord, name))
        return self._encode_advertisement(GAPAdType.COMPLETE_LOCAL_NAME, name_bytes)

    def _encode_advertisement(self, adv_type: GAPAdType, value: Union[bytearray, bytes])
        return struct.pack("BB", len(value) + 1, adv_type.value()) + value
