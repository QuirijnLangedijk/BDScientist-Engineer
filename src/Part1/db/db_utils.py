import os
from sqlalchemy import create_engine
import pandas as pd


def connect_to_db():
    return create_engine('mysql+pymysql://{}:{}@{}/{}'.format(os.environ['DB_USER'], os.environ['DB_PW'], os.environ['DB_HOST'], os.environ['DB_NAME']))


def upload_to_db(df, table_name):
    try:
        engine = connect_to_db()
        with engine.connect() as conn, conn.begin():
            df.to_sql(table_name, conn, if_exists='replace')
    except Exception as e:
        print(e)
    finally:
        conn.close()


def get_from_db(sql):
    engine = connect_to_db()
    conn = engine.connect()
    try:
        return pd.read_sql_query(sql, con=conn)
    except Exception as e:
        print(e)
    finally:
        conn.close()
