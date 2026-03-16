from config import *
import mysql.connector

def make_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn
def create_Table(cursor,TAB):
    ddl=f'''CREATE TABLE IF NOT EXISTS {TAB}(
            id       INT AUTO_INCREMENT PRIMARY KEY,
            name     VARCHAR(255)  NOT NULL,
            city     VARCHAR(100),
            state    VARCHAR(100),
            address  VARCHAR(500),
            phone    VARCHAR(50),
            timings  VARCHAR(255),
            website  VARCHAR(500),
            map_url  VARCHAR(500)
    
    );'''
    cursor.execute(ddl)
def insert_into_db(data, cursor, con):
    try:
        cols = ",".join(data[0].keys())
        vals = ",".join(["%s"] * len(data[0].keys()))
        insert_query = f"INSERT INTO `{TABLE_NAME}` ({cols}) VALUES ({vals});"
        rows = [tuple(p_data.values()) for p_data in data]
        cursor.executemany(insert_query, rows)
        con.commit()
        print(f"{cursor.rowcount} rows inserted.")
    except Exception as e:
        con.rollback()
        print("Error", insert_into_db.__name__, e)