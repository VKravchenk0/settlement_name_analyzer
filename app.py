from flask import Flask

# from database import db_session
from database import recreate_db
from ua_locations_db_importer import save_ua_locations_from_json_to_db

app = Flask(__name__)


@app.route("/")
def index():
    print("index endpoint")
    recreate_db()
    save_ua_locations_from_json_to_db()
    return "Цьомк!"


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db_session.remove()

if __name__ == "__main__":
    app.run()
