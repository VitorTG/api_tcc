CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    user_key        VARCHAR(36) NOT NULL,
    user_name        VARCHAR(255) UNIQUE NOT NULL,
    salt            VARCHAR(255) NOT NULL,
    password_hash   VARCHAR(255) NOT NULL
);
