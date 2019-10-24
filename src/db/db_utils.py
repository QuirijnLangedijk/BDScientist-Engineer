import os
from sqlalchemy import create_engine
import pymysql
import pandas as pd


def connect_to_db():
    '''
    return mysql.connect(host=os.environ['DB_HOST'],
                         port=int(os.environ['DB_PORT']),
                         database=os.environ['DB_NAME'],
                         user=os.environ['DB_USER'],
                         password=os.environ['DB_PW'])
    '''
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
    try:
        engine = connect_to_db()
        conn = engine.connect()
        return pd.read_sql_query(sql, con=conn)
    except Exception as e:
        print(e)
    finally:
        conn.close()
