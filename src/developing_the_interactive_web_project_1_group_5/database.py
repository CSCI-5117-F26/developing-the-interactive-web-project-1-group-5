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

# get a node's information
def get_node(nodeid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("select * from nodes where nodeId = %s", nodeid)
            return cur.fetchone()

# get a user's information
def get_user(userid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("select * from users where userId = %s", userid)
            return cur.fetchone()

# get all nodeids connected to a node
def get_node_connections(nodeid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''select nodeId2 
                            from connections 
                            where nodeId1 = %s''', nodeid)
            return cur.fetchall()

# get a user's saved nodes
def get_saved_nodes(userid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''select nodeId 
                            from savedNodes 
                            where userId = %s''', userid)
            return cur.fetchall()

# get a user's recent nodes
def get_recent_nodes(userid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''select nodeId 
                            from recentNodes 
                            where userId = %s''', userid)
            return cur.fetchall()

# add a node to the node table
def add_node(creatorId, title, image, desc=None, topic=None): # which ones are required?
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''insert into nodes ()''')

# add a user
def add_user(username, bio=None, profilepic=None):
    name = username
    userbio = pic = None

    if bio:
        # input validation here?
        userbio = bio
    if profilepic:
        pic = profilepic

    with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''insert into users (username, bio, profPic)
                                values (%s, %s, %s);''', (name, userbio, pic))

# add a connection between two nodes to the connections table
def add_connection():
    return

