DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    uuid_ BINARY(16) NOT NULL PRIMARY KEY,
    name VARCHAR(32) NOT NULL
);

CREATE TABLE tasks (
    uuid BINARY(16) PRIMARY KEY,
    description NVARCHAR(1024),
    completed BOOLEAN,
    user_uuid BINARY(16) NOT NULL,
    FOREIGN KEY (user_uuid) REFERENCES users(uuid_) ON DELETE CASCADE
);