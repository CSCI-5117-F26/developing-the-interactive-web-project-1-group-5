import os
import atexit
import datetime
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from werkzeug.utils import secure_filename
import dotenv

# for local testing
dotenv.load_dotenv()


# set up connection pool
db_url = os.environ["DATABASE_URL"]
pool = ConnectionPool(db_url, open=False, kwargs={"row_factory": dict_row})
atexit.register(pool.close)

is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
if not is_gunicorn:
    pool.open()

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
            cur.execute(
                """select * 
                            from nodes
                            where nodeId in (
                                select nodeId2 
                                from connections 
                                where nodeId1 = %s) or nodeId in (
                                                    select nodeId1
                                                    from connections
                                                    where nodeId2 = %s);""",
                (nodeid, nodeid),
            )
            return cur.fetchall()


# get node connection
def get_node_connection(node1, node2):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """select * from connections where ((nodeid1, nodeid2) = (%s, %s) 
                        or (nodeid2, nodeid1) = (%s, %s));""",
                (node1, node2, node1, node2),
            )
            return cur.fetchone()


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
            cur.execute(
                """select * 
                                from nodes
                                where subId = %s;""",
                (subId,),
            )
            return cur.fetchall()


# get a user's saved nodes
def get_saved_nodes(subId):
    with pool.connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """select * 
                            from nodes
                            where nodeId in (
                                select nodeId 
                                from savedNodes 
                                where subId = %s);""",
                (subId,),
            )
            return cur.fetchall()


# get a user's recent nodes
def get_recent_nodes(subId):
    with pool.connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """select * 
                            from nodes 
                            where nodeId in (
                                select nodeId 
                                from recentNodes 
                                where subId = %s);""",
                (subId,),
            )

            return cur.fetchall()


# retrieve a user's notifications
def get_notifs(subid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            select U1.username, U1.profPicId, N1.nodeId as userNode, N1.title as userTitle, 
                N2.nodeId as connectingNode, N2.title as connectingTitle, notif.timestamp, 
                notif.notifid, notif.deleted
            from nodes as N1, nodes as N2, users as U1, notifications as notif
            where notif.recipient = %s and
                U1.subId = notif.connector and
                N1.nodeId = notif.usersNode and
                N2.nodeId = notif.connectingNode
            order by timestamp desc;""",
                (subid,),
            )

            return cur.fetchall()
            # [{'username': 'Samantha', 'profpic': None, 'usernode': 5, 'title': 'Plates', 'connectingnode': 6, 'timestamp': '2026-10-17 10:47:51.285334'}, {'username': 'Samantha', 'profpic': None, 'usernode': 4, 'title': 'Plates', 'connectingnode': 6, 'timestamp': '2026-10-17 10:49:25.671458'}]


def get_notif(notif_id):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """select * from notifications where notifId = %s;""", (notif_id,)
            )
            return cur.fetchone()


def get_image(image_id):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT data, mimetype FROM images WHERE imageId = %s;""", (image_id,)
            )
            return cur.fetchone()
        
def get_user_pfp(subId):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """select profPicId
                   from users
                   where subId = %s;""",
                (subId,),
            )
            user = cur.fetchone()
            if (user and user["profpicid"]):
                return user["profpicid"]
            return None

            


# check if existing username
def check_username_taken(username):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """select count(1) from users where username = %s""", (username,)
            )
            return cur.fetchone()


# ---------------- CREATE ----------------


# add a node to the node table


def add_node(
    creatorId, title, image, desc=None, topic=None
):  # which ones are required?
    # TODO: input validation??

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """insert into nodes (title, description, subId, topic)
                            values (%s, %s, %s, %s) returning nodeId;""",
                (title, desc, creatorId, topic),
            )
            node_id = cur.fetchone()["nodeid"]
            image_id = save_image(cur, image)
            cur.execute(
                """update nodes 
                        set imgId = %s where nodeId = %s""",
                (image_id, node_id),
            )
            return node_id


# add a user
def add_user(subId, username, bio=None, profilepic=None):
    # TODO: input validation??

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """insert into users (subId, username, bio, profPicId)
                            values (%s, %s, %s, %s);""",
                (subId, username, bio, profilepic),
            )


