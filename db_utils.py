import pyodbc
import pandas as pd
from config import DB_CONFIG

def connect_to_db():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['user']};"
        f"PWD={DB_CONFIG['password']}"
    )
    try:
        conn = pyodbc.connect(conn_str)
        print("[+] Connected to SQL Server successfully.")
        return conn
    except Exception as e:
        print(f"[Connection Error]: {e}")
        return None

def execute_sql_query(conn, query, params=None):
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    except Exception as e:
        print(f"[SQL Execution Error]: {e}")
        return None