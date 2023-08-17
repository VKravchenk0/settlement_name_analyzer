from typing import List

from app.service.dtos import MissingCoordinatesSettlementDTO, SettlementDTO
from app.db.models import UaLocationsSettlement


def convert_settlements(settlements: List[UaLocationsSettlement]) -> List[SettlementDTO]:
    result = []
    for s in settlements:
        result.append(SettlementDTO(s.id, s.public_name['uk'], s.state, s.district, s.community, round(s.lat, 3), round(s.lng, 3)))
    return result


def convert_missing_coordinates_settlements(settlements: List[UaLocationsSettlement]) -> List[
    MissingCoordinatesSettlementDTO]:
    result = []
    for s in settlements:
        print(f"----------------{s.id}")
        names = get_parent_hierarchy_names(s)
        result.append(MissingCoordinatesSettlementDTO(s.id, names))
    return result


def get_parent_hierarchy_names(settlement):
    """Recursively builds the name of the whole settlement hierarchy
    e.g. "с. Антонівці, Шумська громада, Кременецький р-н, Тернопільська обл."
    """
    result_naming = settlement.public_name['uk']

    if settlement.parent_id is not None and settlement.parent_id != 1:
        parent = UaLocationsSettlement.query.get(settlement.parent_id)
        parent_names = get_parent_hierarchy_names(parent)
        result_naming = result_naming + ', ' + parent_names

    return result_naming
