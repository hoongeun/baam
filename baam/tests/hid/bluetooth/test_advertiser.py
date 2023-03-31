from bluetooth import UUID
from baam.hid.bluetooth.advertiser import AdPayloadFactory
from baam.hid.bluetooth.constants import BLEAppearance

def test_make_payload():
    factory = AdPayloadFactory("dummy")
    assert "asdf" == factory._make_appearance_payload(BLEAppearance.HID_KEYBOARD)
    assert "" == factory._make_name_payload("some_name")
    assert "" == factory._make_service_uuid_payload([UUID(0x2908)])
