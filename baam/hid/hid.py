from abc import ABC, abstractmethod
from enum import Enum
from micropython import const


class DeviceState(Enum):
    BOOT = const(0)
    DISCONNECTED = const(1)
    CONNECTING = const(2)
    IDLE = const(3)
    TERMINATED = const(4)


class HID(ABC):
    def __init__(self, device_name: str = "") -> None:
        self.device_name = device_name
        self.state = DeviceState.BOOT

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass
