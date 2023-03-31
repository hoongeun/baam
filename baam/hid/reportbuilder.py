from abc import ABC, abstractmethod
from typing import Set, TypeVar, Generic

from baam.keyboard.constants import KC


TReportBuilder = TypeVar("TReportBuilder", bound="ReportBuilder")


class ReportBuilder(ABC, Generic[TReportBuilder]):

    @abstractmethod
    def set_modifiers(self, modifiers: Set[KC]) -> TReportBuilder:
        pass

    @abstractmethod
    def set_normals(self, normal: Set[KC]) -> TReportBuilder:
        pass

    @abstractmethod
    def build(self) -> bytearray:
        pass
