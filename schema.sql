CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE user_info (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    names TEXT,
    phone TEXT
);

CREATE TABLE checkpoint (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    theme TEXT,
    location TEXT
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT,
    size INTEGER,
    points INTEGER
);