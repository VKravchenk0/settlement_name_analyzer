import os
import jsonpickle
from flask import Flask, render_template, request, send_from_directory, send_file

from src.config import DATABASE_URL
from src.converters import convert_settlements, convert_missing_coordinates_settlements
from src.database import db
from src.finders import find_settlements_by_regex, find_settlements_without_coordinates
from src.util import split_into_chunks_and_compress_into_archive
from flask_migrate import Migrate, upgrade


def create_app():
    app = Flask(__name__, static_url_path='')

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from src.models import UaLocationsSettlement

    migrate = Migrate(app, db)
    with app.app_context():
        upgrade()

    # serving js files
    @app.route('/js/<path:path>')
    def send_js(path):
        return send_from_directory('templates/js', path)

    # serving js files
    @app.route('/css/<path:path>')
    def send_css(path):
        return send_from_directory('templates/css', path)

    # https://flatlogic.com/blog/top-mapping-and-maps-api/
    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/api/settlements")
    def search_settlements():
        name_regex = request.args.get("settlement_name_regex")
        settlements = find_settlements_by_regex(name_regex)
        settlement_dtos = convert_settlements(settlements)
        response = app.response_class(
            response=jsonpickle.encode(settlement_dtos, unpicklable=False),
            status=200,
            mimetype='application/json'
        )
        return response

    if 'FLASK_ENV' in os.environ and os.environ['FLASK_ENV'] == 'development':
        @app.route("/locations-without-coordinates")
        def download_locations_without_coordinates():
            settlements_without_coordinates = find_settlements_without_coordinates()
            result_dtos = convert_missing_coordinates_settlements(settlements_without_coordinates)
            zip_file = split_into_chunks_and_compress_into_archive(result_dtos, number_of_chunks=5)

            return send_file(zip_file, download_name='settlements_without_coordinates.zip', as_attachment=True)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
