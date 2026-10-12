CREATE table node {
    nodeId serial PRIMARY KEY,
    title varchar(100),
    img BYTEA,
    description varchar(),
    creatorId int FOREIGN KEY,
    topic varchar(100)
};

CREATE table connections {
    node_1_id int FOREIGN KEY NOT NULL,
    node_2_id int FOREIGN KEY NOT NULL,
    connectorId int FOREIGN KEY NOT NULL,
    PRIMARY KEY (node_1_id, node_2_id)
};

CREATE table users {
    userId serial PRIMARY KEY,
    username varchar(50) NOT NULL,
    bio varchar(250),
    profPic BYTEA,
};

CREATE table savedNodes {
    userId FOREIGN KEY NOT NULL,
    nodeId FOREIGN KEY NOT NULL,
    PRIMARY KEY: (userId, nodeId)
};

CREATE table recentNodes {
    userId FOREIGN KEY NOT NULL,
    nodeId FOREIGN KEY NOT NULL,
    PRIMARY KEY: (userId, nodeId)
};