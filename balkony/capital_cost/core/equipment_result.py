from dataclasses import dataclass

@dataclass(frozen=True)
class EquipmentCostResult:
    range_status: str
    value: float
    CEPCI: float