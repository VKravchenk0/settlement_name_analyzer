import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///settlements.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'settlements.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
