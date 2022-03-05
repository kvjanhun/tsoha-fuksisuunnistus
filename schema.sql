CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
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
    ordinal INTEGER,
    theme TEXT,
    location TEXT
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    groups_id INTEGER,
    checkpoint_id INTEGER,
    points INTEGER,
    review TEXT,
    FOREIGN KEY (groups_id) REFERENCES groups
    ON DELETE CASCADE,
    FOREIGN KEY (checkpoint_id) REFERENCES checkpoint
    ON DELETE SET NULL
);

