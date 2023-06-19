import time
from src.constants import *

from pyuca import Collator

from src.models import UaLocationsSettlement
from sqlalchemy import and_, or_

collator = Collator()


def find_settlements_by_regex(name_regex, language=LANGUAGE_UK):
    print(f"[find_settlements_by_regex] start. Regex: {name_regex} Language: {language}")
    search_start_time = time.time()

    search_field = UaLocationsSettlement.name_lower
    if language == LANGUAGE_EN:
        search_field = UaLocationsSettlement.name_en_lower

    settlements = UaLocationsSettlement.query \
        .filter(
        and_(
            # search_field.op("~")(name_regex.lower())), for postgres
            search_field.op("regexp")(name_regex.lower())),
        UaLocationsSettlement.lat.isnot(None)) \
        .order_by(search_field) \
        .all()

    print(f"[find_settlements_by_regex] Query finished in {(time.time() - search_start_time) * 1000} milliseconds")
    print("[find_settlements_by_regex] Results found: " + str(len(settlements)))

    if not settlements:
        print(f"[find_settlements_by_regex] No results found by regex {name_regex}")
        return settlements

    # both sqlite and python sorts ukrainian letters incorrectly (і/ї)
    # attempt to fix it on the sqlite side (with collation) was done in poc/sorting_icu_collation branch,
    # but it wasn't successful. Below is a temporary (ha-ha) solution - sorting results on a python side
    if language == LANGUAGE_UK:
        settlements.sort(key=lambda x: collator.sort_key(x.name_lower))

    print(f"[find_settlements_by_regex] Search finished in {(time.time() - search_start_time) * 1000} milliseconds")

    return settlements


def find_settlements_without_coordinates():
    print("Searching settlements without coordinates")

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
