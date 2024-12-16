CREATE TABLE IF NOT EXISTS plan_service (
    plan_id INTEGER,
    service_id INTEGER,
    CONSTRAINT pk_plan_service PRIMARY KEY (plan_id, service_id)
);
