CREATE TABLE IF NOT EXISTS service (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    cost NUMERIC(5, 2) NOT NULL
);

CREATE INDEX idx_service_description ON service (description);
