import json

import sqlite_icu
from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config import DATABASE_URL
# from ua_locations_db_importer import save_ua_locations_from_json_to_db

# https://stackoverflow.com/questions/66690321/flask-and-heroku-sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy
# database_path = database_path.replace("postgres://", "postgresql://")

engine = create_engine(DATABASE_URL,
                       # ensures unicode symbols are not converted to ascii. see
                       # https://github.com/sqlalchemy/sqlalchemy/issues/4798#issuecomment-519760839
                       json_serializer=lambda x: json.dumps(x, ensure_ascii=False))
#
# with engine.connect() as connection:
#     result = connection.execute("SELECT icu_load_collation('uk_UA', 'ukrainian');")
#     print("result:", result)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# https://stackoverflow.com/questions/48851097/how-to-load-a-sqlite3-extension-in-sqlalchemy
db_collate = 'tr_TR'
def load_extension(dbapi_conn, unused):
    print("load extension start")
    dbapi_conn.enable_load_extension(True)
    replace = sqlite_icu.extension_path().replace('.so', '')
    print(f"Extension path: {replace}")
    dbapi_conn.load_extension(replace)
    dbapi_conn.enable_load_extension(False)
    dbapi_conn.execute("SELECT icu_load_collation(?, 'tr_TR')", (db_collate,))
    fetchone = dbapi_conn.execute("SELECT upper('i', 'tr_TR')").fetchone()
    # Цей участок працює
    print(f"fetchone {fetchone}")
    assert fetchone == ('İ',)


def recreate_db(app):
    print('recreate db start')
    with app.app_context():
        listen(engine, 'connect', load_extension)
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling recreate_db()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # save_ua_locations_from_json_to_db()
