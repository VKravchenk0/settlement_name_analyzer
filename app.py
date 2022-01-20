from flask import Flask

from sqlalchemy.sql.expression import func
from database import recreate_db, db_session
from models import UaLocationsSettlement
from ua_locations_db_importer import save_ua_locations_from_json_to_db


def create_app():
    app = Flask(__name__)
    recreate_db()
    save_ua_locations_from_json_to_db()

    @app.route("/")
    def index():
        settlement = UaLocationsSettlement.query.order_by(func.random()).first()
        settlement_str = str(settlement)
        print("settlement found:")
        print(settlement_str)
        return settlement_str

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
