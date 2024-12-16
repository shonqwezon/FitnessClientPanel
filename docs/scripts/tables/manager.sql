CREATE TABLE IF NOT EXISTS manager (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(50) UNIQUE NOT NULL CHECK (fullname <> ''),
    assign_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email VARCHAR(50) UNIQUE NOT NULL CHECK (email <> ''),
    password_hash VARCHAR(64) NOT NULL CHECK (password_hash <> ''),
    sportcenter_id INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_pass_hash ON manager (password_hash);
