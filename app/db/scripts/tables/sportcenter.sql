CREATE TABLE IF NOT EXISTS sportcenter (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    address VARCHAR(50) NOT NULL,
    open_time TIME NOT NULL,
    close_time TIME NOT NULL,
    cost_ratio NUMERIC(3,2) NOT NULL DEFAULT 1,
    CONSTRAINT cost_ratio_check CHECK (cost_ratio > 0),
    CONSTRAINT open_close_time_check CHECK (open_time < close_time)
);
