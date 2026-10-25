"""
A bunch of helper functions for node related formatting and functionality!
"""
import developing_the_interactive_web_project_1_group_5.database as database

def format_node_display(query=[]):
    # Formatter for displaying any nodes that aren't the current node for jinja vars
    if (query == []):
        return []
    connections = []
    for node in query:
        connections.append (
            {
            "image_id": dict_get(node, "imgid", None),
            "node_title": dict_get(node, "title", "Untitled"),
            "node_description": dict_get(node, "description", ""),
            "link": "/node/" + str(dict_get(node, "nodeid", "doesnotexist")),
            "node_id": str(dict_get(node, "nodeid", "doesnotexist")),
            "creator_id": str(dict_get(node, "subid", 1))
            })
    return connections
    
def dict_get(dict, key, default):
    # Fetch value of key from dictionary, return default if none
    return (dict.get(key) or default)

def get_popular_nodes():
    # Order by number of connections and return n nodes
    # NOTE: removed n nodes, we are returning them all
    all_nodes = database.get_all_nodes()
    popularities = []
    for node in all_nodes:
        nodeid = node.get("nodeid")
        connection_count = len(database.get_node_connections(nodeid))
        node["connection_count"] = connection_count
        popularities.append(node)
    popularities.sort(key=lambda x: x["connection_count"], reverse=True)
    return popularities

def add_selections(subid, newConnections=[]):
    for node_id in newConnections:
        database.add_connection(node_id[0], node_id[1], subid)

def filter_connecting_nodes(node_list, curr_node_id):
    # Remove already existing connections and the node itself for connection modal
    for node in node_list[:]:
        if ((int(node.get("node_id")) == int(curr_node_id)) or (database.connects(node.get("node_id"), curr_node_id))):
            node_list.remove(node)
    return node_list

# retrieve n nodes recently connected to saved and created nodes
def get_new_connections(subid, n=30):
    my_nodes = database.get_user_nodes(subid)
    my_nodes += database.get_saved_nodes(subid)

    new_connections = []

    for node in my_nodes:
        # Don't add the connections you yourself added
        connected_nodes = database.get_node_connections(node["nodeid"], subid)

        for connected in connected_nodes:
            # Don't add duplicates or your saved/created nodes
            if (connected not in new_connections) and (connected not in my_nodes):
                connected['timestamp'] = (database.get_node_connection(node["nodeid"], connected["nodeid"])["timestamp"])
                if (connected['timestamp'] != None):
                    new_connections.append(connected)
    new_connections.sort(key=lambda x: x["timestamp"], reverse=True)
    return new_connections[:n]