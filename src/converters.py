from typing import List

from src.models import UaLocationsSettlement
from src.responses import SettlementDTO


def convert_settlements(settlements: List[UaLocationsSettlement]) -> List[SettlementDTO]:
    result = []
    for s in settlements:
        result.append(SettlementDTO(s.id, s.public_name['uk'], round(s.lat, 3), round(s.lng, 3)))
    return result
