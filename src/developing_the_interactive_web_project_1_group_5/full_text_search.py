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
    keyword = keyword.strip()

    if not keyword:
        return []

    with database.pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT * FROM nodes WHERE "textSearch" @@ plainto_tsquery('english', %s ) ORDER BY ts_rank(
                    "textSearch",
                    plainto_tsquery('english', %s)
                )  DESC;""",
                (keyword, keyword),
            )

            return cur.fetchall()
