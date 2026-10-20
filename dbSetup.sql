CREATE table nodes (
    nodeId serial PRIMARY KEY,
    title varchar(100) NOT NULL,
    img BYTEA,
    description varchar(250),
    creatorId int,
    topic varchar(100),
    category boolean DEFAULT false, 
    FOREIGN KEY (creatorId) REFERENCES users,
    textSearch tsvector GENERATED ALWAYS AS    
    (setweight(to_tsvector('title', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('description', coalesce(description, '')), 'B')) STORED,

);
-- cannot create index within table most be made outside. this is for full text search
CREATE INDEX textSearch_idx
ON nodes USING GIN (textSearch);

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
    subId varchar(250) NOT NULL,
    username varchar(15) NOT NULL,
    bio varchar(250),
    profPic BYTEA
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