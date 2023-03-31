from typing import Set

from baam.hid.hid import ReportBuilder
from baam.keyboard.constants import modifier_bit, KC


class BLEReportBuilder(ReportBuilder):
    def __init__(self):
        self.report = bytearray(8)
        # self.reserved = memoryview(self.report)[1:2] # reserved
        self.bitmap = memoryview(self.report)[2:]
        self.modifier = memoryview(self.report)[0:1]

    def set_modifiers(self, modifiers: Set[KC]):
        self.modifier[0] = 0x00
        for mod in modifiers:
            self.modifier = self.modifier | modifier_bit(mod)
        return self

    def set_normals(self, normals: Set[KC]):
        for i, n in enumerate(normals):
            self.bitmap[i] = 0xFF & n.value()
        for i in range(len(normals), min(6, len(normals))):
            self.bitmap[i] = 0x00
        return self

    def build(self) -> bytearray:
        return self.report
