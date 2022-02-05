import json
from typing import List

import jsonpickle
from flask import Flask, render_template, request, send_from_directory
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
from flask import Response, redirect

from sqlalchemy.sql.expression import func
from sqlalchemy import and_

from src.converters import convert_settlements
from src.database import recreate_db, db_session
from src.image_creator import plot_settlements
from src.models import UaLocationsSettlement
from src.ua_locations_db_importer import save_ua_locations_from_json_to_db


def create_app():
    app = Flask(__name__, static_url_path='')

    # TODO: work on migrations if needed
    # recreate_db_and_import_data()

    # serving js files
    @app.route('/js/<path:path>')
    def send_js(path):
        return send_from_directory('templates/js', path)

    # https://flatlogic.com/blog/top-mapping-and-maps-api/
    @app.route("/")
    def client_side_rendering():
        return render_template('client-side-rendering.html')

    # legacy url
    @app.route("/client-side-rendering")
    def client_side_rendering_legacy():
        return redirect('/', code=302)

    @app.route("/api/settlements")
    def search_settlements():
        name_regex = request.args.get("settlement_name_regex")
        print(f"settlement name to search: ${name_regex}")
        settlements = UaLocationsSettlement.query \
            .filter(
            and_(
                UaLocationsSettlement.name['uk'].as_string().op("~")(name_regex)),
            UaLocationsSettlement.lat.isnot(None)) \
            .all()
        print("result found: " + str(settlements))
        if not settlements:
            print(f"No results found by regex {name_regex}")
        settlement_dtos = convert_settlements(settlements)
        response = app.response_class(
            response=jsonpickle.encode(settlement_dtos, unpicklable=False),
            status=200,
            mimetype='application/json'
        )
        return response

    @app.route("/random-settlement")
    def random_settlement():
        settlement = UaLocationsSettlement.query.order_by(func.random()).first()
        settlement_str = str(settlement)
        print("settlement found:")
        print(settlement_str)
        return settlement_str

    @app.route("/render-image", methods=['post', 'get'])
    def render_image():
        name_regex = ''
        settlements = []
        settlement_ids = []
        if request.method == 'POST':
            name_regex = request.form.get('settlement_name_regex')  # access the data inside
            print("searching by regex " + name_regex)
            settlements = UaLocationsSettlement.query \
                .filter(
                    and_(
                        UaLocationsSettlement.name['uk'].as_string().op("~")(name_regex)),
                        UaLocationsSettlement.lat.isnot(None)) \
                .all()
            print("result found: " + str(settlements))
            if not settlements:
                print(f"No results found by regex {name_regex}")
            for s in settlements:
                settlement_ids.append(str(s.id))
        return render_template('render-image.html', settlements=settlements, settlement_ids=",".join(settlement_ids),
                               settlement_name_regex=name_regex)

    @app.route('/plot.png')
    def plot_png():
        settlement_ids_string = request.args.get("settlement_ids")
        settlement_ids = settlement_ids_string.split(",")
        settlements = UaLocationsSettlement.query.filter(UaLocationsSettlement.id.in_(settlement_ids)).all()
        fig = plot_settlements(settlements)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app


def recreate_db_and_import_data():
    # Add migrations if needed
    # https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
    # https://stackoverflow.com/questions/37863235/how-to-wire-up-migrations-in-flask-with-declarative-base
    recreate_db()
    save_ua_locations_from_json_to_db()


app = create_app()

if __name__ == "__main__":
    app.run()
