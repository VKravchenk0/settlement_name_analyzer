from sqlalchemy import text
from src.database import engine, db_session


def save(model):
    db_session.add(model)
    db_session.commit()

def save_list(model_list):
    db_session.add_all(model_list)
    db_session.commit()


def execute_native_sql_from_file(file_path):
    with engine.connect() as con:
        file = open(file_path)
        query = text(file.read())
        con.execute(query)


def execute_native_sql(sql_string):
    with engine.connect() as con:
        query = text(sql_string)
        con.execute(query)