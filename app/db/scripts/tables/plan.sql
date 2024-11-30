CREATE TABLE IF NOT EXISTS plan (
    id SERIAL PRIMARY KEY,
    base_cost NUMERIC(8, 2) NOT NULL,
    begin_time TIME NOT NULL,
    end_time TIME NOT NULL,
    create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sportcenter_id INTEGER NOT NULL
);
