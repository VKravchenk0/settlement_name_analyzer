from typing import List

from src.models import UaLocationsSettlement
from src.responses import SettlementDTO


def convert_settlements(settlements: List[UaLocationsSettlement]) -> List[SettlementDTO]:
    result = []
    for s in settlements:
        result.append(SettlementDTO(s.id, s.public_name['uk'], s.lat, s.lng))
    return result
