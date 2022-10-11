import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config import DEFAULT_DATABASE_URL
# from ua_locations_db_importer import save_ua_locations_from_json_to_db

database_path = os.getenv('DATABASE_URL', DEFAULT_DATABASE_URL)
# https://stackoverflow.com/questions/66690321/flask-and-heroku-sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy
database_path = database_path.replace("postgres://", "postgresql://")

engine = create_engine(database_path,
                       # ensures unicode symbols are not converted to ascii. see
                       # https://github.com/sqlalchemy/sqlalchemy/issues/4798#issuecomment-519760839
                       json_serializer=lambda x: json.dumps(x, ensure_ascii=False))

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def recreate_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling recreate_db()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