# add a connection between two nodes to the connections table
def add_connection(node1, node2, connector):
    with pool.connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """select * from connections 
                    where nodeId1 = %s and nodeId2 = %s and connectorId = %s;""",
                (node1, node2, connector),
            )
            exists = cur.fetchone()
            if not exists:
                cur.execute(
                    """insert into connections (nodeId1, nodeId2, connectorId)
                                values (%s, %s, %s);""",
                    (node1, node2, connector),
                )

                # also insert into the notification table
                add_notification(node1, node2, connector)


# add a notification (used in add_connection)
def add_notification(node1, node2, connector):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""select subId from nodes where nodeid = %s;""", (node1,))
            node1user = cur.fetchone()['subid']
            cur.execute("""select subId from nodes where nodeid = %s;""", (node2,))
            node2user = cur.fetchone()['subid']

            timestamp = datetime.datetime.now()

            if connector != node1user:
                cur.execute(
                    """insert into notifications (recipient, connector, usersNode, connectingNode, timestamp)
                                    values (%s, %s, %s, %s, %s);""",
                    (node1user, connector, node1, node2, timestamp),
                )
            if connector != node2user and node1user != node2user:
                cur.execute(
                    """insert into notifications (recipient, connector, usersNode, connectingNode, timestamp)
                                    values (%s, %s, %s, %s, %s);""",
                    (node2user, connector, node2, node1, timestamp),
                )


# add a node to a user's saved nodes
def add_to_saved_nodes(subId, nodeid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """select * from savedNodes where subId = %s and nodeId = %s;""",
                (subId, nodeid),
            )
            exists = cur.fetchone()

            if exists:
                return

            cur.execute(
                """insert into savedNodes (subId, nodeId)
                            values (%s, %s);""",
                (subId, nodeid),
            )


# add a node to a user's recent nodes
def add_to_recent_nodes(subId, nodeid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """select * from recentNodes where subId = %s and nodeId = %s;""",
                (subId, nodeid),
            )
            exists = cur.fetchone()
            print(exists)

            if exists:
                num_history = 10
                cur.execute(
                    """select count(subid) from recentNodes where subid = %s""",
                    (subId,),
                )
                count = cur.fetchone()

                # remove oldest node in the history
                if count.get("count") == num_history:
                    cur.execute(
                        """select * from recentNodes where subid = %s order by timestamp;""",
                        (subId,),
                    )
                    recents = cur.fetchall()
                    to_delete = recents[0].get("nodeid")
                    cur.execute(
                        """delete from recentNodes where subid = %s and nodeId = %s""",
                        (subId, to_delete),
                    )

                timestamp = datetime.datetime.now()
                cur.execute(
                    """insert into recentNodes (subId, nodeId, timestamp)
                                values (%s, %s, %s);""",
                    (subId, nodeid, timestamp),
                )


# Putting an uploaded file into the images table. Returns imageId (or none)
def save_image(cur, picture):
    if not picture or not picture.filename:
        return None
    if not picture.mimetype.startswith("image/"):
        return None
    cur.execute(
        """INSERT INTO images (filename, mimetype, data) VALUES (%s, %s, %s) RETURNING imageId""",
        (secure_filename(picture.filename), picture.mimetype, picture.read()),
    )
    return cur.fetchone()["imageid"]


# removes image from image table. duh.
def delete_image(cur, image_id):
    # only delete if there are no nodes + users using the img
    cur.execute(
        """SELECT
               (SELECT COUNT(*) FROM nodes WHERE imgId = %s) +
               (SELECT COUNT(*) FROM users WHERE profPicId = %s)
               AS count;""",
        (image_id, image_id),
    )
    count = cur.fetchone()["count"]

    if count == 0:
        cur.execute("""DELETE FROM images WHERE imageId = %s;""", (image_id,))


# ---------------- UPDATE ----------------


# NOTE: Can you change a node's topic?


# NOTE: Can you change a node's topic?
# update a node with new values
def edit_node(nodeid, title=None, image=None, desc=None):
    with pool.connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """update nodes set title = %s, description = %s where nodeId = %s""",
                (title, desc, nodeid),
            )
            image_id = save_image(cur, image)
            if image_id:
                # image switch: store old imgId before replacing it
                cur.execute("""select * from nodes where nodeId = %s""", (str(nodeid),))
                old_id = cur.fetchone()["imgid"]
                # ye update
                cur.execute(
                    """update nodes 
                            set imgId = %s where nodeId = %s""",
                    (image_id, str(nodeid)),
                )
                if old_id:
                    delete_image(cur, old_id)


# update a user with new values
def edit_user(subId, username, bio, picture):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """update users 
                            set username = %s, bio = %s where subId = %s""",
                (username, bio, subId),
            )

            image_id = save_image(cur, picture)

            if image_id:
                # image switch: store old profpicid before replacing it
                cur.execute(
                    """select profpicid from users where subId = %s""", (subId,)
                )
                old_id = cur.fetchone()["profpicid"]
                # ye update
                cur.execute(
                    """update users 
                            set profpicid = %s where subId = %s""",
                    (image_id, subId),
                )
                if old_id:
                    delete_image(cur, old_id)


# ---------------- DELETE ----------------


def delete_node(nodeid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""delete from nodes where nodeId = %s;""", (nodeid,))


