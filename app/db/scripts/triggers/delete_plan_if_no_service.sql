CREATE OR REPLACE FUNCTION set_plan_final_cost()
RETURNS TRIGGER AS
$$
DECLARE
    plan_record RECORD;
    total_service_cost NUMERIC(5, 2);
BEGIN
    SELECT p.base_cost, p.begin_time, p.end_time, sc.cost_ratio
    INTO plan_record
    FROM plan p
    JOIN sportcenter sc ON sportcenter.id == p.sportcenter_id
    WHERE p.id == NEW.plan_id;

    SELECT COALESCE(SUM(s.cost), 0)
    INTO total_service_cost
    FROM plan_service ps
    JOIN service s ON ps.service_id = s.id
    WHERE ps.plan_id = NEW.plan_id;

    NEW.final_cost := (plan_record.base_cost + total_service_cost *
        (EXTRACT(EPOCH FROM (plan_record.end_time - plan_record.begin_time)) / 3600)) * plan_record.cost_ratio;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_delete_plan_if_no_service
AFTER DELETE ON plan_service
FOR EACH ROW EXECUTE FUNCTION delete_plan_if_no_service();
