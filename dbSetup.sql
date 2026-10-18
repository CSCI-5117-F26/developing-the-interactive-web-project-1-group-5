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


insert into users (username, bio) values ('chungus', 'I am chungus');

insert into nodes (title, description, creatorId) values ('cool dog', 'my dog is cool', 1);
insert into nodes (title, description, creatorId) values ('demure cat', 'this cat so demure', 1);

insert into connections (nodeId1, nodeId2, connectorId) values (1, 2, 1);