CREATE TABLE IF NOT EXISTS client (
    id SERIAL PRIMARY KEY,
    balance NUMERIC(8, 2) NOT NULL DEFAULT 0,
    reg_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_fullname ON client (fullname);
