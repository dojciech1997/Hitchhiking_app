CREATE TABLE IF NOT EXISTS person (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    photo_url VARCHAR(500),
    latitude FLOAT,
    longitude FLOAT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS tag (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS person_tag (
    person_id INTEGER REFERENCES person(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tag(id),
    PRIMARY KEY (person_id, tag_id)
);