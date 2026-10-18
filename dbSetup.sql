--title and img currently not required in actual db (need to figure out images, also for simpler initial testing)
CREATE table nodes (
    nodeId serial PRIMARY KEY,
    title varchar(100) NOT NULL,
    img BYTEA NOT NULL,
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
    subId varchar(250) NOT NULL,
    username varchar(15) NOT NULL,
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


insert into users (username, bio) values ('chungus', 'I am chungus');

insert into nodes (title, description, creatorId) values ('cool dog', 'my dog is cool', 1);
insert into nodes (title, description, creatorId) values ('demure cat', 'this cat so demure', 1);

insert into connections (nodeId1, nodeId2, connectorId) values (1, 2, 1)  