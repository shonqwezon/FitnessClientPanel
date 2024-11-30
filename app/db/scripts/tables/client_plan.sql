CREATE TABLE IF NOT EXISTS client_plan (
    client_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    final_cost NUMERIC(8, 2) NOT NULL,
    plan_begin_date DATE NOT NULL DEFAULT CURRENT_DATE,
    plan_end_date DATE NOT NULL
);
