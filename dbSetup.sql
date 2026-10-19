CREATE table nodes (
    nodeId serial PRIMARY KEY,
    title varchar(100) NOT NULL,
    imgId int,
    description varchar(250),
    creatorId int,
    topic varchar(100),
    category boolean DEFAULT false, 
    FOREIGN KEY (creatorId) REFERENCES users,
    FOREIGN KEY (img) REFERENCES images
);

CREATE TABLE images (
    imageId serial PRIMARY KEY,
    filename varchar(255),
    mimetype varchar(100) NOT NULL,
    data BYTEA NOT NULL
);

CREATE table connections (
    nodeId1 int NOT NULL,
    nodeId2 int NOT NULL,
    connectorId int NOT NULL,
    PRIMARY KEY (nodeId1, nodeId2),
    FOREIGN KEY (nodeId1) REFERENCES nodes ON DELETE CASCADE,
    FOREIGN KEY (nodeId2) REFERENCES nodes ON DELETE CASCADE,
    FOREIGN KEY (connectorId) REFERENCES users
);

-- TODO: auth0 stuff
CREATE table users (
    userId serial PRIMARY KEY,
    username varchar(50) NOT NULL,
    bio varchar(250),
    profPicId int,
    FOREIGN KEY (profPic) REFERENCES images
);

CREATE table savedNodes (
    userId int NOT NULL,
    nodeId int NOT NULL,
    FOREIGN KEY (userId) REFERENCES users,
    FOREIGN KEY (nodeId) REFERENCES nodes ON DELETE CASCADE,
    PRIMARY KEY (userId, nodeId)
);

CREATE table recentNodes (
    userId int NOT NULL,
    nodeId int NOT NULL,
    timestamp varchar(50),
    FOREIGN KEY (userId) REFERENCES users,
    FOREIGN KEY (nodeId) REFERENCES nodes ON DELETE CASCADE,
    PRIMARY KEY (userId, nodeId)
);

CREATE table notifications (
    notifId serial PRIMARY KEY,
    recipient int NOT NULL,
    connector int NOT NULL,
    usersNode int NOT NULL,
    connectingNode int NOT NULL,
    timestamp varchar(50),
    FOREIGN KEY (recipient) REFERENCES users,
    FOREIGN KEY (connector) REFERENCES users,
    FOREIGN KEY (usersNode) REFERENCES nodes,
    FOREIGN KEY (connectingNode) REFERENCES nodes
);

insert into notifications (recipient, connector, usersnode, connectingNode) values (1, 2, 5, 6);

insert into users (username, bio) values ('chungus', 'I am chungus');

insert into nodes (title, description, creatorId) values ('cool dog', 'my dog is cool', 1);
insert into nodes (title, description, creatorId) values ('demure cat', 'this cat so demure', 1);

insert into connections (nodeId1, nodeId2, connectorId) values (1, 2, 1);