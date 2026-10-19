CREATE table nodes (
    nodeId serial PRIMARY KEY,
    title varchar(100) NOT NULL,
    imgId int,
    description varchar(250),
    --creatorId int,
    subId varchar(255),
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
    connectorId varchar(255) NOT NULL,
    PRIMARY KEY (nodeId1, nodeId2),
    FOREIGN KEY (nodeId1) REFERENCES nodes ON DELETE CASCADE,
    FOREIGN KEY (nodeId2) REFERENCES nodes ON DELETE CASCADE,
    FOREIGN KEY (connectorId) REFERENCES users
);

-- TODO: auth0 stuff
CREATE table users (
    userId serial PRIMARY KEY,
    subId varchar(250) NOT NULL UNIQUE,
    username varchar(15) NOT NULL,
    bio varchar(250),
    profPicId int,
    FOREIGN KEY (profPic) REFERENCES images
);

CREATE table savedNodes (
    userId int NOT NULL,
    nodeId int NOT NULL,
    subId varchar(255),
    FOREIGN KEY (userId) REFERENCES users,
    FOREIGN KEY (nodeId) REFERENCES nodes ON DELETE CASCADE,
    FOREIGN KEY (subId) REFERENCES users,
    PRIMARY KEY (userId, nodeId)
);

CREATE table recentNodes (
    userId int NOT NULL,
    nodeId int NOT NULL,
    subId varchar(255),
    timestamp varchar(50),
    FOREIGN KEY (userId) REFERENCES users,
    FOREIGN KEY (nodeId) REFERENCES nodes ON DELETE CASCADE,
    FOREIGN KEY (subId) REFERENCES users,
    PRIMARY KEY (userId, nodeId)
);

CREATE table notifications (
    notifId serial PRIMARY KEY,
    recipient varchar(255) NOT NULL,
    connector varchar(255) NOT NULL,
    usersNode int NOT NULL,
    connectingNode int NOT NULL,
    timestamp varchar(50),
    FOREIGN KEY (recipient) REFERENCES users(subid),
    FOREIGN KEY (connector) REFERENCES users(subid),
    FOREIGN KEY (usersNode) REFERENCES nodes,
    FOREIGN KEY (connectingNode) REFERENCES nodes
);

insert into users (username, bio) values ('chungus', 'I am chungus');

insert into nodes (title, description, creatorId) values ('cool dog', 'my dog is cool', 1);
insert into nodes (title, description, creatorId) values ('demure cat', 'this cat so demure', 1);

insert into connections (nodeId1, nodeId2, connectorId) values (1, 2, 1);