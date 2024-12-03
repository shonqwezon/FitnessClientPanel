CREATE OR REPLACE FUNCTION app.calculate_plan_cost(in_plan_id INTEGER)
RETURNS NUMERIC(8, 2)
SECURITY DEFINER
AS $$
DECLARE
    plan_record RECORD;
    total_service_cost NUMERIC(5, 2);
    final_cost NUMERIC(8, 2);
BEGIN
    SELECT p.base_cost, p.begin_time, p.end_time, sc.cost_ratio
    INTO plan_record
    FROM plan p
    JOIN sportcenter sc ON sc.id = p.sportcenter_id
    WHERE p.id = in_plan_id;

    SELECT COALESCE(SUM(s.cost), 0)
    INTO total_service_cost
    FROM plan_service ps
    JOIN service s ON ps.service_id = s.id
    WHERE ps.plan_id = in_plan_id;

    final_cost := (plan_record.base_cost + total_service_cost *
        (EXTRACT(EPOCH FROM (plan_record.end_time - plan_record.begin_time)) / 3600)) * plan_record.cost_ratio;

    RAISE NOTICE 'Final cost for plan "%" has been calculated.', in_plan_id;
    RETURN final_cost;
END;
$$ LANGUAGE plpgsql;
