from sqlalchemy import text
from src.database import db


def save(model):
    db.session.add(model)
    db.session.commit()

def save_list(model_list):
    db.session.add_all(model_list)
    db.session.commit()


def execute_native_sql_from_file(file_path):
    file = open(file_path)
    query = text(file.read())
    db.engine.execute(query)


def execute_native_sql(sql_string):
    query = text(sql_string)
    db.engine.execute(query)
