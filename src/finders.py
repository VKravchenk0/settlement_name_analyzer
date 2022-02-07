from src.models import UaLocationsSettlement
from sqlalchemy import and_


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
