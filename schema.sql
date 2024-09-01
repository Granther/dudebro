DROP TABLE IF EXISTS containers;
DROP TABLE IF EXISTS users;

CREATE TABLE containers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subdomain TEXT,
    domain TEXT,
    port INT,
    weight INT,
    priority INT,
    name TEXT,
    userid INT,
    type TEXT,
    FOREIGN KEY(userid) REFERENCES users(id)
);

CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

-- sqlite3 dude.db < bro.sql