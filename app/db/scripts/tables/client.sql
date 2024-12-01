CREATE TABLE IF NOT EXISTS client (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(50) NOT NULL,
    balance NUMERIC(8, 2) NOT NULL DEFAULT 0,
    reg_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT balance_check CHECK (balance >= 0)
);

CREATE INDEX IF NOT EXISTS idx_client_fullname ON client (fullname);
