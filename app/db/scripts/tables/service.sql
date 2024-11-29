CREATE TABLE IF NOT EXISTS service (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    cost REAL NOT NULL
);

CREATE INDEX idx_description ON service (description);
