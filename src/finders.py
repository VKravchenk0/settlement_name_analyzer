from src.models import UaLocationsSettlement
from sqlalchemy import and_, or_


def find_settlements_by_regex(name_regex):
    print("searching by regex " + name_regex)

    settlements = UaLocationsSettlement.query \
        .filter(
        and_(
            UaLocationsSettlement.name_lower.op("~")(name_regex.lower())),
        UaLocationsSettlement.lat.isnot(None)) \
        .order_by(UaLocationsSettlement.name_lower) \
        .all()

    print("result found: " + str(settlements))
    if not settlements:
        print(f"No results found by regex {name_regex}")

    return settlements


def find_settlements_without_coordinates():
    print("searching settlements without coordinates")

    settlements = UaLocationsSettlement.query \
        .filter(
        and_(
            UaLocationsSettlement.type.not_in(['COUNTRY', 'CAPITAL_CITY', 'STATE', 'DISTRICT', 'COMMUNITY']),
            or_(
                UaLocationsSettlement.lat.is_(None),
                UaLocationsSettlement.lng.is_(None)
            ))) \
        .order_by(UaLocationsSettlement.name_lower) \
        .all()

    return settlements
