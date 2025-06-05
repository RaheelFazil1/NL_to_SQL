from sqlalchemy import create_engine
import pandas as pd
from config import DB_CONFIG
import pyodbc

def connect_to_db():
    # conn_str = (
    #     f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    #     f"SERVER={DB_CONFIG['server']};"
    #     f"DATABASE={DB_CONFIG['database']};"
    #     f"UID={DB_CONFIG['user']};"
    #     f"PWD={DB_CONFIG['password']}"
    # )
    # connection_string = (
    #     f"mssql+pyodbc://@localhost/{DB_CONFIG['database']}?"
    #     f"driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    # )

    # connection_string = (
    #     f"mssql+pyodbc://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['server']}/{DB_CONFIG['database']}?"
    #     f"driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    # )

    username = DB_CONFIG['user']
    password = DB_CONFIG['password']
    server = DB_CONFIG['server']
    database = DB_CONFIG['database']
    driver = 'ODBC Driver 17 for SQL Server'

    connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
    try:
        # conn = pyodbc.connect(connection_string)
        engine = create_engine(connection_string)
        print("[INFO]: Connected to SQL Server successfully.")
        return engine
    except Exception as e:
        print(f"[Connection Error]: {e}")
        return None

def execute_sql_query(query, conn, params=None):
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    except Exception as e:
        print(f"[SQL Execution Error]: {e}")
        return None

# db_connection = connect_to_db()
# TABLE_NAME = "Test_TSSR"
# my_query = f"SELECT * FROM {TABLE_NAME} WHERE site_location = 'Residential Area'"
# result_df = execute_sql_query(my_query, db_connection)
#
# print(result_df)


