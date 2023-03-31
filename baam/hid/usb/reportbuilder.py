from typing import Set, Self

from baam.hid.hid import ReportBuilder
from baam.keyboard.constants import KC, modifier_bit


class USBReportBuilder(ReportBuilder):
    def __init__(self, nkro: bool=False):
        self.nkro = nkro
        if self.nkro:
            self.report = bytearray(16)
            # self.reserved = memoryview(self.report)[1:2] # reserved
            self.bitmap = memoryview(self.report)[2:]
        else:
            self.report = bytearray(8)
            # self.reserved = memoryview(self.report)[1:2] # reserved
            self.bitmap = memoryview(self.report)[2:]

        self.modifier = memoryview(self.report)[0:1]

    def set_modifiers(self, modifiers: Set[KC]) -> Self:
        self.modifier[0] = 0x00
        for mod in modifiers:
            self.modifier = self.modifier | modifier_bit(mod)
        return self

    def set_normals(self, normals: Set[KC]) -> Self:
        if self.nkro:
            for i in range(2, 16):
                self.bitmap[i-2] = 0x00
            for n in normals:
                self.bitmap[int(n.value()) >> 3] |= 1 << (int(n.value()) & 0x7)
        else:
            for i, n in enumerate(normals):
                self.bitmap[i] = 0xFF & n.value()
            for i in range(len(normals), min(6, len(normals))):
                self.bitmap[i] = 0x00
        return self

    def build(self) -> bytearray:
        return self.report
