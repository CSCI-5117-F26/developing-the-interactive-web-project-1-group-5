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



# ---------------- READ ----------------

# get a node's information
def get_node(nodeid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("select * from nodes where nodeId = %s;", (nodeid,))
            return cur.fetchone()

# get a user's information
def get_user(subId):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("select * from users where subId = %s;", (subId,))
            return cur.fetchone()
        

# get all nodeids connected to a node
def get_node_connections(nodeid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''select * 
                            from nodes
                            where nodeId in (
                                select nodeId2 
                                from connections 
                                where nodeId1 = %s);''', (nodeid,))
            return cur.fetchall()

# get all nodes with a certain topic
def get_nodes_by_topic(topic):
    with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("select * from nodes where topic = %s;", (topic,))
                return cur.fetchall()

# get nodes that a user has created
def get_user_nodes(userid):
    with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''select * 
                                from nodes
                                where creatorId = %s;''', (userid,))
                return cur.fetchall()

# get a user's saved nodes
def get_saved_nodes(userid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''select * 
                            from nodes
                            where nodeId in (
                                select nodeId 
                                from savedNodes 
                                where userId = %s);''', (userid,))
            return cur.fetchall()

# get a user's recent nodes
def get_recent_nodes(userid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''select * 
                            from nodes 
                            where nodeId in (
                                select nodeId 
                                from recentNodes 
                                where userId = %s);''', (userid,))
            return cur.fetchall()

# ---------------- CREATE ----------------

# add a node to the node table
def add_node(creatorId, title, image, desc=None, topic=None): # which ones are required?
    #TODO: input validation??

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''insert into nodes (title, img, description, creatorId, topic)
                            values (%s, %s, %s, %s, %s);''', (title, image, desc, creatorId, topic))

# add a user
def add_user(subId, username, bio=None, profilepic=None):
    #TODO: input validation??

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''insert into users (subId, username, bio, profPic)
                            values (%s, %s, %s, %s);''', (subId, username, bio, profilepic))

# add a connection between two nodes to the connections table
def add_connection(node1, node2, connector):
    with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('''insert into connections (nodeId1, nodeId2, connectorId)
                                    values (%s, %s, %s);''', (node1, node2, connector))

# add a node to a user's saved nodes
def add_to_saved_nodes(userid, nodeid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''insert into savedNodes (userId, nodeId)
                            values (%s, %s);''', (userid, nodeid))

# add a node to a user's recent nodes
def add_to_recent_nodes(userid, nodeid):
    with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''insert into recentNodes (userId, nodeId)
                                values (%s, %s);''', (userid, nodeid))

    