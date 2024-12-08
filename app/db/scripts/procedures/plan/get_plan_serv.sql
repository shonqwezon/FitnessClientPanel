CREATE OR REPLACE FUNCTION app.get_plan(service_ids INTEGER[] DEFAULT '{}')
RETURNS TABLE (id INTEGER,
                name VARCHAR(50),
                cost_per_month NUMERIC(8, 2),
                begin_time TIME,
                end_time TIME,
                body TEXT[],
                center_name VARCHAR(50),
                center_address VARCHAR(50))
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT p.id,
                        p.name,
                        app.calculate_plan_cost(p.id) * 30 AS cost_per_month,
                        p.begin_time,
                        p.end_time,
                        array_agg(s.description) AS body,
                        (SELECT sp.name FROM app.get_sportcenter(p.sportcenter_id) sp) AS center_name,
                        (SELECT address FROM app.get_sportcenter(p.sportcenter_id)) AS center_address
                FROM plan AS p
                JOIN plan_service ps ON ps.plan_id = p.id
                JOIN service s ON s.id = ps.service_id
                WHERE ps.service_id = ANY(service_ids)
                GROUP BY p.id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Plans with services_ids "%" for manager do not exist', service_ids;
    END IF;
END;
$$ LANGUAGE plpgsql;
