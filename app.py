from flask import Flask, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
from flask import Response

from sqlalchemy.sql.expression import func
from src.database import recreate_db, db_session
from src.image_creator import plot_settlements
from src.models import UaLocationsSettlement
from src.ua_locations_db_importer import save_ua_locations_from_json_to_db


def create_app():
    app = Flask(__name__)

    # TODO: work on migrations if needed
    # recreate_db_and_import_data()

    @app.route("/")
    def index():
        settlement = UaLocationsSettlement.query.order_by(func.random()).first()
        settlement_str = str(settlement)
        print("settlement found:")
        print(settlement_str)
        return settlement_str

    @app.route("/example-render-template")
    def server_side_template():
        settlement = UaLocationsSettlement.query.order_by(func.random()).first()
        return render_template('example-render-template.html', settlement=settlement)

    @app.route("/render-image", methods=['post', 'get'])
    def render_image():
        return render_template('render-image.html')

    @app.route('/plot.png')
    def plot_png():
        settlements = UaLocationsSettlement.query.order_by(func.random()).limit(5).all()
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
