CREATE TABLE IF NOT EXISTS manager (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(50) NOT NULL,
    assigned_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    sportcenter_id INTEGER NOT NULL,
    FOREIGN KEY (sportcenter_id) REFERENCES sportcenter(id)
        ON UPDATE CASCADE ON DELETE CASCADE
        DEFERRABLE INITIALLY DEFERRED -- Для создания таблиц без конфликтов
);

CREATE INDEX idx_fullname ON manager (fullname); -- Для быстрого поиска по имени
