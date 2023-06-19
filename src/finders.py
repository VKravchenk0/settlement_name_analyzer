# from sqlalchemy.sql.operators import collate
from sqlalchemy import collate

from src.models import UaLocationsSettlement
from sqlalchemy import and_, or_


def find_settlements_by_regex(name_regex, language='uk'):
    print("Searching by regex " + name_regex)

    search_field = UaLocationsSettlement.name_lower
    if language == 'en':
        search_field = UaLocationsSettlement.name_en_lower

    settlements = UaLocationsSettlement.query \
        .filter(
        and_(
            # search_field.op("~")(name_regex.lower())), for postgres
            search_field.op("regexp")(name_regex.lower())),
        UaLocationsSettlement.lat.isnot(None)) \
        .order_by(collate(search_field, 'tr_TR')) \
        .all()
    # тут не працює

    print("Results found: " + str(len(settlements)))
    if not settlements:
        print(f"No results found by regex {name_regex}")

    return settlements


def find_settlements_without_coordinates():
    print("Searching settlements without coordinates")

    settlements = UaLocationsSettlement.query \
        .filter(
        and_(
            UaLocationsSettlement.type.not_in(['COUNTRY', 'STATE', 'DISTRICT', 'COMMUNITY']),
            or_(
                UaLocationsSettlement.lat.is_(None),
                UaLocationsSettlement.lng.is_(None)
            ))) \
        .order_by(UaLocationsSettlement.name_lower) \
        .all()

    return settlements
