CREATE TABLE IF NOT EXISTS sportcenter (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    address VARCHAR(50) NOT NULL,
    open_time TIME NOT NULL,
    close_time TIME NOT NULL,
    cost_ratio NUMERIC(3,2) NOT NULL
);
