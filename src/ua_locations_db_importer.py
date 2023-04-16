from sqlalchemy_utils import database_exists

from src.config import DATABASE_URL
from src.crud import save_list, save
import json, os
from src.database import db_session
from datetime import datetime

from src.models import UaLocationsSettlement, ImportSuccessFlag
from src.util import replace_latin_letters_with_cyrillic, replace_apostrophe


def convert_to_string_and_strip(input_value):
    if not input_value:
        return input_value
    return str(input_value).strip()


def process_json_entry(json_obj):
    result = {}
    for key, value in json_obj.items():
        if isinstance(value, str):
            result_value = replace_apostrophe(value.strip())
            if key == 'uk':
                result_value = replace_latin_letters_with_cyrillic(result_value)
        elif isinstance(value, dict):
            result_value = process_json_entry(value)
        else:
            result_value = value
        result[key] = result_value
    return result


def convert_raw_entry_to_model(list):
    result = []
    for entry in list:
        settlement = UaLocationsSettlement()
        settlement.id = entry["id"]
        settlement.uuid = convert_to_string_and_strip(entry["uuid"])
        settlement.meta = process_json_entry(entry["meta"])
        date_format = '%Y-%m-%d %H:%M:%S.%f'
        settlement.created_at = datetime.strptime(entry["created_at"], date_format)
        settlement.updated_at = datetime.strptime(entry["updated_at"], date_format)
        settlement.type = convert_to_string_and_strip(entry["type"])
        settlement.name = process_json_entry(entry["name"])
        settlement.name_lower = settlement.name["uk"].lower()
        settlement.post_code = entry["post_code"]
        settlement.katottg = convert_to_string_and_strip(entry["katottg"])
        settlement.koatuu = convert_to_string_and_strip(entry["koatuu"])
        settlement.lng = entry["lng"]
        settlement.lat = entry["lat"]
        settlement.parent_id = entry["parent_id"]
        settlement.public_name = process_json_entry(entry["public_name"])

        result.append(settlement)
    return result


def save_ua_locations_from_json_to_db():
    print("Base locations import -> start")
    locations_list = read_json_file('./resources/ua_locations_db/ua_locations_10_11_2021.json')
    settlements = convert_raw_entry_to_model(locations_list)
    print(f"Base locations import. Saving {len(settlements)} locations")
    save_list(settlements)
    print("Base locations import -> finish")


def update_settlements_with_manual_coordinates():
    dir_name = './resources/ua_locations_db/manual_coordinates'
    for filename in os.listdir(dir_name):
        file_path = os.path.join(dir_name, filename)
        json_object = read_json_file(file_path)
        process_manual_coordinates_entires(json_object)


def process_manual_coordinates_entires(json_object):
    for entry in json_object:
        if entry["lat"] and entry["lon"]:
            #print(f"lat and lon values present for id {entry['id']}")
            UaLocationsSettlement.query.filter(UaLocationsSettlement.id == int(entry['id'])) \
                .update({
                    "lat": float(entry['lat']),
                    "lng": float(entry['lon']),
                    "coordinates_added_manually": True
            })
            db_session.commit()
        #else:
            #print(f"lat and long values are absent for id {entry['id']}")


def flag_import_as_successful():
    print("[flag_import_as_successful] Start")
    success_flag = ImportSuccessFlag()
    success_flag.id = 1
    success_flag.finished_at = datetime.now()
    success_flag.success = True
    print(f"[flag_import_as_successful] Saving {success_flag}")
    save(success_flag)
    print("[flag_import_as_successful] Finish")


def db_is_initialized():
    print("[db_is_initialized] Start")
    if not database_exists(DATABASE_URL):
        print("[db_is_initialized] Db not initialized")
        return False

    success_flags = ImportSuccessFlag.query.all()
    print(f"[db_is_initialized] Success flags found: {success_flags}")
    if len(success_flags) != 1:
        print("[db_is_initialized] Success flags length not equal to 1")
        return False
    if not success_flags[0].success:
        print(f"[db_is_initialized] Success flag value: {success_flags[0].success}")
        return False
    print("[db_is_initialized] DB is initialized")
    return True


def read_json_file(file_path):
    with open(file_path, 'r') as f:
        json_data = f.read()
        result = json.loads(json_data)
        f.close()
        return result
