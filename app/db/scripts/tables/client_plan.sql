CREATE TABLE IF NOT EXISTS client_plan (
    client_id INTEGER,
    plan_id INTEGER,
    final_cost NUMERIC(8, 2) NOT NULL,
    plan_begin_date DATE NOT NULL DEFAULT CURRENT_DATE,
    plan_end_date DATE NOT NULL,
    CONSTRAINT pk_client_plan PRIMARY KEY (client_id, plan_id),
    CONSTRAINT final_cost_check CHECK (final_cost_check >= 0),
    CONSTRAINT begin_end_date_check CHECK (plan_begin_date <= plan_end_date)
);
