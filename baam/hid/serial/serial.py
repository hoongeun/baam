from baam.hid import HID
from baam.keyboard.constants import KC


class Serial(HID):
    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def press(self, *keys: KC):
        pass

    async def release(self, *key: KC):
        pass
