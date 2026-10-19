import os
import atexit
import datetime
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from werkzeug.utils import secure_filename


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
            cur.execute("select * from nodes where category = false;")
            return cur.fetchall()

# get every single category in the table
def get_all_categories():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("select * from nodes where category = true;")
            return cur.fetchall()

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
def get_user_nodes(subId):
    with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''select * 
                                from nodes
                                where subId = %s;''', (subId,))
                return cur.fetchall()

# get a user's saved nodes
def get_saved_nodes(subId):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''select * 
                            from nodes
                            where nodeId in (
                                select nodeId 
                                from savedNodes 
                                where subId = %s);''', (subId,))
            return cur.fetchall()

# get a user's recent nodes
def get_recent_nodes(subId):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''select * 
                            from nodes 
                            where nodeId in (
                                select nodeId 
                                from recentNodes 
                                where subId = %s);''', (subId,))
            return cur.fetchall()

# retrieve a user's notifications
def get_notifs(userid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
            select U1.username, U1.profPic, N1.nodeId as userNode, N1.title as userTitle, N2.nodeId as connectingNode, N2.title as connectingTitle, notif.timestamp, notif.notifid
            from nodes as N1, nodes as N2, users as U1, notifications as notif
            where notif.recipient = %s and
                U1.userId = notif.connector and
                N1.nodeId = notif.usersNode and
                N2.nodeId = notif.connectingNode
            order by timestamp asc;''', (userid,))

            return cur.fetchall()
            # [{'username': 'Samantha', 'profpic': None, 'usernode': 5, 'title': 'Plates', 'connectingnode': 6, 'timestamp': '2026-10-17 10:47:51.285334'}, {'username': 'Samantha', 'profpic': None, 'usernode': 4, 'title': 'Plates', 'connectingnode': 6, 'timestamp': '2026-10-17 10:49:25.671458'}]

def get_notif_recipient(notif_id):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''select recipient from notifications where notifId = %s;''', (notif_id,))
            return cur.fetchone()

def get_image(cur, picture):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''SELECT data, mimetype FROM images WHERE imageId = %s;''', (image_id,))
            return cur.fetchone()



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
            cur.execute('''select * from connections where nodeId1 = %s and nodeId2 = %s;''', (node2, node1))
            exists = cur.fetchone()
            if not exists:
                cur.execute('''insert into connections (nodeId1, nodeId2, connectorId)
                                values (%s, %s, %s);''', (node1, node2, connector))

                # also insert into the notification table
                add_notification(node1, node2, connector)
        
# add a notification (used in add_connection)
def add_notification(node1, node2, connector):
    with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''select creatorId from nodes where nodeid = %s;''', (node1))
                node1user = cur.fetchone()
                cur.execute('''select creatorId from nodes where nodeid = %s;''', (node2))
                node2user = cur.fetchone()

                timestamp = datetime.datetime.now()

                if connector != node1user:
                    cur.execute('''insert into notifications (recipient, connector, usersNode, connectingNode, timestamp)
                                    values (%s, %s, %s, %s, %s);''', (node1user, connector, node1, node2, timestamp))
                if connector != node2user and node1user != node2user:
                    cur.execute('''insert into notifications (recipient, connector, usersNode, connectingNode, timestamp)
                                    values (%s, %s, %s, %s, %s);''', (node2user, connector, node2, node1, timestamp))


# add a node to a user's saved nodes
def add_to_saved_nodes(subId, nodeid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''insert into savedNodes (subId, nodeId)
                            values (%s, %s);''', (subId, nodeid))

# add a node to a user's recent nodes
def add_to_recent_nodes(subId, nodeid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            num_history = 10
            cur.execute('''select count(nodeId) from recentNodes where userId = %s''', (userid,))
            count = cur.fetchone()

            # remove oldest node in the history
            if count.get("count") == num_history:
                cur.execute('''select * from recentNodes where userId = %s order by timestamp;''', (userid,))
                recents = cur.fetchall()
                to_delete = recents[0].get("nodeid") 
                cur.execute('''delete from recentNodes where userId = %s and nodeId = %s''', (userid, to_delete))

            timestamp = datetime.datetime.now(datetime.timezone.utc)
            cur.execute('''insert into recentNodes (userId, nodeId, timestamp)
                            values (%s, %s, %s);''', (userid, nodeid, timestamp))
            timestamp = datetime.datetime.now()
            cur.execute('''insert into recentNodes (subId, nodeId, timestamp)
                            values (%s, %s, %s);''', (subId, nodeid, timestamp))

# Putting an uploaded file into the images table. Returns imageId (or none)
def save_image(cur, picture):
    if not picture or not picture.filename:
        return None
    if not picture.mimetype.startswith("image/"):
        return None
    cur.execute('''INSERT INTO images (filename, mimetype, data) VALUES (%s, %s, %s) RETURNING imageId''',
                (secure_filename(picture.filename), picture.mimetype, picture.read()),
    )
    return cur.fetchone()["imageid"]


# ---------------- UPDATE ----------------

#NOTE: Can you change a node's topic?
# update a node with new values
def edit_node(title=None, image=None, desc=None):
    with pool.connection() as conn:
        with conn.cursor() as cur:

            cur.execute('''update nodes 
                            set title = %s, img = %s, description = %s''', (title, image, desc))

# update a user with new values
def edit_user(subId, username, bio, picture):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''update users 
                            set username = %s, bio = %s where subId = %s''', (username, bio, subId))
            image_id = save_image(cur, picture)
            if image_id:
                cur.execute('''update users 
                            set profpicid = %s where subId = %s''', (image_id, subId))

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

def remove_from_saved(subId, nodeid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''delete from savedNodes where nodeId = %s and subId = %s;''', (nodeid,subId))

def delete_notif(notifid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''delete from notifications where notifId = %s;''', (notifid,))

#NOTE: Do we need this?
def remove_from_recent():
    return