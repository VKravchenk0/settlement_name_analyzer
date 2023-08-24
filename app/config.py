import os

basedir = os.path.abspath(os.path.dirname(__file__))

LOCATIONS_IMPORT_BATCH_NUMBER = int(os.environ.get('LOCATIONS_IMPORT_BATCH_NUMBER', 20))

class Config:
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///settlements.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'settlements.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
