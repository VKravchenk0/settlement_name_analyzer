import csv
import os
import io

import jsonpickle
from flask import Blueprint, send_file, request, Response, make_response, jsonify

from app.service.converters import convert_settlements, convert_missing_coordinates_settlements
from app.service.finders import find_settlements_by_regex, find_settlements_without_coordinates
from app.misc.util import split_into_chunks_and_compress_into_archive

api_bp = Blueprint('api_bp', __name__)


@api_bp.route("/api/settlements")
def search_settlements():
    name_regex = request.args.get("settlement_name_regex")
    settlements = find_settlements_by_regex(name_regex)
    settlement_dtos = convert_settlements(settlements)
    # TODO: not sure if using Response instead of app.response_class is fine
    response = Response(
        response=jsonpickle.encode(settlement_dtos, unpicklable=False),
        status=200,
        mimetype='application/json'
    )
    return response


@api_bp.route("/api/settlements/export")
def export_to_file():
    name_regex = request.args.get("settlement_name_regex")
    file_format = request.args.get("file_format")
    if not file_format and (file_format not in ['json', 'csv']):
        return f"Invalid file format {file_format}. Must be either 'json' or 'csv'", 400

    settlements = find_settlements_by_regex(name_regex)
    settlement_dtos = convert_settlements(settlements)

    if file_format == 'csv':
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerow(["id", "name", "lat", "lon", "region", "district", "community"])
        for dto in settlement_dtos:
            cw.writerow(vars(dto).values())
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output
    elif file_format == 'json':
        string_json = jsonpickle.encode(settlement_dtos, unpicklable=False, indent=2)

        return Response(string_json,
                        mimetype='application/json',
                        headers={'Content-Disposition': 'attachment;filename=export.json'})




if 'FLASK_ENV' in os.environ and os.environ['FLASK_ENV'] == 'development':
    @api_bp.route("/api/locations-without-coordinates")
    def download_locations_without_coordinates():
        settlements_without_coordinates = find_settlements_without_coordinates()
        result_dtos = convert_missing_coordinates_settlements(settlements_without_coordinates)
        zip_file = split_into_chunks_and_compress_into_archive(result_dtos, number_of_chunks=5)

        return send_file(zip_file, download_name='settlements_without_coordinates.zip', as_attachment=True)
