import os
import atexit
import datetime
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

# get every single node in the table (exclude categories)
def get_all_nodes():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("select nodeId from nodes where category = false;")
            return cur.fetchall()

# get every single category in the table
def get_all_categories():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("select nodeId from nodes where category = true;")
            return cur.fetchall()

# get a user's information
def get_user(userid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("select * from users where userId = %s;", (userid,))
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
                                where nodeId1 = %s) or nodeId in (
                                                    select nodeId1
                                                    from connections
                                                    where nodeId2 = %s);''', (nodeid,nodeid))
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

# TODO: add auth0 stuff
# add a user
def add_user(username, bio=None, profilepic=None):
    #TODO: input validation??

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''insert into users (username, bio, profPic)
                            values (%s, %s, %s);''', (username, bio, profilepic))

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

#TODO: remove the first-in/oldest node when adding the 11th node
# add a node to a user's recent nodes
def add_to_recent_nodes(userid, nodeid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            timestamp = datetime.datetime.now()
            cur.execute('''insert into recentNodes (userId, nodeId, timestamp)
                            values (%s, %s, %s);''', (userid, nodeid, timestamp))



# ---------------- UPDATE ----------------

#NOTE: Can you change a node's topic?
# update a node with new values
def edit_node(title=None, image=None, desc=None):
    with pool.connection() as conn:
        with conn.cursor() as cur:

            cur.execute('''update nodes 
                            set title = %s, img = %s, description = %s''', (title, image, desc))

# update a user with new values
def edit_user(name=None, bio=None, pic=None):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''update users 
                            set username = %s, bio = %s, profPic = %s''', (name, bio, pic))

# ---------------- DELETE ----------------

def delete_node(nodeid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''delete from nodes where nodeId = %s;''', (nodeid,))

def delete_connection(nodeid1, nodeid2):
    with pool.connection() as conn:
            with conn.cursor() as cur:
                # delete both possibilities
                cur.execute('''delete from connections where nodeId1 = %s and nodeId2 = %s;''', (nodeid1, nodeid2))
                cur.execute('''delete from connections where nodeId1 = %s and nodeId2 = %s;''', (nodeid2, nodeid1))

def remove_from_saved(userid, nodeid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''delete from savedNodes where nodeId = %s and userId = %s;''', (nodeid,userid))

#NOTE: Do we need this?
def remove_from_recent():
    return