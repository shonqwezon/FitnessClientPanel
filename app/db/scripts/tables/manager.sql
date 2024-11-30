CREATE TABLE IF NOT EXISTS manager (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(50) NOT NULL,
    assign_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    sportcenter_id INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_manager_fullname ON manager (fullname); -- Для быстрого поиска по имени
