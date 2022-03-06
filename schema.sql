CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE user_info (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    names TEXT,
    phone TEXT,
    FOREIGN KEY (user_id) REFERENCES users
    ON DELETE CASCADE
);

CREATE TABLE checkpoints (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    ordinal INTEGER,
    theme TEXT,
    location TEXT,
    FOREIGN KEY (user_id) REFERENCES users
    ON DELETE CASCADE
);

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    teams_id INTEGER,
    checkpoint_id INTEGER,
    points INTEGER,
    review TEXT,
    FOREIGN KEY (teams_id) REFERENCES teams
    ON DELETE CASCADE,
    FOREIGN KEY (checkpoint_id) REFERENCES checkpoints
    ON DELETE SET NULL
);
