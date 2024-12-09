CREATE TABLE IF NOT EXISTS plan (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL CHECK (name <> ''),
    base_cost NUMERIC(8, 2) NOT NULL,
    begin_time TIME NOT NULL,
    end_time TIME NOT NULL,
    create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sportcenter_id INTEGER NOT NULL,
    CONSTRAINT base_cost_check CHECK (base_cost >= 0),
    CONSTRAINT begin_end_time_check CHECK (begin_time < end_time),
    CONSTRAINT unique_plan UNIQUE (name, sportcenter_id)
);
