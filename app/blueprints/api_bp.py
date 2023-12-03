import os

import jsonpickle
from flask import Blueprint, send_file, request, Response

from app.config import PATTERN_BLACKLIST
from app.service.converters import convert_settlements, convert_missing_coordinates_settlements
from app.service.finders import find_settlements_by_regex, find_settlements_without_coordinates
from app.misc.util import split_into_chunks_and_compress_into_archive

api_bp = Blueprint('api_bp', __name__)


@api_bp.route("/api/settlements")
def search_settlements():
    name_regex = request.args.get("settlement_name_regex")
    print(f"Search settlements: {name_regex}")

    if not name_regex:
        return "Missing settlement_name_regex request param", 400

    if name_regex.strip() in PATTERN_BLACKLIST:
        return Response(
            response=jsonpickle.encode([], unpicklable=False),
            status=200,
            mimetype='application/json'
        )

    settlements = find_settlements_by_regex(name_regex)
    settlement_dtos = convert_settlements(settlements)

    response = Response(
        response=jsonpickle.encode(settlement_dtos, unpicklable=False),
        status=200,
        mimetype='application/json'
    )
    return response


if 'FLASK_ENV' in os.environ and os.environ['FLASK_ENV'] == 'development':
    @api_bp.route("/api/locations-without-coordinates")
    def download_locations_without_coordinates():
        settlements_without_coordinates = find_settlements_without_coordinates()
        result_dtos = convert_missing_coordinates_settlements(settlements_without_coordinates)
        zip_file = split_into_chunks_and_compress_into_archive(result_dtos, number_of_chunks=1)

        return send_file(zip_file, download_name='settlements_without_coordinates.zip', as_attachment=True)