def delete_connection(nodeid1, nodeid2):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            # delete both possibilities
            cur.execute(
                """delete from connections where nodeId1 = %s and nodeId2 = %s;""",
                (nodeid1, nodeid2),
            )
            cur.execute(
                """delete from connections where nodeId1 = %s and nodeId2 = %s;""",
                (nodeid2, nodeid1),
            )

            # update notifications
            cur.execute(
                """update notifications 
                    set deleted = TRUE 
                    where usersNode = %s and connectingNode = %s""",
                (nodeid1, nodeid2),
            )
            cur.execute(
                """update notifications 
                    set deleted = TRUE
                    where usersNode = %s and connectingNode = %s""",
                (nodeid2, nodeid1),
            )


def remove_from_saved(subId, nodeid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """delete from savedNodes where nodeId = %s and subId = %s;""",
                (nodeid, subId),
            )


def delete_notif(notifid):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""delete from notifications where notifId = %s;""", (notifid,))


# NOTE: Do we need this?
def remove_from_recent():
    return


# CHECK EXISTENCE
def connects(node1, node2):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """select count(1) from connections where ((nodeid1, nodeid2) = (%s, %s) 
                        or (nodeid2, nodeid1) = (%s, %s));""",
                (node1, node2, node1, node2),
            )
            count = cur.fetchone()
            if count.get("count") == 0:
                return False
            return True


def is_saved(sub_id, node_id):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """select count(1) from savedNodes where ((subid, nodeid) = (%s, %s));""",
                (sub_id, node_id),
            )
            count = cur.fetchone()
            if count.get("count") == 0:
                return False
            return True


# def view():
#     with pool.connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute("""SELECT
#                * FROM nodes
#             """)
#             a = cur.fetchall()

#             for i in a:
#                 print(i)
#             return cur.fetchall()


# def setup_text_search():
#     with pool.connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute("""
#                 ALTER TABLE nodes
#                 ADD COLUMN IF NOT EXISTS "textSearch" tsvector
#                 GENERATED ALWAYS AS (
#                     setweight(
#                         to_tsvector('english', coalesce(title, '')), 'A'
#                     ) ||
#                     setweight(
#                         to_tsvector('english', coalesce(description, '')), 'B'
#                     )
#                 ) STORED;
#             """)

#             cur.execute("""
#                 CREATE INDEX IF NOT EXISTS "textSearch_idx"
#                 ON nodes USING GIN ("textSearch");
#             """)


# def view_indexes():
#     with pool.connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute("""
#                 SELECT indexname, indexdef
#                 FROM pg_indexes
#                 WHERE schemaname = 'public'
#                   AND tablename = 'nodes';
#             """)

#             indexes = cur.fetchall()

#             for i in indexes:
#                 print(i)


# def main():
#     # setup_text_search()
#     view()
#     view_indexes()


# if __name__ == "__main__":
#     main()
