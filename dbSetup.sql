CREATE table nodes (
    nodeId serial PRIMARY KEY,
    title varchar(100),
    img BYTEA,
    description varchar(250),
    creatorId int,
    topic varchar(100),
    FOREIGN KEY (creatorId) REFERENCES users
);

CREATE table connections (
    nodeId1 int NOT NULL,
    nodeId2 int NOT NULL,
    connectorId int NOT NULL,
    PRIMARY KEY (nodeId1, nodeId2),
    FOREIGN KEY (connectorId) REFERENCES users
);

CREATE table users (
    userId serial PRIMARY KEY,
    username varchar(50) NOT NULL,
    bio varchar(250),
    profPic BYTEA
);

CREATE table savedNodes (
    userId int NOT NULL,
    nodeId int NOT NULL,
    FOREIGN KEY (userId) REFERENCES users,
    FOREIGN KEY (nodeId) REFERENCES nodes,
    PRIMARY KEY (userId, nodeId)
);

CREATE table recentNodes (
    userId int NOT NULL,
    nodeId int NOT NULL,
    FOREIGN KEY (userId) REFERENCES users,
    FOREIGN KEY (nodeId) REFERENCES nodes,
    PRIMARY KEY (userId, nodeId)
);