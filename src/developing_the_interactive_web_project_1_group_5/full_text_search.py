"""
Full Text Search Implementation
"""

import os
import atexit
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool


db_url = os.environ["DATABASE_URL"]
pool = None


def setup():
    global pool

    pool = ConnectionPool(db_url, open=True, kwargs={"row_factory": dict_row})
    atexit.register(pool.close)


# view all nodes- mostly for checking
def view():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT
               * FROM nodes
            """)
            rows = cur.fetchall()
            for row in rows:
                print(row)
            return rows


# get nodes for full tech search
def full_text_search(keyword):
    queryCheck = keyword.replace(" ", " & ")
    print(queryCheck)
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT * FROM nodes WHERE textSearch @@ to_tsquery('english', %s ) ORDER BY ts_rank(textSearch, to_tsquery(%s)) DESC;""",
                (queryCheck, queryCheck),
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)
            return cur.fetchall()
