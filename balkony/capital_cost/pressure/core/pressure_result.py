from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class PressureResult:
    status: Tuple[str, bool]
    value: float