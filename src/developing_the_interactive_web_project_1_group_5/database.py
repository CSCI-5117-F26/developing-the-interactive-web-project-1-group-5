import os
import atexit
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row


db_url = os.environ["DATABASE_URL"]

pool = None

def setup():
    global pool

    pool = ConnectionPool(db_url, open=True, kwargs={"row_factory": dict_row})
    atexit.register(pool.close)



