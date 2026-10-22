"""
Full Text Search Implementation
"""

import developing_the_interactive_web_project_1_group_5.database as database


# view all nodes- mostly for checking
def view():
    with database.pool.connection() as conn:
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
    with database.pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT * FROM nodes WHERE textSearch @@ to_tsquery('english', %s ) ORDER BY ts_rank(textSearch, to_tsquery(%s)) DESC;""",
                (queryCheck, queryCheck),
            )

            return cur.fetchall()


"""
Full Text Search Implementation
"""

import developing_the_interactive_web_project_1_group_5.database as database


# view all nodes- mostly for checking
def view():
    with database.pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT
               * FROM nodes
            """)
            return cur.fetchall()


# get nodes for full tech search
def full_text_search(keyword):
    queryCheck = keyword.replace(" ", " & ")
    print(queryCheck)
    with database.pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT * FROM nodes WHERE textSearch @@ to_tsquery('english', %s ) ORDER BY ts_rank(textSearch, to_tsquery(%s)) DESC;""",
                (queryCheck, queryCheck),
            )

            return cur.fetchall()
