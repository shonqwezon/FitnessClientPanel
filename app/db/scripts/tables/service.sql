CREATE TABLE IF NOT EXISTS service (
    id SERIAL PRIMARY KEY,
    description TEXT UNIQUE NOT NULL,
    cost NUMERIC(5, 2) NOT NULL,
    CONSTRAINT cost_check CHECK (cost >= 0)
);
