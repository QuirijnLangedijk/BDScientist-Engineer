import pymysql as mysql
import os
from sqlalchemy import create_engine


def connect_to_db():
    '''
    return mysql.connect(host=os.environ['DB_HOST'],
                         port=int(os.environ['DB_PORT']),
                         database=os.environ['DB_NAME'],
                         user=os.environ['DB_USER'],
                         password=os.environ['DB_PW'])
    '''
    # return create_engine('mysql+pymysql://user:password@localhost/database')
    return create_engine('mysql+pymysql://{}:{}@{}/{}'.format(os.environ['DB_USER'], os.environ['DB_PW'], os.environ['DB_HOST'], os.environ['DB_NAME']))


def upload_to_db(df):
    engine = connect_to_db()
    con = engine.connect()
    try:
        with engine.connect() as conn, conn.begin():
            print('here')
            df.to_sql('dataset', conn, if_exists='replace')
    except Exception as e:
        print(e)
    finally:
        con.close()
