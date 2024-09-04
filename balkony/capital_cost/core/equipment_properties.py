from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class EquipmentProperties:
    data: Tuple[float, float, float]
    unit: str
    min_size: float
    max_size: float