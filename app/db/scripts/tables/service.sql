CREATE TABLE IF NOT EXISTS service (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    cost NUMERIC(8, 2) NOT NULL
);

CREATE INDEX idx_description ON service (description);
