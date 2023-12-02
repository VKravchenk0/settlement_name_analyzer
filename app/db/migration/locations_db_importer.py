from app.config import LOCATIONS_IMPORT_BATCH_NUMBER
from app.db.crud import save_list
import json, os
from app.db.database import db
from datetime import datetime

from app.db.models import UaLocationsSettlement
from app.misc.util import replace_latin_letters_with_cyrillic, replace_apostrophe, timeit, split_list


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
        settlement.update_file_name = "ua_locations_10_11_2021.json"

        result.append(settlement)
    return result


@timeit
def save_locations_from_json_to_db():
    print("Base locations import -> start")
    locations_list = read_json_file('./resources/ua_locations_db/ua_locations_10_11_2021.json')
    print(f"Saving {len(locations_list)} locations")
    if LOCATIONS_IMPORT_BATCH_NUMBER > 1:
        batches = split_list(locations_list, LOCATIONS_IMPORT_BATCH_NUMBER)
        print(f"Splitting locations in {LOCATIONS_IMPORT_BATCH_NUMBER} batches")
        for batch in batches:
            convert_and_save_list(batch)
    else:
        convert_and_save_list(locations_list)
    print("Base locations import -> finished")
    count = UaLocationsSettlement.query.count()
    print(f"Count of records in db: {count}")


def convert_and_save_list(locations_list):
    print(f"Processing batch of {len(locations_list)} records")
    settlements = convert_raw_entry_to_model(locations_list)
    save_list(settlements)


def execute_updates():
    dir_name = './resources/ua_locations_db/updates'
    for filename in os.listdir(dir_name):
        file_path = os.path.join(dir_name, filename)
        json_object = read_json_file(file_path)
        process_updated_locations(filename, json_object)


def process_updated_locations(filename, json_object):
    for entry in json_object:
        settlement = db.session.query(UaLocationsSettlement).get(int(entry['id']))

        if 'lat' in entry:
            settlement.lat = float(entry['lat'])
        if 'lng' in entry:
            settlement.lng = float(entry['lng'])
        if 'meta' in entry:
            update_meta = entry['meta']
            existing_meta_copy = dict(settlement.meta)
            existing_meta_copy.update(update_meta)
            settlement.meta = existing_meta_copy
        if 'name' in entry:
            update_name = entry['name']
            existing_name_copy = dict(settlement.name)
            existing_name_copy.update(update_name)
            settlement.name = existing_name_copy
        if 'public_name' in entry:
            update_public_name = entry['public_name']
            existing_public_name_copy = dict(settlement.public_name)
            existing_public_name_copy.update(update_public_name)
            settlement.public_name = existing_public_name_copy
        if 'name_lower' in entry:
            settlement.name_lower = entry['name_lower']

        settlement.update_file_name = filename
        settlement.updated_at = datetime.now()
        db.session.commit()


def read_json_file(file_path):
    with open(file_path, 'r') as f:
        json_data = f.read()
        result = json.loads(json_data)
        f.close()
        return result
